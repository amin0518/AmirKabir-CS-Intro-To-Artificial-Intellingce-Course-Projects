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
from game import Directions, Actions, Configuration
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        return betterEvaluationFunction(successorGameState)


def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):  # scoreEvaluationFunction
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether the game state is a winning state

        gameState.isLose():
        Returns whether the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        isTerminal = lambda state: (state.isWin() or state.isLose())
        isPacman = lambda agent: agent == 0

        def miniMax(state, agent, depth):
            agent = agent % gameState.getNumAgents()
            if isTerminal(state):
                return self.evaluationFunction(state), 'Stop'
            if isPacman(agent):
                if depth == self.depth:
                    return self.evaluationFunction(state), 'Stop'
                return max_move(state, agent, depth + 1)
            else:
                return min_move(state, agent, depth)

        def max_move(state, agent, depth):
            legalMoves = state.getLegalActions(agent)
            bestUtil = float('-inf')
            bestMove = 'Stop'
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil, nextAgentMove = miniMax(stateAfterMove, agent + 1, depth)
                if stateUtil > bestUtil:
                    bestUtil = stateUtil
                    bestMove = move
            # if depth == 1:
            #     print("best move and util at depth 1 == ",bestUtil, bestMove)
            return bestUtil, bestMove

        def min_move(state, agent, depth):
            legalMoves = state.getLegalActions(agent)
            bestUtil = float('inf')
            bestMove = 'Stop'
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil, nextAgentMove = miniMax(stateAfterMove, agent + 1, depth)
                if stateUtil < bestUtil:
                    bestUtil = stateUtil
                    bestMove = move

            return bestUtil, bestMove

        minimaxUtil, minimaxMove = miniMax(gameState, 0, 0)
        return minimaxMove


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        isTerminal = lambda state: (state.isWin() or state.isLose())
        isPacman = lambda agent: agent == 0

        def miniMax(state, agent, depth, alpha, beta):
            agent = agent % gameState.getNumAgents()
            if isTerminal(state):
                return self.evaluationFunction(state), 'Stop'
            if isPacman(agent):
                if depth == self.depth:
                    return self.evaluationFunction(state), 'Stop'
                return max_move(state, agent, depth + 1, alpha, beta)
            else:
                return min_move(state, agent, depth, alpha, beta)

        def max_move(state, agent, depth, alpha, beta):
            legalMoves = state.getLegalActions(agent)
            bestUtil = float('-inf')
            bestMove = 'Stop'
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil, nextAgentMove = miniMax(stateAfterMove, agent + 1, depth, alpha, beta)
                if stateUtil > bestUtil:
                    bestUtil = stateUtil
                    bestMove = move
                if bestUtil > beta:
                    return bestUtil, bestMove
                alpha = max(alpha, bestUtil)

            # if depth == 1:
            #     print("best move and util at depth 1 == ",bestUtil, bestMove)
            return bestUtil, bestMove

        def min_move(state, agent, depth, alpha, beta):
            legalMoves = state.getLegalActions(agent)
            bestUtil = float('inf')
            bestMove = 'Stop'
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil, nextAgentMove = miniMax(stateAfterMove, agent + 1, depth, alpha, beta)
                if stateUtil < bestUtil:
                    bestUtil = stateUtil
                    bestMove = move
                if bestUtil < alpha:
                    return bestUtil, bestMove
                beta = min(beta, bestUtil)

            return bestUtil, bestMove

        minimaxUtil, minimaxMove = miniMax(gameState, 0, 0, float('-inf'), float('inf'))
        return minimaxMove


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def __int__(self):
        super()
        self.BestMove = None

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        isTerminal = lambda state: (state.isWin() or state.isLose())
        isPacman = lambda agent: agent == 0

        def expectiMax(state, agent, depth):
            agent = agent % gameState.getNumAgents()
            if isTerminal(state):
                return self.evaluationFunction(state)
            if isPacman(agent):
                if depth == self.depth:
                    return self.evaluationFunction(state)
                return maxMoveValue(state, agent, depth + 1)
            else:
                return expectedMoveValue(state, agent, depth)

        def maxMoveValue(state, agent, depth):
            legalMoves = state.getLegalActions(agent)
            bestUtil = float('-inf')
            bestMove = 'Stop'
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil = expectiMax(stateAfterMove, agent + 1, depth)
                if stateUtil > bestUtil:
                    bestUtil = stateUtil
                    bestMove = move
            if depth == 1:
                self.BestMove = bestMove
            return bestUtil

        def expectedMoveValue(state, agent, depth):
            legalMoves = state.getLegalActions(agent)
            prob = 1 / len(legalMoves)
            expectedUtil = 0
            for move in legalMoves:
                stateAfterMove = state.generateSuccessor(agent, move)
                stateUtil = expectiMax(stateAfterMove, agent + 1, depth)
                expectedUtil += stateUtil
            return expectedUtil

        expectiMaxUtil = expectiMax(gameState, 0, 0)
        return self.BestMove


def nearestFoodsBFS(currentGameState, foodPositionList, leastFoodS):
    numberOfFoodSPots = len(foodPositionList)
    numberOfTargetFoodSPots = min(leastFoodS, numberOfFoodSPots)  # least number of food spots needed to consider
    numberOfFoodSPotsGot = 0
    root = currentGameState.getPacmanPosition()
    distance = {root: 0}
    visitedNodes = {root}
    queue = util.Queue()
    walls = currentGameState.getWalls()
    queue.push(root)
    foodSpotDistance = {}
    while not queue.isEmpty():
        spot = queue.pop()
        if spot in foodPositionList:
            foodSpotDistance[spot] = distance[spot]
            numberOfFoodSPotsGot += 1

            if numberOfFoodSPotsGot == numberOfTargetFoodSPots:
                return sum(foodSpotDistance.values())

        for action in Directions.allMovementactions:
            nextSpot = Directions.nextInDirection(spot, action)
            if not walls[nextSpot[0]][nextSpot[1]] and nextSpot not in visitedNodes:
                distance[nextSpot] = distance[spot] + 1
                queue.push(nextSpot)
                visitedNodes.add(nextSpot)


# def nearestGhostBFS(currentGameState, currentGhostStates):
#     currentGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates]
#     root = currentGameState.getPacmanPosition()
#     distance = {root: 0}
#     visitedNodes = {root}
#     queue = util.Queue()
#     walls = currentGameState.getWalls()
#     queue.push(root)
#     while not queue.isEmpty():
#         spot = queue.pop()
#         if spot in currentGhostPositions:
#             scaredTimer = [ghostState.scaredTimer for ghostState in currentGhostStates if
#                            spot == ghostState.getPosition()]
#             if scaredTimer is [] or scaredTimer is None or scaredTimer is [None]:
#                 scaredTimer = 0
#             else:
#                 scaredTimer = scaredTimer[0]
#
#             return distance[spot], scaredTimer
#
#         for action in Directions.allMovementactions:
#             nextSpot = Directions.nextInDirection(spot, action)
#             if not walls[nextSpot[0]][nextSpot[1]] and nextSpot not in visitedNodes:
#                 distance[nextSpot] = distance[spot] + 1
#                 queue.push(nextSpot)
#                 visitedNodes.add(nextSpot)


def betterEvaluationFunction(currentGameState):
    if currentGameState.isWin():
        return 100000000 + currentGameState.getScore()
    elif currentGameState.isLose():
        return -100000000 + currentGameState.getScore()

    currentPacmanPos = currentGameState.getPacmanPosition()
    currentFoodPositions = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    # currentGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates]
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    currentCapsules = currentGameState.getCapsules()

    distanceFromPacman = lambda pos: util.manhattanDistance(currentPacmanPos, pos)
    addedScore = 0

    addedScore += 20 * 1 / nearestFoodsBFS(currentGameState, currentFoodPositions, 3)  # 20
    addedScore -= 30 * len(currentFoodPositions)

    # currentGhostStates = sorted(currentGhostStates, key=lambda ghostState: ghostState.scaredTimer, reverse=True)

    for ghostState in currentGhostStates:
        ghostDistance = distanceFromPacman(ghostState.getPosition())

        ghostScaredTimeLeft = ghostState.scaredTimer

        if ghostScaredTimeLeft < ghostDistance:
            if ghostDistance <= 4:
                addedScore -= 100
            elif ghostDistance <= 3:
                addedScore -= 5000
                if ghostDistance <= 2:
                    addedScore -= 200000
            # else:
            #     addedScore -= 1 / ghostDistance
        else:
            addedScore += 3 / ghostDistance #10*ghostScaredTimeLeft

    minScaredTimeLeft = min(currentScaredTimes)

    if currentCapsules:
        addedScore += sum([1 / distanceFromPacman(capsule)
                           for capsule in currentCapsules
                           if minScaredTimeLeft <= 0])
    # if minScaredTimeLeft > 0:
    #     addedScore -= 20 * len(currentCapsules)

    # if len(currentGhostStates) > 0:
    #     minGhostDistance, ghostScaredTimeLeft = nearestGhostBFS(currentGameState, currentGhostStates)
    #
    #     if ghostScaredTimeLeft < minGhostDistance:
    #         if minGhostDistance <= 3:
    #             addedScore -= 2000
    #             if minGhostDistance <= 2:
    #                 addedScore -= 200000
    #         else:
    #             addedScore += 3 / minGhostDistance

    return addedScore + 0.2 * currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction

# moveAndUtility = {}
# legalMoves = state.getLegalActions(agent)
#
# for action in legalMoves:
#     moveAndUtility[action] = min_move(state.generateSuccessor(agent, action), agent + 1, depth)
#
# bestMove = max(moveAndUtility, key=moveAndUtility.get)
# bestUtil = moveAndUtility[bestMove]
#
# return bestUtil, bestMove
