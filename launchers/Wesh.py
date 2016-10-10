#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################### SCRIPT DESCRIPTION ############################################## ############################################# PRÉSENTATION DU SCRIPT ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This script studies the mean number of moves required to get a piece of cheese as a function of density     #    Ce script étudie le nombre moyen de mouvements pour avoir un morceau de fromage en fonction de la densité   #
#    Here, we study a 15x15 maze with no mud and a single piece of cheese in its center                          #    Ici, on étudie un labyrinthe sans boue de taille 15x15 avec un unique morceau de fromage en son centre      #
#    The tests are performed for each file given in the command line arguments                                   #    Les tests sont effectués pour chaque fichier dans les arguments de la ligne de commande                     #
#    Command line: python ExampleStatistics.py <playerFileName>+                                                 #    Ligne de commande : python ExampleStatistics.py <playerFileName>+                                           #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    <playerFileName> : string                                                                                   #    <playerFileName> : string                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Path to the player's AI file                                                                            #        Chemin vers le fichier d'AI pour le joueur                                                              #
#        These files must be derivated from the Template.py file                                                 #        Ces fichiers doiventt être des dérivés du fichier Template.py                                           #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# Imports
from LaunchersLibrary import *
import matplotlib.pyplot as plt

# Command line verification
if len(sys.argv) < 2 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <playerFileName>+)")
    exit()
PLAYERS_FILE_NAMES = sys.argv[1:]

###################################################################################################################################################################################################################################
################################################### CONSTANTS ################################################### ################################################### CONSTANTES ##################################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Useful constants for the script                                                                             #    Constantes utiles pour le script                                                                            #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    MAZE_WIDTH : int    MAZE_HEIGHT : int                                                                       #    MAZE_WIDTH : int    MAZE_HEIGHT : int                                                                       #
#    ----------------    -----------------                                                                       #    ----------------    -----------------                                                                       #
#                                                                                                                #                                                                                                                #
#        Dimensions of the maze in number of cells                                                               #        Dimensions du labyrinthe en nombre de cases                                                             #
#        Both dimensions must be greater than one                                                                #        Les deux dimensions doivent être supérieures à 1                                                        #
#                                                                                                                #                                                                                                                #
#    MAZE_DENSITIES : float list                                                                                 #    MAZE_DENSITIES : float list                                                                                 #
#    ---------------------------                                                                                 #    ---------------------------                                                                                 #
#                                                                                                                #                                                                                                                #
#        Densities of walls in the maze to study                                                                 #        Densités de murs dans le labyrinthe à tester                                                            #
#        These are floats in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible             #        Ce sont des réels dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible #
#        The maze will be connected, whatever its density                                                        #        Quelle que soit la densité, le labyrinthe restera connexe                                               #
#                                                                                                                #                                                                                                                #
#    MUD_PROBABILITY : float                                                                                     #    MUD_PROBABILITY : float                                                                                     #
#    -----------------------                                                                                     #    -----------------------                                                                                     #
#                                                                                                                #                                                                                                                #
#        Probability that a path between two cells is covered in mud, thus taking more time to cross             #        Probabilité qu'un chemin entre deux cases soit couvert de boue, prenant donc plus de temps à passer     #
#        This is a float in [0, 1]                                                                               #        C'est un réel dans [0, 1]                                                                               #
#                                                                                                                #                                                                                                                #
#    MAZE_SYMMETRIC : bool                                                                                       #    MAZE_SYMMETRIC : bool                                                                                       #
#    ---------------------                                                                                       #    ---------------------                                                                                       #
#                                                                                                                #                                                                                                                #
#        If set to True, the maze will be symetric                                                               #        Si mis à True, le labyrinthe sera symétrique                                                            #
#        In that case, the pieces of cheese will also be symletrically placed                                    #        Dans ce cas, les morceaux de fromage seront aussi placés symétriquement                                 #
#                                                                                                                #                                                                                                                #
#    NB_PIECES_OF_CHEESE : int                                                                                   #    NB_PIECES_OF_CHEESE : int                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Number of pieces of cheese in the maze                                                                  #        Nombre de morceaux de fromage dans le labyrinthe                                                        #
#        This number must be lower than MAZE_WIDTH * MAZE_HEIGHT - X, with X the number of players               #        Ce nombre doit être inférieur à MAZE_WIDTH * MAZE_HEIGHT - X, avec X le nombre de joueurs               #
#        If the maze has an even number of cells and is symmetric, then NB_PIECES_OF_CHEESE must be odd          #        Si le labyrinthe a un nombre pair de cases et est symétrique, NB_PIECES_OF_CHEESE doit être pair        #
#                                                                                                                #                                                                                                                #
#    PREPROCESSING_TIME : float                                                                                  #    PREPROCESSING_TIME : float                                                                                  #
#    --------------------------                                                                                  #    --------------------------                                                                                  #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "preprocessing" function in the AI script                            #        Nombre de secondes allouées à la fonction "preprocessing" dans le script d'AI                           #
#                                                                                                                #                                                                                                                #
#    TURN_TIME : float                                                                                           #    TURN_TIME : float                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "turn" function in the AI script                                     #        Nombre de secondes allouées à la fonction "turn" dans le script d'AI                                    #
#        If this constant set to None, the game becomes synhronous                                               #        Si cette constante est mise à None, le jeu est synchrone                                                #
#                                                                                                                #                                                                                                                #
#    TIMEOUT : float                                                                                             #    TIMEOUT : float                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Time after which we stop the game anyway                                                                #        Temps après lequel la partie est arrêtée quoi qu'il arrive                                              #
#        Set this constant to None to disable the timeout                                                        #        Mettez cette constante à None pour désactiver le timeout                                                #
#                                                                                                                #                                                                                                                #
#    GAME_MODE : string                                                                                          #    GAME_MODE : string                                                                                          #
#    ------------------                                                                                          #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
#    OUTPUT_DIRECTORY : string                                                                                   #    OUTPUT_DIRECTORY : string                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Every game that finishes is exported to this directory, erasing any other previous game there           #        Toute partie qui se termine est exportée dans ce dossier, en écrasant toute partie s'y trouvant         #
#        Saved games can be played again using script LoadSavedGame.py                                           #        Les parties sauvegardées peuvent être rejouées en utilisant le script LoadSavecGame.py                  #
#                                                                                                                #                                                                                                                #
#    NB_TESTS : int                                                                                              #    NB_TESTS : int                                                                                              #
#    --------------                                                                                              #    --------------                                                                                              #
#                                                                                                                #                                                                                                                #
#        Number of tests to perform per density value                                                            #        Nombre de tests à effectuer par valeur de densité étudiée                                               #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# Maze configuration
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
MAZE_DENSITY = 0.7
MUD_PROBABILITY = 0.15
MAZE_SYMMETRIC = True
NB_PIECES_OF_CHEESE = [k for k in range(1,10)]

# Time configuration
PREPROCESSING_TIME = 0.0
TURN_TIME = None
TIMEOUT = None

# Other useful constants
GAME_MODE = "test"
OUTPUT_DIRECTORY = "./out/previousGame/"
NB_TESTS = 100

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# For every density value, we count the mean number of moves needed to finish the game
meanMovesPerNumber = {fileName:[] for fileName in PLAYERS_FILE_NAMES}
for cheese in NB_PIECES_OF_CHEESE :
    for fileName in PLAYERS_FILE_NAMES :
        meanMoves = 0.0
        for test in range(NB_TESTS) :
            print(fileName + " -- Pieces Of Cheese " + str(cheese)[:3] + " -- Test " + str(test + 1) + "/" + str(NB_TESTS))
            result = startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, MAZE_DENSITY, MUD_PROBABILITY, MAZE_SYMMETRIC, cheese, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, fileName)
            meanMoves += result["player1"]["totalNbMoves"] / NB_TESTS
        meanMovesPerNumber[fileName].append(meanMoves)

# We plot the result
for fileName in PLAYERS_FILE_NAMES :
    plt.plot(NB_PIECES_OF_CHEESE, meanMovesPerNumber[fileName])
plt.xlabel("Cheese Quantity")
plt.ylabel("Mean number of moves")
plt.legend(PLAYERS_FILE_NAMES)
plt.show()

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################
