# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    stack = util.Stack()  #fringe
    checked = list()  #visited states will be inserted here
    path = list()  #the path we will return 
    stack.push((problem.getStartState(), []))  #we push in the fringe the state and a list with the path to reach this state, both in a tuple.
    while stack.isEmpty() == False:
        cur_state,cur_action = stack.pop()
        if cur_state not in checked:  #if state is not visited, then we add it in the visited states
            checked.append(cur_state)
            if problem.isGoalState(cur_state) == False:  #if state is not goal state, then get its successor states. 
                all_successors = problem.getSuccessors(cur_state)
                for state,action,cost in all_successors:
                #for every successor state, make the path for it (parent's_path + action) and push the tuple (state,path) in the fringe so we can check it later.
                    state_path = cur_action + [action]  
                    stack.push((state, state_path))       
            else:  #if state is goal state then return this state's path.
                path = cur_action
                return path
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #same code but fringe is queue instead of stack.
    queue = util.Queue()
    checked = list()
    path = list()
    queue.push((problem.getStartState(), []))
    while queue.isEmpty() == False:
        now_state,now_action = queue.pop()
        if now_state not in checked:
            checked.append(now_state)
            if not problem.isGoalState(now_state):
                all_successors = problem.getSuccessors(now_state)
                for state,action,cost in all_successors:
                    path_of_state = now_action + [action]
                    queue.push((state, path_of_state))       
            else:
                path = now_action
                return path
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #same code but with 3 differences
    pqueue = util.PriorityQueue()  #Firstly, fringe is priority queue
    checked = list()
    path = list()
    #secondly, in the pqueue, we insert the tuple (state,path) and also it's priority(total cost of path)
    pqueue.push((problem.getStartState(), []), 0)
    while pqueue.isEmpty() == False:
        cur_state,cur_action = pqueue.pop()
        if cur_state not in checked:
            checked.append(cur_state)
            if problem.isGoalState(cur_state) == False:
                all_successors = problem.getSuccessors(cur_state)
                for state,action,cost in all_successors:
                    state_path = cur_action + [action]
                    #Thirdly, total cost of a path is computed by the function getCostOfActions
                    tcost = problem.getCostOfActions(state_path) 
                    pqueue.push((state,state_path) ,tcost)       
            else:
                path = cur_action
                return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #same code with uniformCostSearch but the cost of a path is equal to the sum of getCostOfActions and the heuristic function for a state.
    pqueue = util.PriorityQueue()
    checked = list()
    path = list()
    pqueue.push((problem.getStartState(), []), 0)
    while pqueue.isEmpty() == False:
        cur_state,cur_action = pqueue.pop()
        if cur_state not in checked:
            checked.append(cur_state)
            if problem.isGoalState(cur_state) == False:
                all_successors = problem.getSuccessors(cur_state)
                for state,action,cost in all_successors:
                    state_path = cur_action + [action]
                    tcost = problem.getCostOfActions(state_path) + heuristic(state, problem)
                    pqueue.push((state,state_path), tcost)       
            else:
                path = cur_action
                return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
