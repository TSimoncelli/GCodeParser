import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))
from simpleParser import extraire_donnees_fichier
from utils.utils import listesIdentiques


#Test 1 : l'extraction fonctionne bien comme demandé avec le gcode généré par Cura et Slic3r
file = "inputs\\pyramide1_Slic3r_FlavorRepetier_RamsaiParameters.gcode"
output = extraire_donnees_fichier(file)
for ligne in output:
    print(ligne)
    

#Test 2 : méthode de comparaison de listes fonctionne
# liste1 = [0,2,5,4,8]
# liste2 = [0,2,5,4,8]
# liste3 = [0,2,5,0,8]
# print(listesIdentiques(liste1,liste2))
# print(listesIdentiques(liste2,liste3))