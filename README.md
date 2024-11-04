# GCodeParser
Ce projet contient un convertisseur d'instructions G-Code en langage robot KUKA

## Utilisation
Conversion d’instructions G-code de déplacement obtenues à partir d’un trancheur en commandes de déplacement relatif du robot KUKA dans un repère spécifique. Ce convertisseur ne prend pas en compte l’orientation de la buse et n’effectue donc aucune rotation de l’outil depuis sa pose de départ. 
## Configuration
* G-code (Slicer Sli3r ou Cura, Flavor Repetier) fourni en entrée
* Génération de commandes linRel du robot dans un fichier txt en sortie, pour être ensuite copié-collé dans un MotionBatch (dans l’environnement de programmation KUKA Sunrise)
* Le fichier contenant le G-code est placé dans le dossier inputs du projet
* Un fichier commandesRobot.txt existe dans le dossier outputs du projet
## Suppositions : 
* Que le slicer utilisé a été correctement configuré avec les paramètres souhaités (diamètre de buse, hauteur de ligne, type de remplissage, position de la pièce dans le repère)
* Que le robot est à l'origine du repère plateau avec la buse orientée à la verticale pour démarrer la séquence de commandes
* Que les instructions de déplacement sont envoyées avec G0, G1 ou G28 dans le G-code
* Que les mouvements à effectuer sont dans le repère plateau
* Les instructions contenues dans le G-code autres que les déplacements en X,Y,Z sont ignorés lors de la génération du fichier de sortie

![image](https://github.com/user-attachments/assets/0f4c26b3-537d-4ec1-a1d4-88c75022dda9)
Exemple de conversion d'un fichier G-code en liste d'instructions pour robot KUKA
