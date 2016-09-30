#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################### SCRIPT DESCRIPTION ############################################## ############################################# PRÉSENTATION DU SCRIPT ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This script starts a game using files that were previously exported in the given directory                  #    Ce script démarre une partie à 2 joueurs sur un labyrinthe aléatoire                                        #
#    Command line: python LoadSavedGame.py <gameDirectory>                                                       #    Ligne de commande : python LoadSavedGame.py <gameDirectory>                                                 #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    <gameDirectory> : string                                                                                    #    <gameDirectory> : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game to load is saved                                                   #        Chemin vers le répertoire où la partie à charger est sauvegardée                                        #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# Imports
from LaunchersLibrary import *
import os

# Command line verification
if len(sys.argv) != 2 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <gameDirectory>)")
    exit()
GAME_DIRECTORY = sys.argv[1]
MAZE_FILE_NAME = GAME_DIRECTORY + "/maze.txt"
PLAYER_1_FILE_NAME = GAME_DIRECTORY + "/player1.py"
PLAYER_2_FILE_NAME = GAME_DIRECTORY + "/player2.py"
TWO_PLAYERS = os.path.isfile(PLAYER_2_FILE_NAME)

###################################################################################################################################################################################################################################
################################################### CONSTANTS ################################################### ################################################### CONSTANTES ##################################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Useful constants for the script                                                                             #    Constantes utiles pour le script                                                                            #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
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

# Time configuration
PREPROCESSING_TIME = 0.0
TURN_TIME = None
TIMEOUT = None

# Other useful constants
GAME_MODE = "normal"
OUTPUT_DIRECTORY = "./out/previousGame/"

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# We start the game
if (TWO_PLAYERS) :
    result = startCustomGame(MAZE_FILE_NAME, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_1_FILE_NAME, PLAYER_2_FILE_NAME)
else :
    result = startCustomGame(MAZE_FILE_NAME, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_1_FILE_NAME)

# We print the summary of the game
print(repr(result))

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################