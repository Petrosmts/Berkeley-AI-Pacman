# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        all_manhattans = list()
        for ghost_state in newGhostStates:
            if ghost_state.scaredTimer == 0 and ghost_state.getPosition() == newPos: #if there will be a ghost where the pacman will go with the action, DON'T GO THERE!
                return float('-inf')
        if action == Directions.STOP: # pacman should not stop because a ghost might get nearer to it and pacman will not even look for food.
            return float('-inf')
        for food in currentGameState.getFood().asList(): 
            manh = manhattanDistance(food, newPos)
            if manh == 0: #if pacman will be in the same position with a food, go there so it can eat it
                return float('inf')
            all_manhattans.append(1 / manh) #we want the biggest manhattan distance from a food to be the worst case, so we multiply them with -1.
        best_manhattan = max(all_manhattans) #maximum will be the smallest manhattan distance from a food.
        return best_manhattan 

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(ghost_index):
        Returns a list of legal actions for an agent
        ghost_index=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(ghost_index, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #I followed the same logic as the minimax algorithm from the slides of our lesson.
        
        pacman_index = 0
        def max_value(curr_state: GameState, game_depth):
            game_depth += 1 #every time a node is max, we must increase the current depth.
            if game_depth == self.depth or curr_state.isWin() == True or curr_state.isLose() == True: #deepening must stop if pacman wins or loses, or the current depth is equal to the depth of the game.
                return self.evaluationFunction(curr_state)
            #for every available action, I do exactly what the slides of the lesson show us to do.
            v = float('-inf')
            for action in curr_state.getLegalActions(pacman_index):
                succ_state = curr_state.generateSuccessor(pacman_index, action)
                v = max(v, min_value(succ_state, 1, game_depth)) 
            return v
        

        def min_value(curr_state: GameState, ghost_index, game_depth):
            if curr_state.isWin() == True or curr_state.isLose() == True: #deepening must stop if pacman wins or loses.
                return self.evaluationFunction(curr_state)
            #for every available action, I do exactly what the slides of the lesson show us to do.
            v = float('inf')
            for action in curr_state.getLegalActions(ghost_index):
                succ_state = curr_state.generateSuccessor(ghost_index, action)
                if ghost_index == (curr_state.getNumAgents() - 1): #if it's the last ghost, then pacman is playing.
                    v = min(v, max_value(succ_state,game_depth))
                else: #if not, then the next ghost is playing.
                    next_ghost = ghost_index + 1
                    v = min(v, min_value(succ_state, next_ghost, game_depth))
            return v
        

        minimax_list = list()
        for action in gameState.getLegalActions(pacman_index):
            curr_state = gameState.generateSuccessor(pacman_index, action)
            minimax_value = min_value(curr_state, 1, 0)
            minimax_list.append((minimax_value, action)) #we put every minimax value in a tuple with the action that caused her and the tuple in a list.
            best_action = max(minimax_list)[1] #pacman is a max node so it will choose the action with the biggest minimax value.
        return best_action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #I followed the same logic as the alpha-beta algorithm from the slides of our lesson.
        pacman_index = 0
        def max_value(curr_state: GameState, game_depth, a, b):
            game_depth += 1
            if game_depth == self.depth or curr_state.isWin() == True or curr_state.isLose() == True:
                return self.evaluationFunction(curr_state)
            v = float('-inf')
            for action in curr_state.getLegalActions(pacman_index):
                succ_state = curr_state.generateSuccessor(pacman_index, action)
                v = max(v, min_value(succ_state, 1, game_depth, a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v
              

        def min_value(curr_state: GameState, ghost_index, game_depth, a, b):
            if curr_state.isWin() == True or curr_state.isLose() == True: 
                return self.evaluationFunction(curr_state) 
            v = float('inf')          
            for action in curr_state.getLegalActions(ghost_index):
                succ_state = curr_state.generateSuccessor(ghost_index,action)
                if ghost_index == (curr_state.getNumAgents() - 1): #if it's the last ghost, then pacman is playing.
                    v = min(v, max_value(succ_state, game_depth, a, b))
                else: #if not, then the next ghost is playing.
                    next_ghost = ghost_index + 1
                    v = min(v, min_value(succ_state, next_ghost, game_depth, a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v
        

        a = float('-inf')
        b = float('inf')
        alphabeta_list = list()
        for action in gameState.getLegalActions(pacman_index):
            curr_state = gameState.generateSuccessor(pacman_index, action)
            alphabeta_value= min_value(curr_state, 1, 0, a, b) #we find alphabeta value for every action.
            a = max(a,alphabeta_value) #we have to update the variable a for the root node too.
            alphabeta_list.append((alphabeta_value, action)) #we put every alphabeta value in a tuple with the action that caused her and the tuple in a list.
            best_action = max(alphabeta_list)[1] #pacman is a max node so it will choose the action with the biggest alphabeta value.
        return best_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #we implement the expectimax algorithm.
        pacman_index = 0
        def max_value(curr_state: GameState, game_depth):
            game_depth += 1
            if game_depth == self.depth or curr_state.isWin() == True or curr_state.isLose() == True:
                return self.evaluationFunction(curr_state)
            v = float('-inf')
            for action in curr_state.getLegalActions(pacman_index):
                succ_state = curr_state.generateSuccessor(pacman_index, action)
                v = max(v, expectimax_value(succ_state, 1, game_depth))
            return v
        

        def expectimax_value(curr_state: GameState, ghost_index, game_depth):
            all_actions = curr_state.getLegalActions(ghost_index)
            if curr_state.isWin() == True or curr_state.isLose() == True: 
                return self.evaluationFunction(curr_state)
            v = float('inf')
            sum_of_values = 0
            for action in all_actions:
                succ_state = curr_state.generateSuccessor(ghost_index, action)
                if ghost_index == (curr_state.getNumAgents() - 1): #if it's the last ghost, then pacman is playing.
                    v = max_value(succ_state,game_depth)
                else: #if not, then the next ghost is playing.
                    next_ghost = ghost_index + 1
                    v = expectimax_value(succ_state, next_ghost, game_depth)
                sum_of_values += v
            return sum_of_values / len(all_actions) #the expectimax value of a node, is the average value of the values of all actions. 
        

        expectimax_list = list()
        for action in gameState.getLegalActions(pacman_index):
            curr_state = gameState.generateSuccessor(pacman_index, action)
            expectmax_value = expectimax_value(curr_state, 1, 0)
            expectimax_list.append((expectmax_value, action)) #we put every expectimax value in a tuple with the action that caused her and the tuple in a list.
            best_action = max(expectimax_list)[1] #pacman is a max node so it will choose the action with the biggest expectimax value.
        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #useful information we can extract.
    currentFood = currentGameState.getFood().asList()
    currentPos = currentGameState.getPacmanPosition()
    currentGhostStates = currentGameState.getGhostStates()

    min_distance = 1000 #I tried to put a very high value(like float('inf') or even 1200) but it didn't work so I put 1000).
    evaluation = 0 #we initialize the variable evaluation with 0 and the function will return 'evaluation + state's score'.

    #check for ghosts
    for ghost_state in currentGhostStates: 
        current_ghost_position = ghost_state.getPosition() 
        if(ghost_state.scaredTimer == 0): #if a ghost is NOT scared.
            manh = manhattanDistance(currentPos, current_ghost_position)
            if(manh == 0): #if a ghost will be in the same position with the pacman in this state we have to reduce our evaluation(I tried with 20 and it worked).
                evaluation -= 20 
            if(manh == 1): #if a ghost will be next to pacman, we have to reduce our evaluation(I reduce with less than 20(with 10) because it's better to have a ghost next to you rather than on you:)).
                evaluation -= 10
        else: #a scared ghost can be eaten from pacman so we must increase the evaluation.
            evaluation += 150 #I tried to add 200 but with 150 I get better score.

    #check for foods
    for food in currentFood:
        manh = manhattanDistance(currentPos,food)
        if(manh < min_distance): #we find the distance between the nearest food to pacman and pacman.
            min_distance = manh
    evaluation += (100 - 0.5*min_distance) #after many tests, I thought about this and I get a very nice score in autograder. The smallest is the distance between the nearest food to pacman and pacman, the biggest value we add to evaluation.  
    return evaluation + currentGameState.getScore() 
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
