# Créateur de Cours AI avec Ollama

Ce projet est une application graphique construite en Python, qui génère des cours détaillés et structurés à l'aide du modèle Ollama. Il permet de créer des cours sur n'importe quel sujet en offrant une interface utilisateur intuitive avec des fonctionnalités comme l'affichage d'arborescence, la régénération de contenu, et la navigation dans le contenu généré.

## Fonctionnalités

- **Génération automatique de cours** : Saisissez un sujet et laissez l'application générer un cours structuré avec une introduction, des sections principales, et des sous-sections.
- **Arborescence intuitive** : Affiche les sections principales du cours sous forme d'arborescence pour une navigation rapide.
- **Régénération ciblée** : Régénérez l'intégralité du cours ou une partie spécifique.
- **Interface utilisateur moderne** : Construite avec Tkinter pour une utilisation facile.

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Ollama installé localement (ajoutez son chemin à votre PATH si nécessaire)
- Les bibliothèques Python suivantes :
- tkinter (inclus dans la plupart des installations Python)
- threading

### Étapes

1. Clonez ce dépôt :
        ```bash
        git clone https://github.com/votre-utilisateur/votre-repo.git
        cd votre-repo
        ```
2. Installez les dépendances si nécessaire :
        ```bash
        pip install -r requirements.txt
        ```
3. Ajoutez Ollama à votre PATH si ce n'est pas déjà fait :
        ```bash
        export PATH=$PATH:/chemin/vers/ollama
        ```

## Utilisation

Lancez l'application :

```bash
python main.py
```

### Interface utilisateur

1. Entrez un sujet dans la barre de texte dédiée.
2. Cliquez sur "Régénérer" pour générer un cours sur ce sujet.
3. Utilisez l'arborescence pour naviguer entre les sections principales.
4. Cliquez sur "Régénérer la partie" pour modifier uniquement une section sélectionnée.

### Exemple de sujet

- "Introduction à l'intelligence artificielle"
- "Les bases de la programmation en Python"

## Détails techniques

### Modules principaux

- `ai_course_generator.py` : Interface avec Ollama pour générer et traiter le contenu des cours.
- `ui_manager.py` : Gère l'interface utilisateur avec Tkinter.
- `main.py` : Point d'entrée du projet, configure Ollama et lance l'application.

### Modèle utilisé

- Ollama Llama3.2

### Gestion des threads

- Empêche le blocage de l'interface en déplaçant les tâches intensives dans des threads séparés.

## Dépannage

### Erreur : Ollama introuvable

- Vérifiez que Ollama est installé et accessible via le PATH. Ajoutez son chemin si nécessaire.

### Temps limite dépassé

- Assurez-vous que Ollama fonctionne correctement ou augmentez le délai dans `subprocess.run()`.

## Contribuer

Les contributions sont les bienvenues ! Forkez ce dépôt et ouvrez une Pull Request avec vos améliorations ou suggestions.
