import subprocess
import json

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
            process = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )
            if process.returncode != 0:
                error_message = process.stderr.decode("utf-8")
                return f"Erreur : {error_message}"

            return process.stdout.decode("utf-8").strip()
        except subprocess.TimeoutExpired:
            return "Erreur : Temps limite dépassé."
        except Exception as e:
            return f"Erreur inattendue : {str(e)}"

    def extract_course_structure(self, course_text):
        """
        Extrait une arborescence à partir du texte du cours.
        """
        structure = []
        lines = course_text.splitlines()
        current_section = None
        current_subsection = None

        for index, line in enumerate(lines):
            line = line.strip()
            if line.startswith("**Section") or line.startswith("**Introduction**"):
                current_section = {"title": line, "line_index": index, "children": []}
                structure.append(current_section)
                current_subsection = None
            elif line.startswith("###") and current_section:
                current_subsection = {"title": line, "line_index": index, "children": []}
                current_section["children"].append(current_subsection)
            elif line.startswith("*") and current_subsection:
                current_subsection["children"].append({"title": line, "line_index": index})

        return structure

    def display_course_tree(self, tree_widget, course_structure, on_select_callback=None):
        """
        Affiche l'arborescence du cours dans un widget Treeview.
        """
        # Nettoyage de l'arborescence existante
        for item in tree_widget.get_children():
            tree_widget.delete(item)

        # Dictionnaire pour mapper les IDs Treeview à des indices de ligne
        tree_item_map = {}

        # Remplir l'arborescence avec la nouvelle structure
        for section in course_structure:
            section_id = tree_widget.insert("", "end", text=section["title"])
            tree_item_map[section_id] = section["line_index"]
            for subsection in section["children"]:
                subsection_id = tree_widget.insert(section_id, "end", text=subsection["title"])
                tree_item_map[subsection_id] = subsection["line_index"]
                for item in subsection["children"]:
                    item_id = tree_widget.insert(subsection_id, "end", text=item["title"])
                    tree_item_map[item_id] = item["line_index"]

        # Associer l'événement de sélection uniquement si un callback est fourni
        if on_select_callback:
            tree_widget.bind("<<TreeviewSelect>>", lambda event: on_select_callback(event, tree_item_map))

        return tree_item_map
