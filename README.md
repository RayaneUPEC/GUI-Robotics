# GUI_robotics
Interface Graphique (Graphical User Interface)
Ce projet est une interface graphique (GUI) pour visualiser et simuler les mouvements des articulations en utilisant le moteur de physique MuJoCo. L'interface est construite avec PyQt5 et intègre Matplotlib pour l'affichage et la visualisation des données. Les principales fonctionnalités incluent le contrôle de la simulation, la visualisation des données, les réglages de contrôle du mouvement et la détection de défauts.

Fonctionnalités :
Fenêtre d'Ouverture
Écran d'accueil: Affiche un écran introductif avec une image et des boutons pour ouvrir l'interface principale ou fermer l'application.
Interface Principale (MuJoCoApp)

Onglet Simulation:

Visualisation 3D/2D: Affiche les positions et mouvements des articulations en 3D et 2D.
Valeurs des Articulations: Affiche les valeurs actuelles des positions de chaque articulation.
Détection de Défauts: Surveille et affiche les défauts de la simulation.
Indicateur de Batterie et d'État: Montre le niveau de batterie et l'état actuel de la simulation.
Affichage d'Action: Affiche l'action en cours de simulation.
Boutons de Contrôle: Boutons pour démarrer et arrêter la simulation.
Onglet Mouvement:

Charger CSV: Charger des données de mouvement à partir d'un fichier CSV.
Enregistrer CSV: Enregistrer les données de mouvement actuelles dans un fichier CSV.
Zone de Traçage: Visualise les données de mouvement chargées.
Bouton de Sortie: Fermer l'application.
Onglet Contrôle du Mouvement:

Charger le CSV de Mouvement: Charger des données de mouvement pour les réglages de contrôle.
Réconversion et Confirmation: Boutons pour la réconversion et la confirmation des réglages de contrôle du mouvement.
Zone de Traçage: Visualise les données de contrôle du mouvement.
Onglet Données:

Matplotlib Canvas: Zone de traçage pour visualiser les données des articulations à partir des fichiers CSV.
Bouton de Sortie: Fermer l'application.
Onglet Données Graphiques:

Sélecteur d'Articulation: Menu déroulant pour sélectionner une articulation spécifique à visualiser.
Matplotlib Canvas: Zone de traçage pour visualiser les données de l'articulation sélectionnée.
Bouton de Sortie: Fermer l'application.
Contrôle de la Simulation
Démarrer la Simulation: Commence la simulation, mettant à jour les positions des articulations et visualisant les mouvements.
Arrêter la Simulation: Arrête la simulation.
Gestion du Niveau de Batterie: Simule la consommation de batterie et met à jour l'indicateur de batterie.
Détection de Défauts: Surveille les défauts dans la simulation et affiche des messages en cas de détection.
Visualisation
Mouvements des Articulations 3D/2D: Visualise les mouvements des articulations en 3D et 2D.
Centre de Masse (CoM): Calcule et visualise le centre de masse des articulations.
Zoom et Déplacement: Permet de zoomer et de déplacer la visualisation pour une inspection détaillée.
Installation et Configuration
Dépendances: Assurez-vous d'avoir Python 3.x installé avec les packages suivants:
- PyQt5
- Matplotlib
- Pandas
- NumPy
  
Cloner le Dépôt:
bash
Copier le code
git clone https://github.com/RayaneUPEC/GUI-Robotics
cd mujoco-gui
Exécuter l'Application:
bash
Copier le code
python main.py
Structure des Fichiers
main.py: Point d'entrée principal pour l'application.
img/: Répertoire contenant les images utilisées dans l'interface.
css/: Répertoire contenant les styles CSS pour l'interface.
Améliorations Futures# GUI-Robotics
