import math
from TilesProblem import State

class SubProblem:
    def __init__(self, n, tiles):
        self.n = n
        self.legalActions = {'up', 'down', 'right', 'left'}
        start = list(range(1, n))
        start.append(0)
        self.initialState = State(start)
        self.initialState.projection(tiles)

    def heuristic(self,state):
        return 0

    def stepCost(self, state, action, newState):
        if str(state).replace('0', '*') == str(newState).replace('0', '*'):
            return 0
        return 1

    def actions(self, state):
        legalActions = self.legalActions.copy()
        dimension = int(math.sqrt(len(state.table)))
        x = state.blankPos//dimension
        y = state.blankPos-(x*dimension)
        if x == 0:
            legalActions.remove('up')
        if x == dimension-1:
            legalActions.remove('down')
        if y == 0:
            legalActions.remove('left')
        if y == dimension-1:
            legalActions.remove('right')
        return legalActions

    def result(self, state, action):
        newState = state.__copy__()
        dimension = int(math.sqrt(len(state.table)))
        move = 0
        if action == 'up':
            move = (-1)*dimension
        if action == 'down':
            move = dimension
        if action == 'left':
            move = -1
        if action == 'right':
            move = 1
        newState.table[newState.blankPos] = newState.table[newState.blankPos+move]
        newState.table[newState.blankPos+move] = 0
        newState.blankPos = newState.blankPos+move
        return newState