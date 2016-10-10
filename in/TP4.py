#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################# PRE-DEFINED CONSTANTS ############################################# ############################################ CONSTANTES PRÉ-DÉFINIES ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    In this section, you will find some pre-defined constants that are needed for the game                      #    Dans cette section, vous trouvez des constantes pré-définies nécessaires pour la partie                     #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    TEAM_NAME : string                                                                                          #    TEAM_NAME : string                                                                                          #
#    ------------------                                                                                          #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        This constant represents your name as a team                                                            #        Cette constante représente le nom de votre équipe                                                       #
#        Please change the default value to a string of your choice                                              #        Veuillez en changer la valeur par une chaîne de caractères de votre choix                               #
#                                                                                                                #                                                                                                                #
#    MOVE_XXX : char                                                                                             #    MOVE_XXX : char                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        The four MOVE_XXX constants represent the possible directions where to move                             #        Les quatre constantes MOVE_XXX représentent les directions possibles où se déplacer                     #
#        The "turn" function should always return one of these constants                                         #        La fonction "turn" doit toujours renvoyer l'une d'entre elles                                           #
#        Please do not edit them (any other value will be considered incorrect and thus ignored)                 #        Merci de ne pas les éditer (toute autre valeur sera considérée comme incorrecte et sera ignorée)        #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

TEAM_NAME = "Your name here"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###################################################################################################################################################################################################################################
########################################### SPACE FOR FREE EXPRESSION ########################################### ############################################ ZONE D'EXPRESSION LIBRE ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    In this file, you will two functions: "preprocessing" and "turn"                                            #    Dans ce fichier, vous trouverez deux fonctions : "preprocessing" et "turn"                                  #
#    You need to edit these functions to create your PyRat program                                               #    Vous devez éditer ces fonctions pour réaliser votre programme PyRat                                         #
#    However, you are not limited to them, and you can write any Python code in this file                        #    Toutefois, vous n'êtes pas limité(e), et vous pouvez écrire n'importe quel code Python dans ce fichier      #
#    Please use the following space to write your additional constants, variables, functions...                  #    Merci d'utiliser l'espace ci-dessous pour écrire vos constantes, variables, fonctions...                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

#type arbre = |Empty
 #            |Node of (arbre*(element,etiquette)*arbre)
  #        
#def CreateEmptyTasmin():
#    return Empty
#def isEmptyTasmin(arbre):
#    return arbre == Empty
#def push(arbre,element,etiquette):
#    if  
                                    #
                                            #Si tous les nœuds parents ont deux nœuds fils, on transforme une feuille de profondeur minimale en parent de ce nouveau nœud
                                            #Si un nœud parent n’a qu’un seul fils, on lui ajoute comme deuxième fils ce nouveau nœud



def moveFromLocations (sourceLocation, targetLocation) : 
    difference = tuple(numpy.subtract(targetLocation, sourceLocation))          #substract makes the substraction between the coordinate's tuples of the two cases 
    if difference == (1, 0) :                                                       
        return MOVE_DOWN                                                        # With the difference we define the move
    elif difference == (-1, 0) :
        return MOVE_UP
    elif difference == (0, 1) :
        return MOVE_RIGHT
    elif difference == (0, -1) :
        return MOVE_LEFT
    elif difference == (0,0) :
        return "standBy"
    else :
        raise Exception((sourceLocation, targetLocation)) # In case of wall we raise an error



import heapq, numpy
from math import inf

def heapInsertOrReplace(heap,item):                                             
    element=item[0]
    if element not in [k[0] for k in heap]:                                     # In case of non existence of the item (couple : element,weight) in the heap we add this item to our heap  
        heapq.heappush(heap,item)
    else:                                                                       # Else we update the weight of the already existing node

        pos=[k[0] for k in heap].index(element)                                 #index is a function from Python which returns the index of the element which already exists in the list
        heap[pos]=item
        heapq.heapify(heap)
        
    



def dijkstra(mazeMap,beginningNode):
    distances={}
    route={}
    for pos in mazeMap:
        distances[pos]=inf
        route[pos]=None
    heap=[]
    heapq.heappush(heap,(beginningNode,0))
    distances[beginningNode]=0
    while heap !=[] :
        (currentNode,currentNodeDistance)=heapq.heappop(heap)
        for neighbor in mazeMap[currentNode]:
            distance=mazeMap[currentNode][neighbor]
            totalDistance = currentNodeDistance + distance
            if  totalDistance < distances[neighbor]:
                route[neighbor] = currentNode
                distances[neighbor] = totalDistance
                heapInsertOrReplace(heap,(neighbor,totalDistance))
    return (route,distances)


def shortestPath(route,beginningNode,finalNode):
    path=[]
    currentNode=finalNode                                  # We start from the end and we go up until we reach the beginning node 
    while currentNode != beginningNode :
        path = [currentNode]+path                          # We put the current node in the beginning of the path (since we go from finalNode to beginningNode )                
        currentNode = route[currentNode]                   # We choose the neighbours to add thanks to the routing of the previous function
    path = [currentNode]+path                              
    return path                                            # We return the path as a list of couples (coordinates)





def metaGraph(mazeMap,piecesOfCheese,beginningNode):
    metaGraph = {}
    listOfRoutes = {}
    (route,distances) = dijkstra(mazeMap, beginningNode)
    metaGraph[beginningNode] = {}
    for cheese in piecesOfCheese :
        metaGraph[beginningNode][cheese] = distances[cheese]
        listOfRoutes[beginningNode] = route
    for currentNode in piecesOfCheese :
        (route,distances) = dijkstra(mazeMap,currentNode)
        metaGraph[currentNode] = {}
        metaGraph[currentNode][beginningNode] = distances[beginningNode]
        for cheese in piecesOfCheese :
            metaGraph[currentNode][cheese] = distances[cheese]
            listOfRoutes[currentNode] = route
    return (metaGraph,listOfRoutes)
            
                
    
    
def travellingSalesman (metaGraph, beginningNode) :
    bestLength = inf
    bestPath = None
    def exhaustive (remainingNodes, currentNode, currentPath, currentLength, graph) :
        if remainingNodes == [] :
            nonlocal bestLength, bestPath
            if currentLength < bestLength :
                bestLength = currentLength
                bestPath = currentPath
        else :
            for neighbor in graph[currentNode] :
                
                weight = graph[currentNode][neighbor]
                if neighbor in remainingNodes :
                    print("SuperSalut")
                    otherNodes = [x for x in remainingNodes if x != neighbor]
                    exhaustive(otherNodes, neighbor, currentPath + [neighbor], currentLength + weight, graph)
    otherNodes = [x for x in metaGraph if x != beginningNode]
    exhaustive(otherNodes, beginningNode, [beginningNode], 0, metaGraph)
    return (bestPath, bestLength)   


    







###################################################################################################################################################################################################################################
############################################# PREPROCESSING FUNCTION ############################################ ########################################### FONCTION DE PRÉ-TRAITEMENT ##########################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function is executed once at the very beginning of the game                                            #    Cette fonction est exécutée une unique fois au tout début de la partie                                      #
#    It allows you to make some computations before the players are allowed to move                              #    Vous pouvez y effectuer des calculs avant que les joueurs ne puissent commencer à bouger                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #
#    ---------------------------------------------------------                                                   #    ---------------------------------------------------------                                                   #
#                                                                                                                #                                                                                                                #
#        Map of the maze as a data structure                                                                     #        Structure de données représentant la carte du labyrinthe                                                #
#        mazeMap[x] gives you the neighbors of cell x                                                            #        mazeMap[x] renvoie les voisins de la case x                                                             #
#        mazeMap[x][y] gives you the weight of the edge linking cells x and y                                    #        mazeMap[x][y] renvoie le poids de l'arête reliant les cases x et y                                      #
#        if mazeMap[x][y] is undefined, there is no edge between cells x and y                                   #        Si mazeMap[x][y] n'est pas défini, les cases x et y ne sont pas reliées par une arête                   #
#                                                                                                                #                                                                                                                #
#    mazeWidth : int                                                                                             #    mazeWidth : int                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Width of the maze, in number of cells                                                                   #        Largeur du labyrinthe, en nombre de cases                                                               #
#                                                                                                                #                                                                                                                #
#    mazeHeight : int                                                                                            #    mazeHeight : int                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Height of the maze, in number of cells                                                                  #        Hauteur du labyrinthe, en nombre de cases                                                               #
#                                                                                                                #                                                                                                                #
#    playerLocation : pair(int, int)                                                                             #    playerLocation : pair(int, int)                                                                             #
#    -------------------------------                                                                             #    -------------------------------                                                                             #
#                                                                                                                #                                                                                                                #
#        Initial location of your character in the maze                                                          #        Emplacement initial de votre personnage dans le labyrinthe                                              #
#        It is a pair (line, column), with (0, 0) being the top-left cell in the maze                            #        C'est une paire (ligne, colonne), (0, 0) étant la case en haut à gauche du labyrinthe                   #
#        playerLocation[0] gives you your current line                                                           #        playerLocation[0] renvoie votre ligne actuelle                                                          #
#        playerLocation[1] gives you your current column                                                         #        playerLocation[1] renvoie votre colonne actuelle                                                        #
#        mazeMap[playerLocation] gives you the cells you can access directly                                     #        mazeMap[playerLocation] renvoie les cases auxquelles vous pouvez accéder directement                    #
#                                                                                                                #                                                                                                                #
#    opponentLocation : pair(int, int)                                                                           #    opponentLocation : pair(int, int)                                                                           #
#    ---------------------------------                                                                           #    ---------------------------------                                                                           #
#                                                                                                                #                                                                                                                #
#        Initial location opponent's character in the maze                                                       #        Emplacement initial du personnage de votre adversaire dans le labyrinthe                                #
#        The opponent's location can be used just as playerLocation                                              #        La position de l'adversaire peut être utilisée comme pour playerLocation                                #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    piecesOfCheese : list(pair(int, int))                                                                       #    piecesOfCheese : list(pair(int, int))                                                                       #
#    -------------------------------------                                                                       #    -------------------------------------                                                                       #
#                                                                                                                #                                                                                                                #
#        Locations of all pieces of cheese in the maze                                                           #        Emplacements des morceaux de fromage dans le labyrinthe                                                 #
#        The locations are given in no particular order                                                          #        Les emplacements sont données dans un ordre quelconque                                                  #
#        As for the players locations, these locations are pairs (line, column)                                  #        Comme pour les positions des joueurs, ces emplacements sont des paires (ligne, colonne)                 #
#                                                                                                                #                                                                                                                #
#    timeAllowed : float                                                                                         #    timeAllowed : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Time that is allowed for preprocessing, in seconds                                                      #        Temps alloué pour le pré-traitement, en secondes                                                        #
#        After this time, players will have the right to move                                                    #        Après ce temps, les joueurs pourront commencer à bouger                                                 #
#        If your preprocessing is too long, you will still finish it                                             #        Si votre pré-traitement est trop long, vous terminerez quand même son exécution                         #
#        However, it will not prevent your opponent from moving                                                  #        Toutefois, cela n'empêchera pas votre adversaire de bouger                                              #
#        Make sure to finish your preprocessing within the allowed time                                          #        Assurez vous de terminer votre pré-traitement dans le temps imparti                                     #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function does not return anything                                                                      #    Cette fonction ne renvoie rien                                                                              #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    (graph,listOfRoutes) = metaGraph(mazeMap,piecesOfCheese,playerLocation)
    (bestPath, bestLength) = travellingSalesman(graph,playerLocation)
    print(bestPath)
    global finalPath
    finalPath = [playerLocation]
    for k in range (len(bestPath)-1) :
        route = listOfRoutes[bestPath[k]]
        path = shortestPath(route,bestPath[k],bestPath[k+1])
        finalPath += path[1:]
    print(finalPath)
        
        
    
    
###################################################################################################################################################################################################################################
################################################# TURN FUNCTION ################################################# ############################################ FONCTION DE TOUR DE JEU ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Once the preprocessing is over, the game starts and players can start moving                                #    Une fois le pré-traitement terminé, la partie démarre et les joueurs peuvent commencer à bouger             #
#    The "turn" function is called at regular times                                                              #    La fonction "turn" est appelée à intervalles réguliers                                                      #
#    You should determine here your next move, given a game configuration                                        #    Vous devez déterminer ici votre prochain mouvement, étant donnée une configuration du jeu                   #
#    This decision will then be applied, and your character will move in the maze                                #    Cette décision sera ensuite appliquée, et votre personnage se déplacera dans le labyrinthe                  #
#    Then, the "turn" function will be called again with the new game configuration                              #    Ensuite, la fonction "turn" sera appelée à nouveau, avec la nouvelle configuration du jeu                   #
#    This process is repeated until the game is over                                                             #    Ce processus est répété jusqu'à la fin de la partie                                                         #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #
#    ---------------------------------------------------------                                                   #    ---------------------------------------------------------                                                   #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeMap does not change between two calls of function "turn"                               #        La valeur de mazeMap ne change pas d'un appel à l'autre de la fonction "turn"                           #
#                                                                                                                #                                                                                                                #
#    mazeWidth : int                                                                                             #    mazeWidth : int                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeWidth does not change between two calls of function "turn"                             #        La valeur de mazeWidth ne change pas d'un appel à l'autre de la fonction "turn"                         #
#                                                                                                                #                                                                                                                #
#    mazeHeight : int                                                                                            #    mazeHeight : int                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeHeight does not change between two calls of function "turn"                            #        La valeur de mazeHeight ne change pas d'un appel à l'autre de la fonction "turn"                        #
#                                                                                                                #                                                                                                                #
#    playerLocation : pair(int, int)                                                                             #    playerLocation : pair(int, int)                                                                             #
#    -------------------------------                                                                             #    -------------------------------                                                                             #
#                                                                                                                #                                                                                                                #
#        Current location of your character in the maze                                                          #        Emplacement actuel de votre personnage dans le labyrinthe                                               #
#        At the first call of function "turn", it will be your initial location                                  #        Au premier appel de la fonction "turn", ce sera votre emplacement initial                               #
#                                                                                                                #                                                                                                                #
#    opponentLocation : pair(int, int)                                                                           #    opponentLocation : pair(int, int)                                                                           #
#    ---------------------------------                                                                           #    ---------------------------------                                                                           #
#                                                                                                                #                                                                                                                #
#        Current location of your opponent's character in the maze                                               #        Emplacement actuel de votre personnage dans le labyrinthe                                               #
#        At the first call of function "turn", it will be your opponent's initial location                       #        Au premier appel de la fonction "turn", ce sera votre emplacement initial                               #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    playerScore : float                                                                                         #    playerScore: float                                                                                          #
#    -------------------                                                                                         #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        Your current score when the turn begins                                                                 #        Votre score actuel au début du tour                                                                     #
#        It is initialized at 0, and increases by 1 when you eat a piece of cheese                               #        Il est initialisé à 0, et augmente de 1 pour chaque morceau de fromage mangé                            #
#        If you reach the same piece of cheese as your opponent at the same moment, it is worth 0.5 points       #        Si vous arrivez sur le même morceau de fromage que votre adversaire au même moment, il vaut 0.5 points  #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    opponentScore : float                                                                                       #    opponentScore: float                                                                                        #
#    ---------------------                                                                                       #    --------------------                                                                                        #
#                                                                                                                #                                                                                                                #
#        The score of your opponent when the turn begins                                                         #        Le score de votre adversaire au début du tour                                                           #
#                                                                                                                #                                                                                                                #
#    piecesOfCheese : list(pair(int, int))                                                                       #    piecesOfCheese : list(pair(int, int))                                                                       #
#    -------------------------------------                                                                       #    -------------------------------------                                                                       #
#                                                                                                                #                                                                                                                #
#        Locations of all remaining pieces of cheese in the maze                                                 #        Emplacements des morceaux de fromage restants dans le labyrinthe                                        #
#        The list is updated at every call of function "turn"                                                    #        La liste est mise à jour à chaque appel de la fonction "turn"                                           #
#                                                                                                                #                                                                                                                #
#    timeAllowed : float                                                                                         #    timeAllowed : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Time that is allowed for determining the next move to perform, in seconds                               #        Temps alloué pour le calcul du prochain mouvement, en secondes                                          #
#        After this time, the decided move will be applied                                                       #        Après ce temps, le mouvement choisi sera appliqué                                                       #
#        If you take too much time, you will still finish executing your code, but you will miss the deadline    #        Si vous prenez trop de temps, votre code finira quand-même son excution, mais vous raterez le timing    #
#        Your move will then be considered the next time PyRat checks for players decisions                      #        Votre mouvement sera alors considéré la prochaine fois que PyRat vérifiera les décisions des joueurs    #
#        However, it will not prevent your opponent from moving if he respected the deadline                     #        Toutefois, cela n'empêchera pas votre adversaire de bouger s'il a respecté le timing                    #
#        Make sure to finish your computations within the allowed time                                           #        Assurez vous de terminer vos calculs dans le temps imparti                                              #
#        Also, save some time to ensure that PyRat will receive your decision before the deadline                #        Aussi, gardez un peu de temps pour garantir que PyRat recevra votre decision avant la fin du temps      #
#        If you are playing in synchronous mode, this variable is undefined                                      #        Si vous jouez en mode synchrone, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function should return one of the following constants: MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP       #    Cette fonction renvoie l'une des constantes suivantes : MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP           #
#    The returned constant represents the move you decide to perform: down, left, right, up                      #    La constante renvoyée représente le mouvement que vous décidez d'effectuer : bas, gauche, droite, haut      #
#    Any other value will be ignored and will lead to a turn spent without moving                                #    Toute autre valeur sera ignorée, et entraînera la perte du tour de jeu                                      #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    move = 'X'                                                # If the list is empty, the player stands still
    
    if len(finalPath)>1:
                                                 # If at least one move remain (thus 2 couples)
        move = moveFromLocations(finalPath[0],finalPath[1])          # We convert the cases to a move understandable by the core
        if move == "standBy" :
            finalPath.pop(0)
            move = moveFromLocations(finalPath[0],finalPath[1])                                                         
        finalPath.pop(0)
    if move != 'X' :
        print(playerLocation)                                          # Then we remove the first coordinates of the path
    return(move)

###################################################################################################################################################################################################################################
###################################################################################################################################################################################################################################