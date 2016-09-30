#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################### LIBRARY DESCRIPTION ############################################# ######################################## PRÉSENTATION DE LA BIBLIOTHÈQUE ########################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This library contains every function that can be used to manipulate the various PyRat programs              #    Cette bibliothèque contient toutes les fonctions utiles pour manipuler les programmes PyRat                 #
#    Unless you know what you are doing, please do not edit anything in this file                                #    À moins de savoir ce que vous faites, merci de ne rien éditer dans ce fichier                               #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# Imports
import ast
import os
import random
import selenium.webdriver
import signal
import subprocess
import sys
import threading
import time

###################################################################################################################################################################################################################################
################################################### CONSTANTS ################################################### ################################################### CONSTANTES ##################################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Useful constants                                                                                            #    Constantes utiles                                                                                           #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    GUI_IP : string    GUI_PORT : int                                                                           #    GUI_IP : string    GUI_PORT : int                                                                           #
#    ---------------    --------------                                                                           #    ---------------    --------------                                                                           #
#                                                                                                                #                                                                                                                #
#        Connection information for the GUI to work properly                                                     #        Informations de connexion pour que l'interface graphique fonctionne correctement                        #
#        The port must be a valid integer in [1024, 65535]                                                       #        Le port doit être un entier valide dans [1024, 65535]                                                   #
#        The IP address must correspond to where the GUI program runs                                            #        L'adresse IP doit correspondre à là où l'interface graphique tourne                                     #
#                                                                                                                #                                                                                                                #
#    PLAYER_1_IP : string    PLAYER_1_PORT : int                                                                 #    PLAYER_1_IP : string    PLAYER_1_PORT : int                                                                 #
#    --------------------    -------------------                                                                 #    --------------------    -------------------                                                                 #
#                                                                                                                #                                                                                                                #
#        Connection information for the first player's program to work properly                                  #        Informations de connexion pour que le premier joueur fonctionne correctement                            #
#        The port must be a valid PyRat program port                                                             #        Le port doit être un port d'application PyRat valide                                                    #
#        The server IP address must correspond to where the PyRat core runs                                      #        L'adresse IP doit correspondre à là où le noyau PyRat tourne                                            #
#                                                                                                                #                                                                                                                #
#    PLAYER_2_IP : string    PLAYER_2_PORT : int                                                                 #    PLAYER_2_IP : string    PLAYER_2_PORT : int                                                                 #
#    --------------------    -------------------                                                                 #    --------------------    -------------------                                                                 #
#                                                                                                                #                                                                                                                #
#        Connection information for the second player's program to work properly                                 #        Informations de connexion pour que le second joueur fonctionne correctement                             #
#        The port must be a valid PyRat program port                                                             #        Le port doit être un port d'application PyRat valide                                                    #
#        The server IP address must correspond to where the PyRat core runs                                      #        L'adresse IP doit correspondre à là où le noyau PyRat tourne                                            #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

# GUI configuration
GUI_IP = "127.0.0.1"
GUI_PORT = 12345

# First player configuration
PLAYER_1_IP = "127.0.0.1"
PLAYER_1_PORT = 23456

# Second player configuration
PLAYER_2_IP = "127.0.0.1"
PLAYER_2_PORT = 34567

###################################################################################################################################################################################################################################
########################################### START RANDOM CORE FUNCTION ########################################## ################################### FONCTION DE DÉMARRAGE D'UN NOYAU ALÉATOIRE ##################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat core program with a random maze                                                            #    Démarre le noyau PyRat avec un labyrinthe aléatoire                                                         #
#    Unless you know what you are doing, do not call this function                                               #    A moins de savoir ce que vous faites, n'appelez pas cette fonction                                          #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeWidth : int    mazeHeight : int                                                                         #    mazeWidth : int    mazeHeight : int                                                                         #
#    ---------------    ----------------                                                                         #    ---------------    ----------------                                                                         #
#                                                                                                                #                                                                                                                #
#        Dimensions of the maze in number of cells                                                               #        Dimensions du labyrinthe en nombre de cases                                                             #
#        Both dimensions must be greater than one                                                                #        Les deux dimensions doivent être supérieures à 1                                                        #
#                                                                                                                #                                                                                                                #
#    mazeDensity : float                                                                                         #    mazeDensity : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Density of walls in the maze                                                                            #        Densité de murs dans le labyrinthe                                                                      #
#        This is a float in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible              #        C'est un réel dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible     #
#        The maze will be connected, whatever its density                                                        #        Quelle que soit la densité, le labyrinthe restera connexe                                               #
#                                                                                                                #                                                                                                                #
#    mudProbability : float                                                                                      #    mudProbability : float                                                                                      #
#    ----------------------                                                                                      #    ----------------------                                                                                      #
#                                                                                                                #                                                                                                                #
#        Probability that a path between two cells is covered in mud, thus taking more time to cross             #        Probabilité qu'un chemin entre deux cases soit couvert de boue, prenant donc plus de temps à passer     #
#        This is a float in [0, 1]                                                                               #        C'est un réel dans [0, 1]                                                                               #
#                                                                                                                #                                                                                                                #
#    mazeSymmetric : bool                                                                                        #    mazeSymmetric : bool                                                                                        #
#    --------------------                                                                                        #    --------------------                                                                                        #
#                                                                                                                #                                                                                                                #
#        If set to True, the maze will be symetric                                                               #        Si mis à True, le labyrinthe sera symétrique                                                            #
#        In that case, the pieces of cheese will also be symletrically placed                                    #        Dans ce cas, les morceaux de fromage seront aussi placés symétriquement                                 #
#                                                                                                                #                                                                                                                #
#    nbPiecesOfCheese : int                                                                                      #    nbPiecesOfCheese : int                                                                                      #
#    ----------------------                                                                                      #    ----------------------                                                                                      #
#                                                                                                                #                                                                                                                #
#        Number of pieces of cheese in the maze                                                                  #        Nombre de morceaux de fromage dans le labyrinthe                                                        #
#        This number must be lower than mazeWidth * mazeHeight - x, with x the number of players                 #        Ce nombre doit être inférieur à mazeWidth * mazeHeight - x, avec x le nombre de joueurs                 #
#        If the maze has an even number of cells and is symmetric, then nbPiecesOfCheese must be odd             #        Si le labyrinthe a un nombre pair de cases et est symétrique, nbPiecesOfCheese doit être pair           #
#                                                                                                                #                                                                                                                #
#    preprocessingTime : float                                                                                   #    preprocessingTime : float                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "preprocessing" function in the AI script                            #        Nombre de secondes allouées à la fonction "preprocessing" dans le script d'AI                           #
#                                                                                                                #                                                                                                                #
#    turnTime : float                                                                                            #    turnTime : float                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "turn" function in the AI script                                     #        Nombre de secondes allouées à la fonction "turn" dans le script d'AI                                    #
#        If this parameter set to None, the game becomes synhronous                                              #        Si ce paramètre est mis à None, le jeu est synchrone                                                    #
#                                                                                                                #                                                                                                                #
#    gameMode : string                                                                                           #    gameMode : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
#    twoPlayers : bool                                                                                           #    twoPlayers : bool                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Indicates the number of players in the game                                                             #        Indique le nombre de joueurs dans la partie                                                             #
#                                                                                                                #                                                                                                                #
#    outputDirectory : string                                                                                    #    outputDirectory : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game result is exported                                                 #        Chemin vers le réportoire où le résultat de la partie est exporté                                       #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns two functions: "stop" and "poll"                                                      #    Cette fonction renvoie deux fonctions : "stop" et "poll"                                                    #
#    The "stop" function stops the program when called                                                           #    La fonction "stop" arrête le programme quand elle est appelée                                               #
#    The "poll" function returns None if the program is running, 0 if it exited correctly, or the error code     #    La fonction "poll" renvoie None si le programme tourne, 0 s'il a terminé correctement, ou le code d'erreur  #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startRandomCore (mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, preprocessingTime, turnTime, gameMode, twoPlayers, outputDirectory) :
    
    # Core command line
    commandLine = ["pyrat_core",
                   "-ip1", str(PLAYER_1_IP),
                   "-port1", str(PLAYER_1_PORT),
                   "-mazeWidth", str(mazeWidth),
                   "-mazeHeight", str(mazeHeight),
                   "-mazeDensity", str(mazeDensity),
                   "-mudProbability", str(mudProbability),
                   "-mazeSymmetric", str(mazeSymmetric),
                   "-outputDirectory", str(outputDirectory),
                   "-nbPiecesOfCheese", str(nbPiecesOfCheese),
                   "-closeAtEnd", str(gameMode != "normal"),
                   "-preprocessingTime", str(preprocessingTime)]
    
    # Additional argument if the game is asynchronous
    if turnTime != None :
        commandLine += ["-turnTime", str(turnTime)]
    
    # Additional arguments if the GUI is shown
    if gameMode != "test" :
        commandLine += ["-ipGUI", str(GUI_IP),
                        "-portGUI", str(GUI_PORT)]
    
    # Additional arguments if there are two players
    if twoPlayers :
        commandLine += ["-ip2", str(PLAYER_2_IP),
                        "-port2", str(PLAYER_2_PORT)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

###################################################################################################################################################################################################################################
########################################### START CUSTOM CORE FUNCTION ########################################## ################################# FONCTION DE DÉMARRAGE D'UN NOYAU PERSONNALISÉ #################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat core program from a file                                                                   #    Démarre le noyau PyRat à partir d'un fichier                                                                #
#    Unless you know what you are doing, do not call this function                                               #    A moins de savoir ce que vous faites, n'appelez pas cette fonction                                          #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeFileName : string                                                                                       #    mazeFileName : string                                                                                       #
#    ---------------------                                                                                       #    ---------------------                                                                                       #
#                                                                                                                #                                                                                                                #
#        Path to the maze file                                                                                   #        Chemin vers le fichier du labyrinthe                                                                    #
#                                                                                                                #                                                                                                                #
#    preprocessingTime : float                                                                                   #    preprocessingTime : float                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "preprocessing" function in the AI script                            #        Nombre de secondes allouées à la fonction "preprocessing" dans le script d'AI                           #
#                                                                                                                #                                                                                                                #
#    turnTime : float                                                                                            #    turnTime : float                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "turn" function in the AI script                                     #        Nombre de secondes allouées à la fonction "turn" dans le script d'AI                                    #
#        If this parameter set to None, the game becomes synhronous                                              #        Si ce paramètre est mis à None, le jeu est synchrone                                                    #
#                                                                                                                #                                                                                                                #
#    gameMode : string                                                                                           #    gameMode : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
#    twoPlayers : bool                                                                                           #    twoPlayers : bool                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Indicates the number of players in the game                                                             #        Indique le nombre de joueurs dans la partie                                                             #
#                                                                                                                #                                                                                                                #
#    outputDirectory : string                                                                                    #    outputDirectory : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game result is exported                                                 #        Chemin vers le réportoire où le résultat de la partie est exporté                                       #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns two functions: "stop" and "poll"                                                      #    Cette fonction renvoie deux fonctions : "stop" et "poll"                                                    #
#    The "stop" function stops the program when called                                                           #    La fonction "stop" arrête le programme quand elle est appelée                                               #
#    The "poll" function returns None if the program is running, 0 if it exited correctly, or the error code     #    La fonction "poll" renvoie None si le programme tourne, 0 s'il a terminé correctement, ou le code d'erreur  #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startCustomCore (mazeFileName, preprocessingTime, turnTime, gameMode, twoPlayers, outputDirectory) :
    
    # Core command line
    commandLine = ["pyrat_core",
                   "-ip1", str(PLAYER_1_IP),
                   "-port1", str(PLAYER_1_PORT),
                   "-mazeFileName", str(mazeFileName),
                   "-outputDirectory", str(outputDirectory),
                   "-closeAtEnd", str(gameMode != "normal"),
                   "-preprocessingTime", str(preprocessingTime)]
    
    # Additional argument if the game is asynchronous
    if turnTime != None :
        commandLine += ["-turnTime", str(turnTime)]
    
    # Additional arguments if the GUI is shown
    if gameMode != "test" :
        commandLine += ["-ipGUI", str(GUI_IP),
                        "-portGUI", str(GUI_PORT)]
    
    # Additional arguments if there are two players
    if twoPlayers :
        commandLine += ["-ip2", str(PLAYER_2_IP),
                        "-port2", str(PLAYER_2_PORT)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

###################################################################################################################################################################################################################################
############################################### START GUI FUNCTION ############################################## ################################# FONCTION DE DÉMARRAGE DE L'INTERFACE GRAPHIQUE ################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat GUI program                                                                                #    Démarre l'interface graphique PyRat                                                                         #
#    Unless you know what you are doing, do not call this function                                               #    A moins de savoir ce que vous faites, n'appelez pas cette fonction                                          #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns two functions: "stop" and "poll"                                                      #    Cette fonction renvoie deux fonctions : "stop" et "poll"                                                    #
#    The "stop" function stops the program when called                                                           #    La fonction "stop" arrête le programme quand elle est appelée                                               #
#    The "poll" function returns None if the program is running, 0 if it exited correctly, or the error code     #    La fonction "poll" renvoie None si le programme tourne, 0 s'il a terminé correctement, ou le code d'erreur  #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startGUI () :
    
    # GUI web server address and arguments
    address = "http://" + str(GUI_IP) + "/index.php" \
            + "?address=" + str(GUI_IP) \
            + "&port=" + str(GUI_PORT)
    
    # We start a browser at this address
    try :
        browser = selenium.webdriver.Firefox()
        browser.maximize_window()
        browser.get(address)
    except :
        pass
    
    # Function to stop the program
    def stop () :
        try :
            browser.close()
        except :
            pass
    
    # function to poll the program
    def poll () :
        try :
            browser.find_element_by_id("pyrat")
            return None
        except :
            return 0
            
    # We return the stop and poll functions
    return (stop, poll)

###################################################################################################################################################################################################################################
############################################# START PLAYER FUNCTION ############################################# ####################################### FONCTION DE DÉMARRAGE D'UN JOUEUR #######################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat player manager                                                                             #    Démarre le gestionnaire de joueur PyRat                                                                     #
#    Unless you know what you are doing, do not call this function                                               #    A moins de savoir ce que vous faites, n'appelez pas cette fonction                                          #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    number : int                                                                                                #    number : int                                                                                                #
#    ------------                                                                                                #    ------------                                                                                                #
#                                                                                                                #                                                                                                                #
#        Number of the player for which we start a program                                                       #        Numéro du joueur pour lequel on démarre un programme                                                    #
#        Must be either 1 or 2                                                                                   #        Doit être 1 ou 2                                                                                        #
#                                                                                                                #                                                                                                                #
#    fileName : string                                                                                           #    fileName : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Path to the player's AI file                                                                            #        Chemin vers le fichier d'AI pour le joueur                                                              #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                #                                                                                                                #
#    gameMode : string                                                                                           #    gameMode : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns two functions: "stop" and "poll"                                                      #    Cette fonction renvoie deux fonctions : "stop" et "poll"                                                    #
#    The "stop" function stops the program when called                                                           #    La fonction "stop" arrête le programme quand elle est appelée                                               #
#    The "poll" function returns None if the program is running, 0 if it exited correctly, or the error code     #    La fonction "poll" renvoie None si le programme tourne, 0 s'il a terminé correctement, ou le code d'erreur  #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startPlayer (number, fileName, gameMode) :

    # Player manager command line
    commandLine = ["pyrat_client",
                   "-fileName", str(fileName),
                   "-ip", str(PLAYER_1_IP if number == 1 else PLAYER_2_IP),
                   "-port", str(PLAYER_1_PORT if number == 1 else PLAYER_2_PORT),
                   "-closeAtEnd", str(gameMode != "normal"),
                   "-number", str(number)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

###################################################################################################################################################################################################################################
############################################## START GAME FUNCTION ############################################## ####################################### FONCTION DE DÉMARRAGE D'UNE PARTIE ######################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts a game with the given elements                                                                       #    Démarre une partie avec les éléments donnés                                                                 #
#    Unless you know what you are doing, do not call this function                                               #    A moins de savoir ce que vous faites, n'appelez pas cette fonction                                          #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    coreFunctions : pair(function, function)                                                                    #    coreFunctions : pair(function, function)                                                                    #
#    ----------------------------------------                                                                    #    ----------------------------------------                                                                    #
#                                                                                                                #                                                                                                                #
#        Functions "stop" and "poll" for the core as returned by one of the functions above                      #        Fonctions "stop" et "poll" pour le noyau telles que renvoyées par une des fonctions ci-dessus           #
#                                                                                                                #                                                                                                                #
#    guiFunctions : pair(function, function)                                                                     #    guiFunctions : pair(function, function)                                                                     #
#    ---------------------------------------                                                                     #    ---------------------------------------                                                                     #
#                                                                                                                #                                                                                                                #
#        Functions "stop" and "poll" for the GUI as returned by the function above                               #        Fonctions "stop" et "poll" pour l'interface graphique telles que renvoyées par la fonction ci-dessus    #
#                                                                                                                #                                                                                                                #
#    player1Functions : pair(function, function)                                                                 #    player1Functions : pair(function, function)                                                                 #
#    -------------------------------------------                                                                 #    -------------------------------------------                                                                 #
#                                                                                                                #                                                                                                                #
#        Functions "stop" and "poll" for the first player as returned by the function above                      #        Fonctions "stop" et "poll" pour le premier joueur telles que renvoyées par la fonction ci-dessus        #
#                                                                                                                #                                                                                                                #
#    player2Functions : pair(function, function)                                                                 #    player2Functions : pair(function, function)                                                                 #
#    -------------------------------------------                                                                 #    -------------------------------------------                                                                 #
#                                                                                                                #                                                                                                                #
#        Functions "stop" and "poll" for the second player as returned by the function above                     #        Fonctions "stop" et "poll" pour le second joueur telles que renvoyées par la fonction ci-dessus         #
#                                                                                                                #                                                                                                                #
#    outputDirectory : string                                                                                    #    outputDirectory : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game result is exported                                                 #        Chemin vers le réportoire où le résultat de la partie est exporté                                       #
#                                                                                                                #                                                                                                                #
#    timeout : float                                                                                             #    timeout : float                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Time after which we stop the game anyway                                                                #        Temps après lequel la partie est arrêtée quoi qu'il arrive                                              #
#        Set this parameter to None to disable the timeout                                                       #        Mettez ce paramètre à None pour désactiver le timeout                                                   #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns the contents of the file that is exported after the game is over                      #    Cette fonction renvoie le contenu du fichiers exporté une fois la partie terminée                           #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startGame (coreFunctions, guiFunctions, player1Functions, player2Functions, outputDirectory, timeout) :
    
    # Corresponding lists of existing functions
    stopFunctions = [elementFunctions[0] for elementFunctions in [coreFunctions, guiFunctions, player1Functions, player2Functions] if elementFunctions[0]]
    pollFunctions = [elementFunctions[1] for elementFunctions in [coreFunctions, guiFunctions, player1Functions, player2Functions] if elementFunctions[1]]
    
    # Function to stop all programs (useless arguments to use as a callback too)
    def stopAll (signal=None, frame=None) :
        [stopFunction() for stopFunction in stopFunctions]
    
    # We capture the CTRL+C command to stop everything on request
    signal.signal(signal.SIGINT, stopAll)
    print("Press CTRL+C to abort execution")
    
    # We stop everything if we reach a defined timeout
    timer = threading.Timer(timeout, stopAll)
    if timeout :
        timer.start()
    
    # If everything has stopped or the core has exited with an error, we stop
    while (any([pollFunction() is None for pollFunction in pollFunctions])) :
        if pollFunctions[0]() :
            stopAll()
        time.sleep(0.01)
    timer.cancel()
    
    # We return the contents of the output file if everything ended correctly
    resultsFileName = outputDirectory + "/results.txt"
    if pollFunctions[0]() == 0 and os.path.isfile(resultsFileName) :
        with open(resultsFileName, "r") as results :
            return ast.literal_eval(results.read())
    return {}
    
###################################################################################################################################################################################################################################
########################################### START RANDOM GAME FUNCTION ########################################## ################################## FONCTION DE DÉMARRAGE D'UNE PARTIE ALÉATOIRE #################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat elements and performs a game with a random maze                                            #    Démarre les éléments PyRat et joue une partie sur un labyrinthe aléatoire                                   #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeWidth : int    mazeHeight : int                                                                         #    mazeWidth : int    mazeHeight : int                                                                         #
#    ---------------    ----------------                                                                         #    ---------------    ----------------                                                                         #
#                                                                                                                #                                                                                                                #
#        Dimensions of the maze in number of cells                                                               #        Dimensions du labyrinthe en nombre de cases                                                             #
#        Both dimensions must be greater than one                                                                #        Les deux dimensions doivent être supérieures à 1                                                        #
#                                                                                                                #                                                                                                                #
#    mazeDensity : float                                                                                         #    mazeDensity : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Density of walls in the maze                                                                            #        Densité de murs dans le labyrinthe                                                                      #
#        This is a float in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible              #        C'est un réel dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible     #
#        The maze will be connected, whatever its density                                                        #        Quelle que soit la densité, le labyrinthe restera connexe                                               #
#                                                                                                                #                                                                                                                #
#    mudProbability : float                                                                                      #    mudProbability : float                                                                                      #
#    ----------------------                                                                                      #    ----------------------                                                                                      #
#                                                                                                                #                                                                                                                #
#        Probability that a path between two cells is covered in mud, thus taking more time to cross             #        Probabilité qu'un chemin entre deux cases soit couvert de boue, prenant donc plus de temps à passer     #
#        This is a float in [0, 1]                                                                               #        C'est un réel dans [0, 1]                                                                               #
#                                                                                                                #                                                                                                                #
#    mazeSymmetric : bool                                                                                        #    mazeSymmetric : bool                                                                                        #
#    --------------------                                                                                        #    --------------------                                                                                        #
#                                                                                                                #                                                                                                                #
#        If set to True, the maze will be symetric                                                               #        Si mis à True, le labyrinthe sera symétrique                                                            #
#        In that case, the pieces of cheese will also be symletrically placed                                    #        Dans ce cas, les morceaux de fromage seront aussi placés symétriquement                                 #
#                                                                                                                #                                                                                                                #
#    nbPiecesOfCheese : int                                                                                      #    nbPiecesOfCheese : int                                                                                      #
#    ----------------------                                                                                      #    ----------------------                                                                                      #
#                                                                                                                #                                                                                                                #
#        Number of pieces of cheese in the maze                                                                  #        Nombre de morceaux de fromage dans le labyrinthe                                                        #
#        This number must be lower than mazeWidth * mazeHeight - x, with x the number of players                 #        Ce nombre doit être inférieur à mazeWidth * mazeHeight - x, avec x le nombre de joueurs                 #
#        If the maze has an even number of cells and is symmetric, then nbPiecesOfCheese must be odd             #        Si le labyrinthe a un nombre pair de cases et est symétrique, nbPiecesOfCheese doit être pair           #
#                                                                                                                #                                                                                                                #
#    preprocessingTime : float                                                                                   #    preprocessingTime : float                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "preprocessing" function in the AI script                            #        Nombre de secondes allouées à la fonction "preprocessing" dans le script d'AI                           #
#                                                                                                                #                                                                                                                #
#    turnTime : float                                                                                            #    turnTime : float                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "turn" function in the AI script                                     #        Nombre de secondes allouées à la fonction "turn" dans le script d'AI                                    #
#        If this parameter set to None, the game becomes synhronous                                              #        Si ce paramètre est mis à None, le jeu est synchrone                                                    #
#                                                                                                                #                                                                                                                #
#    gameMode : string                                                                                           #    gameMode : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
#    outputDirectory : string                                                                                    #    outputDirectory : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game result is exported                                                 #        Chemin vers le réportoire où le résultat de la partie est exporté                                       #
#                                                                                                                #                                                                                                                #
#    timeout : float                                                                                             #    timeout : float                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Time after which we stop the game anyway                                                                #        Temps après lequel la partie est arrêtée quoi qu'il arrive                                              #
#        Set this parameter to None to disable the timeout                                                       #        Mettez ce paramètre à None pour désactiver le timeout                                                   #
#                                                                                                                #                                                                                                                #
#    player1FileName : string                                                                                    #    player1FileName : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the first player's AI file                                                                      #        Chemin vers le fichier d'AI pour le premier joueur                                                      #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                #                                                                                                                #
#    player2FileName : string                                                                                    #    player2FileName : string                                                                                    #
#    -------------------------                                                                                   #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the second player's AI file                                                                     #        Chemin vers le fichier d'AI pour le second joueur                                                       #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#        Optional argument                                                                                       #        Paramètre facultatif                                                                                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns what is transmitted by the game starting function                                     #    Cette fonction renvoie ce qui est transmis par la finction de création de partie                            #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startRandomGame (mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, preprocessingTime, turnTime, gameMode, outputDirectory, timeout, player1FileName, player2FileName=None) :
    
    # We start the various programs
    core = startRandomCore(mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, preprocessingTime, turnTime, gameMode, player2FileName != None, outputDirectory)
    player1 = startPlayer(1, player1FileName, gameMode)
    player2 = startPlayer(2, player2FileName, gameMode) if player2FileName else (None, None)
    gui = startGUI() if gameMode != "test" else (None, None)
    
    # We run the game with them
    return startGame(core, gui, player1, player2, outputDirectory, timeout)
    
###################################################################################################################################################################################################################################
########################################### START CUSTOM GAME FUNCTION ########################################## ################################ FONCTION DE DÉMARRAGE D'UNE PARTIE PERSONNALISÉE ###############################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Starts the PyRat elements and performs a game with a custom maze                                            #    Démarre les éléments PyRat et joue une partie sur un labyrinthe personnalisé                                #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeFileName : string                                                                                       #    mazeFileName : string                                                                                       #
#    ---------------------                                                                                       #    ---------------------                                                                                       #
#                                                                                                                #                                                                                                                #
#        Path to the maze file                                                                                   #        Chemin vers le fichier du labyrinthe                                                                    #
#                                                                                                                #                                                                                                                #
#    preprocessingTime : float                                                                                   #    preprocessingTime : float                                                                                   #
#    -------------------------                                                                                   #    -------------------------                                                                                   #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "preprocessing" function in the AI script                            #        Nombre de secondes allouées à la fonction "preprocessing" dans le script d'AI                           #
#                                                                                                                #                                                                                                                #
#    turnTime : float                                                                                            #    turnTime : float                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Number of seconds allocated to the "turn" function in the AI script                                     #        Nombre de secondes allouées à la fonction "turn" dans le script d'AI                                    #
#        If this parameter set to None, the game becomes synhronous                                              #        Si ce paramètre est mis à None, le jeu est synchrone                                                    #
#                                                                                                                #                                                                                                                #
#    gameMode : string                                                                                           #    gameMode : string                                                                                           #
#    -----------------                                                                                           #    -----------------                                                                                           #
#                                                                                                                #                                                                                                                #
#        Can take values "normal", "test" or "tournament"                                                        #        Peut prendre les valeurs "normal", "test" ou "tournament"                                               #
#        If it is "normal", the shells and GUI will show normally                                                #        Si c'est "normal", les terminaux et l'interface graphique apparaîtront normalement                      #
#        If it is "test", the GUI will not appear, and the shells will close as fast as possible                 #        Si c'est "test", l'interface graphique n'apparaîtra pas, et les terminaux se fermeront dès que possible #
#        If it is "tournament", the GUI will show normally but the shells will close as fast as possible         #        Si c'est "tournament", l'interface graphique apparaîtra, et les terminaux se fermeront dès que possible #
#                                                                                                                #                                                                                                                #
#    outputDirectory : string                                                                                    #    outputDirectory : string                                                                                    #
#    ------------------------                                                                                    #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the directory where the game result is exported                                                 #        Chemin vers le réportoire où le résultat de la partie est exporté                                       #
#                                                                                                                #                                                                                                                #
#    timeout : float                                                                                             #    timeout : float                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Time after which we stop the game anyway                                                                #        Temps après lequel la partie est arrêtée quoi qu'il arrive                                              #
#        Set this parameter to None to disable the timeout                                                       #        Mettez ce paramètre à None pour désactiver le timeout                                                   #
#                                                                                                                #                                                                                                                #
#    player1FileName> : string                                                                                   #    player1FileName : string                                                                                    #
#    -------------------------                                                                                   #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the first player's AI file                                                                      #        Chemin vers le fichier d'AI pour le premier joueur                                                      #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                #                                                                                                                #
#    player2FileName : string                                                                                    #    player2FileName : string                                                                                    #
#    -------------------------                                                                                   #    ------------------------                                                                                    #
#                                                                                                                #                                                                                                                #
#        Path to the second player's AI file                                                                     #        Chemin vers le fichier d'AI pour le second joueur                                                       #
#        This file must be derivated from the Template.py file                                                   #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#        Optional argument                                                                                       #        Paramètre facultatif                                                                                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function returns the contents of the file that is exported after the game is over                      #    Cette fonction renvoie le contenu du fichiers exporté une fois la partie terminée                           #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def startCustomGame (mazeFileName, preprocessingTime, turnTime, gameMode, outputDirectory, timeout, player1FileName, player2FileName=None) :
    
    # We start the various programs
    core = startCustomCore(mazeFileName, preprocessingTime, turnTime, gameMode, player2FileName != None, outputDirectory)
    player1 = startPlayer(1, player1FileName, gameMode)
    player2 = startPlayer(2, player2FileName, gameMode) if player2FileName else (None, None)
    gui = startGUI() if gameMode != "test" else (None, None)
    
    # We run the game with them
    return startGame(core, gui, player1, player2, outputDirectory, timeout)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################