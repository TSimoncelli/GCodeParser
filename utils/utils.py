import os

def listesIdentiques(liste1,liste2):
    ''' Fonction de comparaison de listes de nombre reels ou entiers
    liste 1 : 1ere liste a verifier
    liste 2 : 2eme liste a verifier
    return : false si les 2 listes ont au moins une case differente
    return : true si les 2 listes contiennent les memes elements '''
    identique = True
    for i in range(0,len(liste1)):
        if(liste1[i]!=liste2[i]):
            identique = False
            break
    return identique 

def getFilesIn(dossier):
    ''' Fonction renvoyant la liste des fichiers presents dans un dossier
    dossier : chemin relatif vers le dossier dans lequel regarder
    return : liste des noms de fichiers trouves '''
    # Lister les fichiers et dossiers
    contenu = os.listdir(dossier)
    # Filtrer uniquement les fichiers
    fichiers = [f for f in contenu if os.path.isfile(os.path.join(dossier, f))]
    return fichiers
