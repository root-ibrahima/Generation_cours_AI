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
