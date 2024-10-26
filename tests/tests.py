import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))
from simpleParser import extraire_donnees_fichier, calculDirectionDepl
from utils.utils import listesIdentiques


#Test 1 : Méthode extraire donnees : l'extraction fonctionne bien comme demandé avec le gcode généré par Cura et Slic3r
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

#Test 3 : Méthode calculDirectionDepl : semble fonctionner mais difficile à vérifier juste avec valeurs
# file = "inputs\\pyramide1_Cura_FlavorRepetier_RamsaiParameters.gcode"
# output = extraire_donnees_fichier(file)
# deplacement = calculDirectionDepl(output)

# for ligne in deplacement:
#     print(ligne)

#Test 4 : validation graphique du fonctionnement
def configPlot(vect_deplacement, ax):
    # Récupération des points de trajectoire dans l'espace
    t = np.linspace(0, 5, 1000) #nb de points à afficher
    x = [coord[0] for coord in vect_deplacement]
    y = [coord[1] for coord in vect_deplacement]
    z = [coord[2] for coord in vect_deplacement]

    # Configuration initiale : définir les limites et la ligne vide qui sera mise à jour
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.set_zlim(0, 20)
    line, = ax.plot([], [], [], lw=2)

    # Plateau 200x200 (en noir) dans le plan z=0
    x_rect = [0, 200, 200, 0, 0]  # Sommets du rectangle sur l'axe x
    y_rect = [0, 0, 200, 200, 0]  # Sommets du rectangle sur l'axe y
    z_rect = [0, 0, 0, 0, 0]          # Le rectangle est dans le plan z=0

    ax.plot(x_rect, y_rect, z_rect, color='black')  # Tracer le rectangle

    return line,x,y,z,t

# Fonction pour initialiser l'animation (ici on efface la ligne)
def initPlot(line):
    line.set_data([], [])
    line.set_3d_properties([])
    return line

# Fonction de mise à jour de l'animation : tracer la trajectoire au fur et à mesure
def updatePlot(num,line,x,y,z):
    #Somme les déplacements depuis le début pour obtenir la position actuelle
    x_rel = np.cumsum(x[:num])
    y_rel = np.cumsum(y[:num])
    z_rel = np.cumsum(z[:num])
    line.set_data(x_rel,y_rel)
    line.set_3d_properties(z_rel)
    return line

file = "inputs\\pyramide1_Cura_FlavorRepetier_RamsaiParameters.gcode"
output = extraire_donnees_fichier(file)
deplacement = calculDirectionDepl(output)

# Création de la figure 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Création de l'animation
line,x,y,z,t = configPlot(deplacement,ax)
ani = FuncAnimation(fig, updatePlot, frames=len(t), fargs=(line, x, y, z), init_func=lambda: initPlot(line), blit=False, interval=5)

# Affichage de l'animation
plt.show()

for ligne in deplacement:
    print(ligne)



        