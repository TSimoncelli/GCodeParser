import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simpleParser import extraire_donnees_fichier


#Test 1 : l'extraction fonctionne bien comme demandé
file = "inputs\\pyramide1_Cura_FlavorRepetier_RamsaiParameters.gcode"
output = extraire_donnees_fichier(file)
for ligne in output:
    print(ligne)