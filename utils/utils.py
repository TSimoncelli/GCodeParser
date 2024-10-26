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
