import pickle
import math
import random


def getValueFromDB(state, tiles, file):
    keyState = state.__copy__()
    db = pickle.load(open(file, 'rb'))
    keyState.projection(tiles)
    key = str(keyState)
    value = db[key]
    return value


class State:
    def __init__(self, table):
        self.table = table.copy()
        for i in range(len(table)):
            if table[i] == 0:
                self.blankPos = i

    def __str__(self):
        s = ''
        for i in range(len(self.table)):
            if self.table[i] != len(self.table):
                s += str(self.table[i])+','
            else:
                s += '*,'
        return s[:-1]

    def __copy__(self):
        return State(self.table)

    def projection(self, tiles):
        n = len(self.table)
        for i in range(n):
            if (self.table[i] not in tiles) and self.table[i] != 0:
                self.table[i] = n

class TilesProblem:
    def __init__(self, n, scrambles=100):
        self.scrambles = scrambles
        self.n = n
        self.legalActions = {'left', 'right', 'up', 'down'}
        goal = list(range(1, self.n))
        goal.append(0)
        self.goalState = State(goal)
        self.h = self.uniformCost
        self.db1 = pickle.load(open('DB-15Tiles\\DB1.txt', 'rb'))
        self.db2 = pickle.load(open('DB-15Tiles\\DB2.txt', 'rb'))
        self.db3 = pickle.load(open('DB-15Tiles\\DB3.txt', 'rb'))
        self.db4 = pickle.load(open('DB-15Tiles\\DB4.txt', 'rb'))
        self.db5 = pickle.load(open('DB-15Tiles\\DB5.txt', 'rb'))
        self.db6 = pickle.load(open('DB-15Tiles\\DB6.txt', 'rb'))

    def setHeuristic(self, heuristic):
        if heuristic == 'uniformCost':
            self.h = self.uniformCost
        if heuristic == 'manhattan':
            self.h = self.manhattan
        if heuristic == 'linearConflicts':
            self.h = self.linearConflicts
        if heuristic == 'disjointDatabases':
            self.h = self.disjointDatabases
        if heuristic == 'disjointAndReflected':
            self.h = self.disjointAndReflected

    def heuristic(self, state):
        return self.h(state)

    def setInitialState(self, table):
        self.n = len(table)
        self.initialState = State(table)
        goal = list(range(1, self.n))
        goal.append(0)
        self.goalState = State(goal)

    def randomTable(self):
        state = self.goalState.__copy__()
        for i in range(self.scrambles):
            action = random.sample(self.actions(state), 1)
            state = self.result(state, action[0])
        return state.table

    def stepCost(self, state, action, newState):
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

    def goalTest(self, state):
        for i in range(len(state.table)):
            if state.table[i]!=self.goalState.table[i]:
                return False
        return True

    def getValueFromDB(self,state, tiles, db):
        keyState = state.__copy__()
        keyState.projection(tiles)
        key = str(keyState)
        return db[key]

    # TODO define heuristics here! they must have a state for formal parameter

    def uniformCost(self, state):
        return 0

    def manhattan(self, state):
        n = len(state.table)
        distance = 0
        dimension = int(math.sqrt(n))
        for i in range(n):
            if state.table[i] != 0:
                x = i // dimension
                y = i - x * dimension
                goalPos = state.table[i] - 1
                goalX = goalPos // dimension
                goalY = goalPos - goalX * dimension
                distance += abs(x - goalX) + abs(y - goalY)
        return distance

    def linearConflicts(self, state):
        distance = self.manhattan(state)
        count = 0
        n = len(state.table)
        goal = list(range(1, n))
        goal.append(0)
        dimension = int(math.sqrt(n))
        for i in range(dimension):
            row = []
            column = []
            goalRow = []
            goalColumn = []
            for j in range(dimension - 1):
                for k in range(j + 1, dimension):
                    row.append((state.table[i * dimension + j], state.table[i * dimension + k]))
                    goalRow.append((goal[i * dimension + j], goal[i * dimension + k]))
                    column.append((state.table[j * dimension + i], state.table[k * dimension + i]))
                    goalColumn.append((goal[j * dimension + i], goal[k * dimension + i]))
            for j in range(len(row)):
                for k in range(len(row)):
                    if row[j][0] != 0 and row[j][1] != 0 and goalRow[k][0] != 0 and goalRow[k][1] != 0:
                        if row[j][0] == goalRow[k][1] and row[j][1] == goalRow[k][0]:
                            count += 1
                    if column[j][0] != 0 and column[j][1] != 0 and goalColumn[k][0] != 0 and goalColumn[k][1] != 0:
                        if column[j][0] == goalColumn[k][1] and column[j][1] == goalColumn[k][0]:
                            count += 1
        return distance + 2 * count

    def disjointDatabases(self, state):
        # TODO the following variables(tiles) must be the same of the DBLoader module
        tiles1 = {1, 5, 9, 13, 2}
        tiles2 = {6, 10, 14, 3, 7}
        tiles3 = {11, 15, 4, 8, 12}

        value1 = self.getValueFromDB(state, tiles1, self.db1)
        value2 = self.getValueFromDB(state, tiles2, self.db2)
        value3 = self.getValueFromDB(state, tiles3, self.db3)
        return value1 + value2 + value3

    def disjointAndReflected(self, state):
        # TODO the following variables(tiles) must be the same of the DBLoader module
        tiles4 = {1, 2, 3, 4, 5}
        tiles5 = {6, 7, 8, 9, 10}
        tiles6 = {11, 12, 13, 14, 15}

        firstValue = self.disjointDatabases(state)
        value4 = self.getValueFromDB(state, tiles4, self.db4)
        value5 = self.getValueFromDB(state, tiles5, self.db5)
        value6 = self.getValueFromDB(state, tiles6, self.db6)
        secondValue = value4 + value5 + value6
        if firstValue < secondValue:
            return secondValue
        return firstValue