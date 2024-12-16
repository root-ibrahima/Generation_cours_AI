from ui_manager import CourseApp
import os
import subprocess

# Ajouter le chemin d'Ollama à PATH si nécessaire
ollama_path = r"C:\Users\Ohlone\AppData\Local\Programs\Ollama"
if ollama_path not in os.environ["PATH"]:
    os.environ["PATH"] += f";{ollama_path}"

# Vérifier si Ollama est accessible
try:
    process = subprocess.run(
        ["ollama", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10
    )
    print("Ollama version :", process.stdout.decode("utf-8").strip())
except Exception as e:
    print(f"Erreur lors de la vérification d'Ollama : {str(e)}")

# Lancer l'application
if __name__ == "__main__":
    try:
        app = CourseApp()
        app.run()
    except Exception as e:
        print(f"Erreur : {str(e)}")
