#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################### SCRIPT DESCRIPTION ############################################## ############################################# PRÉSENTATION DU SCRIPT ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This script starts a single player match using a random maze                                                #    Ce script démarre une partie à 1 joueur sur un labyrinthe aléatoire                                         #
#    Command line: python SinglePlayersGame.py <playerFileName>                                                  #    Ligne de commande : python SinglePlayersGame.py <playerFileName>                                            #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    <playerFileName> : string                                                                                   #    <playerFileName> : string                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Path to the player's AI file                                                                            #        Chemin vers le fichier d'AI pour le joueur                                                              #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# Imports
from LaunchersLibrary import *

# Command line verification
if len(sys.argv) != 2 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <playerFileName>)")
    exit()
PLAYER_FILE_NAME = sys.argv[1]

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
#    MAZE_DENSITY : float                                                                                        #    MAZE_DENSITY : float                                                                                        #
#    --------------------                                                                                        #    --------------------                                                                                        #
#                                                                                                                #                                                                                                                #
#        Density of walls in the maze                                                                            #        Densité de murs dans le labyrinthe                                                                      #
#        This is a float in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible              #        C'est un réel dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible     #
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
###################################################################################################################################################################################################################################

# Maze configuration
MAZE_WIDTH = 10
MAZE_HEIGHT = 10
MAZE_DENSITY = 0.7
MUD_PROBABILITY = 0.0
MAZE_SYMMETRIC = False
NB_PIECES_OF_CHEESE = 1

# Time configuration
PREPROCESSING_TIME = 3.0
TURN_TIME = 0.1
TIMEOUT = None

# Other useful constants
GAME_MODE = "normal"
OUTPUT_DIRECTORY = "./out/previousGame/"

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# We start the game
result = startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, MAZE_DENSITY, MUD_PROBABILITY, MAZE_SYMMETRIC, NB_PIECES_OF_CHEESE, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_FILE_NAME)

# We print the summary of the game
print(repr(result))

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################
