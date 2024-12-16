# Fichier : ui_manager.py
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

        self.root = tk.Tk()
        self.root.title("Créateur de Cours avec Ollama")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        """
        Configure l'interface utilisateur.
        """
        # Sujet du cours
        ttk.Label(self.root, text="Sujet du Cours :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.topic_entry = ttk.Entry(self.root, width=50)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10)
        self.topic_entry.bind("<Return>", self.on_topic_entered)

        # Zone de texte pour afficher le cours généré
        ttk.Label(self.root, text="Cours généré :").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.course_text = tk.Text(self.root, wrap=tk.WORD, width=80, height=25)
        self.course_text.grid(row=1, column=1, padx=10, pady=10)

    def on_topic_entered(self, event):
        """
        Gère l'entrée utilisateur pour générer un cours.
        """
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Sujet vide", "Veuillez entrer un sujet pour générer un cours.")
            return

        self.course_text.delete("1.0", tk.END)
        self.course_text.insert(tk.END, "Génération en cours...\n")
        self.root.update()

        # Lancer la génération dans un thread séparé
        threading.Thread(target=self.generate_course_in_thread, args=(topic,)).start()

    def generate_course_in_thread(self, topic):
        """
        Génère un cours dans un thread séparé pour éviter de bloquer l'interface.
        """
        try:
            course = self.generator.generate_course(topic)
            self.course_text.delete("1.0", tk.END)
            self.course_text.insert(tk.END, course)
        except Exception as e:
            print(f"Erreur lors de la génération : {str(e)}")
            self.course_text.delete("1.0", tk.END)
            self.course_text.insert(tk.END, f"Erreur : {str(e)}")

    def run(self):
        """
        Lance l'application Tkinter.
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = CourseApp()
    app.run()
