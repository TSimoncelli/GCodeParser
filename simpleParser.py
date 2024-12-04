
# TODO :
# 


import re 
import utils.utils

#---------------------------VARIABLES---------------------------#

inFolder = "inputs"
outFile = "outputs\\commandesRobot.txt"
repere = "/RPlateau"

#---------------------------FONCTIONS---------------------------#

def extraire_donnees_fichier(fichier):
    ''' Parcourt le fichier donne et recupere les valeurs des positions X,Y,Z et celle de l'extrudeur E
    Commandes traitees : G0,G1,G28
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z], elements = None si pas de deplacement dans une direction'''

    donnees = []
    lastPos = [0,0,0,0] #liste pour sauvegarder les dernieres positions sur chaque axe
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # Traduit la commande G28 = "home all axis" en une position [0,0,0]
            if ligne.startswith('G28'):
                donnees.append([0.0,0.0,0.0,lastPos[3]])
            # Verifier si la ligne commence par G1 ou G0 = "linear move"
            elif ligne.startswith(('G1','G0')):
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
                # Verifie que l'on a au moins une instruction de deplacement differente des precedentes (exclue les commandes Feedrate)
                if not utils.utils.listesIdentiques(valeurs, lastPos):
                    # Ajouter cette ligne de valeurs e la liste de donnees
                    donnees.append(valeurs)
                    lastPos = valeurs

    return donnees


def calculDirectionDepl(donnees):
    '''Creation du vecteur contenant les valeurs de deplacement en X,Y,Z entre 2 positions
    donnees : liste des positions absolues [X,Y,Z]
    return : liste des deplacement relatifs [X,Y,Z] '''

    directions = []
    for i in range (1,len(donnees)):
        # Calcule les deplacements relatifs dans chaque direction (arrondis e 5 digits)
        diffX = round(donnees[i][0] - donnees[i-1][0],5)
        diffY = round(donnees[i][1] - donnees[i-1][1],5)
        diffZ = round(donnees[i][2] - donnees[i-1][2],5)
        diffE = round(donnees[i][3],5)
        directions.append([diffX,diffY,diffZ,diffE])
    return directions

def export_commandes_robot(fichier,vecteurs,repere,vit_lin):
    '''Genere les instructions de deplacement du robot en langage KUKA a partir de la liste des deplacements relatifs
    fichier : chemin vers le fichier .txt dans lequel generer les commandes robot
    vecteurs : liste des vecteurs deplacement [X,Y,Z,E]
    repere : nom du repere pour le deplacement du robot ["/NomRepere"]
    vit_lin : vitesse lineaire lors des translations [mm/s]
    return : None'''

    # Cree une sous liste sans les infos en E (derniere colonne)
    xyzPos = [vect[:4] for vect in vecteurs]
    oldE = 0
    i = 1 #numéro du motionbatch
    j = 1
    resetLigne = 0
    # Ouvrir un fichier en mode ecriture
    with open(fichier, "w") as f:
        #Ajout d'une ligne initiale pour la creation de methode JAVA motionbatch
        f.write("public void mb1(){" + "\n")
        f.write("double blend = 4;" + "\n" )
        f.write("MotionBatch mb191 = new MotionBatch(" + "\n")
        # Parcourir chaque ligne du tableau
        for pos in xyzPos:
            if (pos[3]>0 and oldE==0): #Si E positif, on clos le motionbatch et on active l'extrusion puis on ouvre le motionbatch_suivant
                f.write("\n" + ").setBlendingCart(blend);" + "\n")
                f.write("_lbr.move(mb191);" + "\n")
                f.write("_medflange.setOutputX3Pin2(true);" + "\n")
                f.write("}" + "\n" + "\n")
                i = i + 1
                resetLigne = 0
                f.write("public void mb"+ str(i) + "(){" + "\n")
                f.write("double blend = 4;" + "\n" )
                f.write("MotionBatch mb191 = new MotionBatch(" + "\n")
                oldE = 1
            if (pos[3]<0 and oldE==1): #Si E negatif, on désactive l'extrusion
                f.write("\n" + ").setBlendingCart(blend);" + "\n")
                f.write("_lbr.move(mb191);" + "\n")
                f.write("_medflange.setOutputX3Pin2(false);"+ "\n")
                f.write("}" + "\n" + "\n")
                i = i + 1
                resetLigne = 0
                f.write("public void mb"+ str(i) + "(){" + "\n")
                f.write("double blend = 4;" + "\n" )
                f.write("MotionBatch mb191 = new MotionBatch(" + "\n")
                oldE = 0    # Si c'est un deplacement lineaire en X, Y ou Z
            if ((pos[0]!=0 or pos[1]!=0 or pos[2]!=0) and resetLigne==1):
                # Ecrit la commande robot pour les deplacements donnes dans le fichier 
                f.write("," + "\n" + "linRel(Transformation.ofDeg(" + ",".join(map(str, pos[:3])) + ",0.0,0.0,0.0),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ")") 
            if ((pos[0]!=0 or pos[1]!=0 or pos[2]!=0) and resetLigne==0):
                # Ecrit la commande robot pour les deplacements donnes dans le fichier 
                f.write("linRel(Transformation.ofDeg(" + ",".join(map(str, pos[:3])) + ",0.0,0.0,0.0),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ")") 
                resetLigne = 1
            

        f.write(").setBlendingCart(blend);" + "\n")
        f.write("_lbr.move(mb191);" + "\n")
        f.write("_medflange.setOutputX3Pin2(false);"+ "\n")
        f.write("}" + "\n" + "\n")
        f.write("Appel de methode a mettre dans le run " + "\n")
        while i > 0 :
            f.write("mb"+str(j)+"();"+"\n")
            i = i - 1
            j = j + 1

def choixFichierEntree(liste):
    ''' Fonction qui permet la selection d'un fichier parmi une liste de noms de fichiers dans le terminal
    liste : liste des noms de fichiers parmi lesquels selectionner
    return : fichier selectionne par l'utilisateur'''
    print("\nSelectionnez le fichier a convertir parmi :")
    for f in liste:
        print(f + " ; ")
    try:
        # Tente de convertir en entier la saisie utilisateur
        index = int(input("\nIndex du fichier a selectionner dans la liste (0-"+str(len(liste)-1)+"): "))
    except ValueError:
        print("\nErreur : veuillez entrer un nombre entier valide.")
    return liste[index]

def runConsole(inFolder,outFile,repere):
    ''' Fonction prenant en charge la configuration du parser de g-code via un terminal'''
    print("Convertisseur de G-code en code robot KUKA")
    # Recupere et laisse l'utilisateur selectionner le fichier d'entree de son choix
    listeFichier = utils.utils.getFilesIn(inFolder)
    inFile = inFolder + "\\" + choixFichierEntree(listeFichier)
    print("fichier gcode entree = " + inFile)
    # Affiche les differents parametres du parser de G-Code
    print("fichier commandes robot KUKA sortie = " + outFile)
    print("\ndeplacements robot dans repere = " + repere)
    vitesse = input("Entrez vitesse max. de deplacement [mm/s] :")
    print("Vitesse max. de deplacement = " + vitesse + "mm/s")
    # Effectue la conversion
    output = extraire_donnees_fichier(inFile)
    deplacements = calculDirectionDepl(output)
    export_commandes_robot(outFile,deplacements,repere,vitesse)
    print("\n Conversion terminee, resultat disponible dans " + outFile)


#-----------------------BOUCLE PRINCIPALE-------------------------#

runConsole(inFolder,outFile,repere)
