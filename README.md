# GCodeParser
Ce projet contient un convertisseur d'instructions G-Code en langage robot KUKA

## Utilisation
Conversion d’instructions G-code de déplacement obtenues à partir d’un trancheur en commandes de déplacement relatif du robot KUKA dans un repère spécifique. Ce convertisseur ne prend pas en compte l’orientation de l'outil et n’effectue donc aucune rotation de l’outil depuis sa pose de départ. 
## Configuration
* G-code (Slicer Sli3r ou Cura, Flavor Repetier) fourni en entrée
* Génération de commandes linRel du robot dans un fichier txt en sortie, pour être ensuite copié-collé dans un MotionBatch (dans l’environnement de programmation KUKA Sunrise)
* Le fichier contenant le G-code est placé dans le dossier inputs du projet
* Un fichier commandesRobot.txt existe dans le dossier outputs du projet
## Suppositions
* Que le slicer utilisé a été correctement configuré avec les paramètres souhaités (diamètre de buse, hauteur de ligne, type de remplissage, position de la pièce dans le repère)
* Que le robot est à l'origine du repère plateau avec la buse orientée à la verticale pour démarrer la séquence de commandes
* Que les mouvements à effectuer sont dans le repère plateau
* Les instructions contenues dans le G-code autres que les déplacements en X,Y,Z (extrudeur, angles de l'outil) sont ignorés lors de la génération du fichier de sortie
* Commandes G-code supportées :
* * G0: Rapid move
  * G1: Controlled linear move
  * G28: Home
## Fonctionnement de la conversion
![fonctionnementPasserelleSimpleParser](https://github.com/user-attachments/assets/2dcb8400-b1c9-4f51-b4f0-a564803338fa)
Etapes de conversion du g-code en code robot KUKA

![image](https://github.com/user-attachments/assets/0f4c26b3-537d-4ec1-a1d4-88c75022dda9 )
Exemple de conversion d'un fichier G-code en liste d'instructions pour robot KUKA

## Tutoriel d'utilisation du convertisseur
#### 1) Télécharger le projet en zip ou cloner le projet Github directement dans un IDE
#### 2) Ouvrir le projet dans un IDE permettant d'exécuter du code Python
#### 3) Lancer le programme SimpleParser.py
#### 4) Un écran de terminal s'ouvre et demande de choisir un fichier gcode parmi ceux présents dans le dossier inputs, entrer le chiffre correspondant à l'index du fichier à selectionner dans la liste des fichiers affichés
![image](https://github.com/user-attachments/assets/0c0bb1b4-fef4-4761-b092-e69fc9a791eb)
#### 5) La localisation du fichier gcode d'entrée et du fichier de commandes robot de sortie s'affichent dans la console
#### 6) Entrer la vitesse de déplacement maximum en mm/s pour les déplacements du robot (Vitesse précisée lors de l'exécution d'un déplacement avec la commande linRel en langage robot KUKA)
![image](https://github.com/user-attachments/assets/26becf26-e6f1-4853-9031-d27a5d86f6fb)
#### 7) La conversion s'exécute et le résultat est disponible dans un fichier texte dans le répertoire outputs
![image](https://github.com/user-attachments/assets/910cedaa-f9b5-41f3-9dde-579ea26a14d1)



