# Fichier : ai_course_generator.py
import subprocess

class AICourseGenerator:
    """
    Classe pour interagir avec Ollama en local et générer des cours.
    """

    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_course(self, topic):
        """
        Génère un cours structuré sur un sujet donné en utilisant le modèle Ollama.
        """
        prompt = (
            f"Crée un cours structuré et détaillé sur le sujet '{topic}'. "
            "Le cours doit inclure une introduction, des sections principales (I, II, III), "
            "et des sous-sections (A, B, C)."
        )
        try:
            print(f"Lancement de la commande : ollama run {self.model}")
            process = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )
            if process.returncode != 0:
                error_message = process.stderr.decode("utf-8")
                print(f"Erreur rencontrée : {error_message}")
                return f"Erreur : {error_message}"

            response = process.stdout.decode("utf-8").strip()
            print(f"Réponse reçue : {response}")
            return response

        except subprocess.TimeoutExpired:
            print("Erreur : Temps limite dépassé.")
            return "Erreur : Temps limite dépassé pour l'exécution d'Ollama."
        except Exception as e:
            print(f"Erreur inattendue : {str(e)}")
            return f"Erreur inattendue : {str(e)}"

    def extract_course_structure(self, course_text):
        """
        Extrait une arborescence à partir du texte du cours.
        """
        structure = []
        lines = course_text.splitlines()
        current_section = None
        current_subsection = None

        for line in lines:
            line = line.strip()
            if line.startswith("**Introduction**") or line.startswith("**Section"):
                current_section = {"title": line, "children": []}
                structure.append(current_section)
            elif line.startswith("###"):
                current_subsection = {"title": line, "children": []}
                if current_section:
                    current_section["children"].append(current_subsection)
            elif line.startswith("*") and current_subsection:
                current_subsection["children"].append(line)

        return structure

    def display_course_tree(self, tree_widget, course_structure):
        """
        Affiche l'arborescence du cours dans un widget Treeview.
        """
        # Nettoyage de l'arborescence existante
        for item in tree_widget.get_children():
            tree_widget.delete(item)

        # Remplir l'arborescence avec la nouvelle structure
        for section in course_structure:
            section_id = tree_widget.insert("", "end", text=section["title"])
            for subsection in section["children"]:
                subsection_id = tree_widget.insert(section_id, "end", text=subsection["title"])
                for item in subsection["children"]:
                    tree_widget.insert(subsection_id, "end", text=item)
