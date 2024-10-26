# TODO :
# modifier traitement du G92 pour ne pas faire de déplacement quand on envoie G92


import re 

#---------------------------VARIABLES---------------------------#



#---------------------------FONCTIONS---------------------------#

def extraire_donnees_fichier(fichier):
    ''' Parcourt le fichier donne et recupere les valeurs des positions X,Y,Z et celle de l'extrudeur E
    Commandes traitees : G0,G1,G28,G92
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z], elements = None si pas de deplacement dans une direction'''

    donnees = []
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # Traduit la commande G28 = "home all axis" en une position [0,0,0]
            if ligne.startswith('G28'):
                donnees.append([0.0,0.0,0.0,None])
            # Vérifier si la ligne commence par G1 ou G0 = "linear move"
            elif ligne.startswith(('G1','G0','G92')):
                # Utiliser une regex pour trouver les valeurs X,Y,Z,E
                x = re.search(r'X([-\d.]+)', ligne)
                y = re.search(r'Y([-\d.]+)', ligne)
                z = re.search(r'Z([-\d.]+)', ligne)
                e = re.search(r'E([-\d.]+)', ligne)

                # Extraire les valeurs et les mettre dans une liste, mettre None si une valeur est manquante
                valeurs = [
                    float(x.group(1)) if x else None,
                    float(y.group(1)) if y else None,
                    float(z.group(1)) if z else None,
                    float(e.group(1)) if e else None
                ]
                # Vérifie que l'on a au moins une instruction de déplacement en X, Y, Z ou E (exclue les commandes Feedrate)
                if any (val is not None for val in valeurs):
                    # Ajouter cette ligne de valeurs à la liste de données
                    donnees.append(valeurs)

    return donnees


def calculDirectionDepl(donnees):
    '''Creation du vecteur contenant les valeurs de deplacement en X,Y,Z entre 2 positions
    donnees : liste des positions absolues [X,Y,Z]
    return : liste des deplacement relatifs [X,Y,Z] '''

    directions = []
    for i in range (1,len(donnees)):
            # Calculer les différences si la ligne contient X ou Y
            if donnees[i][0] is not None and donnees[i][1] is not None:
                # Si pas de position précédente avec X et Y, on remonte en arrière jusqu'à la dernière position connue
                goback=1
                #Tant que l'on a pas trouvé la position précédente
                while donnees[i-goback][0] is None or donnees[i-goback][1] is None: 
                    goback+=1
                # Si on a une position précédente avec X et Y, on calcule la différence (arrondie à 5 décimales)
                diffX = round(donnees[i][0] - donnees[i-goback][0],5)
                diffY = round(donnees[i][1] - donnees[i-goback][1],5)
                directions.append([diffX,diffY,0])
            # Calculer la différence si la ligne contient Z
            if donnees[i][2] is not None:
                goback=1
                while donnees[i-goback][2] is None:
                    goback+=1
                # Si on a une position précédente en Z, on calcule la différence (arrondie à 5 décimales)
                diffZ = round(donnees[i][2] - donnees[i-goback][2],5)
                directions.append([0,0,diffZ])
    return directions

#-----------------------BOUCLE PRINCIPALE-------------------------#