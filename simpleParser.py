# TODO :
# modifier traitement du G92 pour ne pas faire de déplacement quand on envoie G92


import re 
import utils.utils

#---------------------------VARIABLES---------------------------#



#---------------------------FONCTIONS---------------------------#

def extraire_donnees_fichier(fichier):
    ''' Parcourt le fichier donne et recupere les valeurs des positions X,Y,Z et celle de l'extrudeur E
    Commandes traitees : G0,G1,G28,G92
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z], elements = None si pas de deplacement dans une direction'''

    donnees = []
    lastPos = [0,0,0,0] #liste pour sauvegarder les dernières positions sur chaque axe
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # Traduit la commande G28 = "home all axis" en une position [0,0,0]
            if ligne.startswith('G28'):
                donnees.append([0.0,0.0,0.0,lastPos[3]])
            # Vérifier si la ligne commence par G1 ou G0 = "linear move"
            elif ligne.startswith(('G1','G0','G92')):
                # Utiliser une regex pour trouver les valeurs X,Y,Z,E
                x = re.search(r'X([-\d.]+)', ligne)
                y = re.search(r'Y([-\d.]+)', ligne)
                z = re.search(r'Z([-\d.]+)', ligne)
                e = re.search(r'E([-\d.]+)', ligne)

                # Extraire les valeurs et les mettre dans une liste, mettre None si une valeur est manquante
                valeurs = [
                    float(x.group(1)) if x else lastPos[0],
                    float(y.group(1)) if y else lastPos[1],
                    float(z.group(1)) if z else lastPos[2],
                    float(e.group(1)) if e else lastPos[3]
                ]
                # Vérifie que l'on a au moins une instruction de déplacement différente des précédentes (exclue les commandes Feedrate)
                if not utils.utils.listesIdentiques(valeurs, lastPos):
                    # Ajouter cette ligne de valeurs à la liste de données
                    donnees.append(valeurs)
                    lastPos = valeurs

    return donnees


def calculDirectionDepl(donnees):
    '''Creation du vecteur contenant les valeurs de deplacement en X,Y,Z entre 2 positions
    donnees : liste des positions absolues [X,Y,Z]
    return : liste des deplacement relatifs [X,Y,Z] '''

    directions = []
    for i in range (1,len(donnees)):
        # Calcule les déplacements relatifs dans chaque direction (arrondis à 5 digits)
        diffX = round(donnees[i][0] - donnees[i-1][0],5)
        diffY = round(donnees[i][1] - donnees[i-1][1],5)
        diffZ = round(donnees[i][2] - donnees[i-1][2],5)
        diffE = round(donnees[i][3] - donnees[i-1][3],5)
        directions.append([diffX,diffY,diffZ,diffE])
    return directions

#-----------------------BOUCLE PRINCIPALE-------------------------#