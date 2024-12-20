import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from ai_course_generator import AICourseGenerator
import json

class CourseApp:
    """
    Interface utilisateur pour générer des cours avec Ollama.
    """

    def __init__(self):
        self.generator = AICourseGenerator(model="llama3.2")
        self.tree_item_map = {}
        self.course_structure = None  # Initialise la structure du cours
        self.root = tk.Tk()
        self.root.title("Créateur de Cours avec Ollama")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self._setup_ui()

    def _setup_ui(self):
        """
        Configure l'interface utilisateur.
        """
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._setup_tree_frame(main_frame)
        self._setup_content_frame(main_frame)

    def _setup_tree_frame(self, parent):
        """
        Configure le cadre de l'arborescence.
        """
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.course_tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
        self.course_tree.pack(fill=tk.Y, expand=True)

        self.regenerate_part_button = ttk.Button(tree_frame, text="Régénérer la partie", command=self.on_regenerate_part)
        self.regenerate_part_button.pack(pady=5)
        self.regenerate_part_button.config(state=tk.DISABLED)

        self.export_button = ttk.Button(tree_frame, text="Exporter JSON", command=self.export_json)
        self.export_button.pack(pady=5)

        self.import_button = ttk.Button(tree_frame, text="Importer JSON", command=self.import_json)
        self.import_button.pack(pady=5)

    def _setup_content_frame(self, parent):
        """
        Configure le cadre de contenu.
        """
        content_frame = ttk.Frame(parent)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(content_frame, text="Sujet du Cours :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.topic_entry = ttk.Entry(content_frame, width=50)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10)
        self.topic_entry.bind("<Return>", self.on_topic_entered)

        self.regenerate_button = ttk.Button(content_frame, text="Régénérer", command=self.on_regenerate)
        self.regenerate_button.grid(row=0, column=2, padx=10, pady=10)
        self.regenerate_button.config(state=tk.DISABLED)

        self.status_label = ttk.Label(content_frame, text="Prêt", foreground="green")
        self.status_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(content_frame, text="Cours généré :").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.course_text = tk.Text(content_frame, wrap=tk.WORD, width=80, height=30)
        self.course_text.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    def on_topic_entered(self, event):
        """
        Gère l'entrée utilisateur pour générer un cours.
        """
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Sujet vide", "Veuillez entrer un sujet pour générer un cours.")
            return

        self.topic = topic
        self._start_course_generation(topic)

    def _start_course_generation(self, topic):
        """
        Démarre la génération du cours.
        """
        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, "Génération en cours...\n")
        self.status_label.config(text="Génération en cours...", foreground="orange")
        self._toggle_buttons(state=tk.DISABLED)

        threading.Thread(target=self.generate_course_in_thread, args=(topic,)).start()

    def generate_course_in_thread(self, topic):
        """
        Génère un cours dans un thread séparé pour éviter de bloquer l'interface.
        """
        try:
            course = self.generator.generate_course(topic)
            self._display_generated_course(course)
        except Exception as e:
            self._handle_generation_error(e)

    def _display_generated_course(self, course):
        """
        Affiche le cours généré et met à jour l'interface.
        """
        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, course)

        self.course_structure = self.generator.extract_course_structure(course)  # Stocke la structure du cours
        self.tree_item_map = self.generator.display_course_tree(self.course_tree, self.course_structure, self.scroll_to_section)

        self._toggle_buttons(state=tk.NORMAL)
        self.status_label.config(text="Génération terminée", foreground="green")

    def _handle_generation_error(self, error):
        """
        Gère les erreurs de génération.
        """
        print(f"Erreur lors de la génération : {str(error)}")
        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, f"Erreur : {str(error)}")
        self._toggle_buttons(state=tk.NORMAL)
        self.status_label.config(text="Erreur lors de la génération", foreground="red")

    def on_regenerate(self):
        """
        Gère la régénération du cours avec le même sujet.
        """
        confirm = messagebox.askyesno("Confirmation", "Voulez-vous régénérer le cours ?")
        if not confirm:
            return

        self._start_course_generation(self.topic)

    def on_regenerate_part(self):
        """
        Gère la régénération d'une partie spécifique du cours.
        """
        selected_item = self.course_tree.focus()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une partie à régénérer dans l'arborescence.")
            return

        if not isinstance(self.tree_item_map, dict) or selected_item not in self.tree_item_map:
            messagebox.showerror("Erreur", "Impossible de trouver la partie sélectionnée.")
            return

        part_title = self.course_tree.item(selected_item, "text")
        confirm = messagebox.askyesno("Confirmation", f"Voulez-vous régénérer la partie '{part_title}' ?")
        if not confirm:
            return

        self._start_part_regeneration(part_title)

    def _start_part_regeneration(self, part_title):
        """
        Démarre la régénération d'une partie spécifique du cours.
        """
        self.course_text.insert("end", f"\nRégénération de la partie : {part_title} en cours...\n")
        self.status_label.config(text=f"Régénération de '{part_title}' en cours...", foreground="orange")
        self._toggle_buttons(state=tk.DISABLED)

        threading.Thread(target=self.generate_part_in_thread, args=(part_title,)).start()

    def generate_part_in_thread(self, part_title):
        """
        Régénère une partie spécifique du cours dans un thread séparé.
        """
        try:
            part_content = self.generator.generate_course(part_title)
            self._replace_part_content(part_title, part_content)
        except Exception as e:
            self._handle_part_regeneration_error(part_title, e)

    def _replace_part_content(self, part_title, part_content):
        """
        Remplace le contenu d'une partie spécifique du cours.
        """
        lines = self.course_text.get("1.0", "end").splitlines()
        new_lines = []
        replacing = False
        for line in lines:
            if line.strip() == part_title:
                replacing = True
                new_lines.append(f"{part_title}\n{part_content}")
            elif replacing and not line.strip():
                replacing = False
            elif not replacing:
                new_lines.append(line)

        self.course_text.delete("1.0", tk.END)
        self.course_text.insert("1.0", "\n".join(new_lines))

        self.status_label.config(text=f"Régénération de '{part_title}' terminée", foreground="green")
        self._toggle_buttons(state=tk.NORMAL)

    def _handle_part_regeneration_error(self, part_title, error):
        """
        Gère les erreurs de régénération de partie.
        """
        print(f"Erreur lors de la régénération de la partie : {str(error)}")
        self.course_text.insert("end", f"\nErreur lors de la régénération de '{part_title}' : {str(error)}\n")
        self.status_label.config(text="Erreur lors de la régénération", foreground="red")
        self._toggle_buttons(state=tk.NORMAL)

    def scroll_to_section(self, event, tree_item_map):
        """
        Fait défiler la zone de texte jusqu'à la section correspondante lorsqu'un élément de l'arborescence est sélectionné.
        """
        selected_item = self.course_tree.focus()
        if selected_item in tree_item_map:
            line_index = tree_item_map[selected_item]
            self.course_text.see(f"{line_index + 1}.0")

    def export_json(self):
        """
        Exporte le cours actuel et sa structure en JSON.
        """
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Fichiers JSON", "*.json")])
            if not filepath:
                return

            data = {
                "text": self.course_text.get("1.0", tk.END).strip(),
                "structure": self.course_structure
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Succès", "Cours exporté avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {str(e)}")

    def import_json(self):
        """
        Importe un cours et sa structure depuis un fichier JSON.
        """
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
            if not filepath:
                return

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.course_text.delete("1.0", tk.END)
            self.course_text.insert("1.0", data["text"])
            self.course_structure = data["structure"]
            self.tree_item_map = self.generator.display_course_tree(self.course_tree, self.course_structure, self.scroll_to_section)
            messagebox.showinfo("Succès", "Cours importé avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'importation : {str(e)}")

    def _toggle_buttons(self, state):
        """
        Active ou désactive les boutons de l'interface.
        """
        self.regenerate_button.config(state=state)
        self.regenerate_part_button.config(state=state)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CourseApp()
    app.run()
