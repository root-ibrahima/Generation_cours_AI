import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ai_course_generator import AICourseGenerator

class CourseApp:
    """
    Interface utilisateur pour générer des cours avec Ollama.
    """

    def __init__(self):
        self.generator = AICourseGenerator(model="llama3.2")
        self.tree_item_map = {}  # Assure que tree_item_map est défini
        self.root = tk.Tk()
        self.root.title("Créateur de Cours avec Ollama")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        """
        Configure l'interface utilisateur.
        """
        # Cadre principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cadre pour l'arborescence (à gauche)
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Widget Treeview pour afficher l'arborescence
        self.course_tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
        self.course_tree.pack(fill=tk.Y, expand=True)

        # Bouton pour régénérer une partie spécifique
        self.regenerate_part_button = ttk.Button(tree_frame, text="Régénérer la partie", command=self.on_regenerate_part)
        self.regenerate_part_button.pack(pady=10)
        self.regenerate_part_button.config(state=tk.DISABLED)

        # Cadre pour le contenu (à droite)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sujet du cours
        ttk.Label(content_frame, text="Sujet du Cours :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.topic_entry = ttk.Entry(content_frame, width=50)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10)
        self.topic_entry.bind("<Return>", self.on_topic_entered)

        # Bouton pour régénérer le cours
        self.regenerate_button = ttk.Button(content_frame, text="Régénérer", command=self.on_regenerate)
        self.regenerate_button.grid(row=0, column=2, padx=10, pady=10)
        self.regenerate_button.config(state=tk.DISABLED)

        # Indicateur de statut
        self.status_label = ttk.Label(content_frame, text="Prêt", foreground="green")
        self.status_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Zone de texte pour afficher le contenu généré
        ttk.Label(content_frame, text="Cours généré :").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.course_text = tk.Text(content_frame, wrap=tk.WORD, width=60, height=25)
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
        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, "Génération en cours...\n")
        self.status_label.config(text="Génération en cours...", foreground="orange")
        self.root.update()

        # Désactiver les boutons pendant la génération
        self.regenerate_button.config(state=tk.DISABLED)
        self.regenerate_part_button.config(state=tk.DISABLED)

        # Lancer la génération dans un thread séparé
        threading.Thread(target=self.generate_course_in_thread, args=(topic,)).start()

    def generate_course_in_thread(self, topic):
        """
        Génère un cours dans un thread séparé pour éviter de bloquer l'interface.
        """
        try:
            # Génère le texte du cours
            course = self.generator.generate_course(topic)
            # Affiche le texte complet dans la zone de texte
            self.course_text.delete("1.0", tk.END)
            self.course_text.insert(tk.END, course)

            # Extrait et affiche l'arborescence
            course_structure = self.generator.extract_course_structure(course)
            self.tree_item_map = self.generator.display_course_tree(self.course_tree, course_structure, self.scroll_to_section)

            # Activer les boutons après la génération
            self.regenerate_button.config(state=tk.NORMAL)
            self.regenerate_part_button.config(state=tk.NORMAL)
            self.status_label.config(text="Génération terminée", foreground="green")
        except Exception as e:
            print(f"Erreur lors de la génération : {str(e)}")
            self.course_text.delete("1.0", tk.END)
            self.course_text.insert(tk.END, f"Erreur : {str(e)}")
            self.regenerate_button.config(state=tk.NORMAL)
            self.status_label.config(text="Erreur lors de la génération", foreground="red")

    def on_regenerate(self):
        """
        Gère la régénération du cours avec le même sujet.
        """
        confirm = messagebox.askyesno("Confirmation", "Voulez-vous régénérer le cours ?")
        if not confirm:
            return

        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, "Régénération en cours...\n")
        self.status_label.config(text="Régénération en cours...", foreground="orange")
        self.root.update()

        # Désactiver les boutons pendant la régénération
        self.regenerate_button.config(state=tk.DISABLED)
        self.regenerate_part_button.config(state=tk.DISABLED)

        # Lancer la régénération dans un thread séparé
        threading.Thread(target=self.generate_course_in_thread, args=(self.topic,)).start()

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

        # Récupère le titre de la partie sélectionnée
        part_title = self.course_tree.item(selected_item, "text")
        confirm = messagebox.askyesno("Confirmation", f"Voulez-vous régénérer la partie '{part_title}' ?")
        if not confirm:
            return

        self.course_text.insert("end", f"\nRégénération de la partie : {part_title} en cours...\n")
        self.status_label.config(text=f"Régénération de '{part_title}' en cours...", foreground="orange")
        self.root.update()

        # Lancer la régénération de la partie dans un thread séparé
        threading.Thread(target=self.generate_part_in_thread, args=(part_title,)).start()

    def generate_part_in_thread(self, part_title):
        """
        Régénère une partie spécifique du cours dans un thread séparé.
        """
        try:
            # Génère le texte pour la partie spécifique
            part_content = self.generator.generate_course(part_title)
            # Remplace uniquement le texte de la partie sélectionnée
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
        except Exception as e:
            print(f"Erreur lors de la régénération de la partie : {str(e)}")
            self.course_text.insert("end", f"\nErreur lors de la régénération de '{part_title}' : {str(e)}\n")
            self.status_label.config(text="Erreur lors de la régénération", foreground="red")

    def scroll_to_section(self, event, tree_item_map):
        """
        Fait défiler la zone de texte jusqu'à la section correspondante lorsqu'un élément de l'arborescence est sélectionné.
        """
        selected_item = self.course_tree.focus()
        if selected_item in tree_item_map:
            line_index = tree_item_map[selected_item]
            self.course_text.see(f"{line_index + 1}.0")

    def run(self):
        """
        Lance l'application Tkinter.
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = CourseApp()
    app.run()
