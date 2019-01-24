import math
import random
import pickle


class State:
    def __init__(self, A):
        self.n = len(A)
        self.dim = int(math.sqrt(self.n))
        self.tiles = self.n
        self.pos = {}
        self.table = {}
        for i in range(len(A)):
            if A[i] != len(A):
                self.pos[A[i]] = i
                self.table[i] = A[i]

    def __copy__(self):
        state = State(self.Array())
        state.tiles = self.tiles
        return state

    def Array(self):
        A = []
        for i in range(self.n):
            if i in self.table:
                A.append(self.table[i])
            else:
                A.append(self.n)
        return A

    def GetRows(self):
        rows = []
        A = self.Array()
        for i in range(self.dim):
            rows.append(A[self.dim * i:self.dim * i + self.dim])
        return rows

    def GetColumns(self):
        columns = []
        A = self.Array()
        for i in range(self.dim):
            column = []
            for j in range(self.dim):
                column.append(A[i + j * self.dim])
            columns.append(column.copy())
        return columns

    def Serialization(self):
        s = ''
        for i in range(self.dim):
            for j in range(self.dim):
                pos = self.dim * i + j
                if pos in self.table:
                    value = self.table[pos]
                    s += str(value) + ','
                else:
                    s += '*,'
        return s[:-1]

    def Print(self):
        for i in range(self.dim):
            s = '|'
            for j in range(self.dim):
                pos = self.dim * i + j
                if pos in self.table:
                    value = self.table[pos]
                    if value == 0:
                        s += '  |'
                    elif value // 10 == 0:
                        s += ' ' + str(value) + '|'
                    else:
                        s += str(value) + '|'
                else:
                    s += ' *|'
            print(s)

    def Project(self, tiles):  # tiles è un insieme di celle(quelle che voglio tenere nello stato parziale)
        state = self.__copy__()
        for i in range(1, self.n):
            if i not in tiles:
                pos = state.pos[i]
                del state.table[pos]
                del state.pos[i]
                state.tiles = state.tiles - 1
        return state

    def FringeTiles(self):
        s = ''
        for i in range(self.dim):
            for j in range(self.dim):
                pos = self.dim * i + j
                if pos in self.table:
                    value = self.table[pos]
                    if value != 0:
                        s += str(value) + ','
                    else:
                        s += '*,'
                else:
                    s += '*,'
        return s[:-1]


def abs(x):
    if x >= 0:
        return x
    return -1 * x


def GetCouple(A):
    n = len(A)
    couples = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            couple = []
            couple.append(A[i])
            couple.append(A[j])
            couples.append(couple.copy())
    return couples


def ManhattanDistance(state, problem):
    #    n = problem.numTiles + 1
    #    d = math.ceil(math.sqrt(n))
    n = state.n
    d = state.dim
    distance = 0
    for i in range(1, n):
        posg = problem.goal.pos[i]
        x = posg // d
        y = posg - x * d
        pos = state.pos[i]
        posx = pos // d
        posy = pos - d * posx
        distance = distance + abs(x - posx) + abs(y - posy)
    return distance


def LinearConflicts(state, problem):
    def _Conflict(A, B):
        count = 0
        ACouples = GetCouple(A)
        BCouples = GetCouple(B)
        for i in range(len(ACouples)):
            for j in range(len(BCouples)):
                if ACouples[i][0] == BCouples[j][1] and ACouples[i][1] == BCouples[j][0]:  # togliere le coppie con zeri
                    if ACouples[i][0] != 0 and ACouples[i][1] != 0:
                        count += 1
        return (count)

    value = ManhattanDistance(state, problem)
    goalRows = problem.goal.GetRows()
    goalColumns = problem.goal.GetColumns()
    rows = state.GetRows()
    columns = state.GetColumns()
    count = 0
    for i in range(len(rows)):
        count += _Conflict(rows[i], goalRows[i])
        count += _Conflict(columns[i], goalColumns[i])
    return value + count * 2


def DisjointPatternDatabases(state, problem):
    s1 = state.Project({1, 2, 3, 4}).Serialization()
    s2 = state.Project({5, 6, 7, 8}).Serialization()
    value1 = problem.db1[s1]
    value2 = problem.db2[s2]
    return value1 + value2


def DisjointAndReflected(state, problem):
    max = DisjointPatternDatabases(state, problem)
    s3 = state.Project({2, 5, 7, 8}).Serialization()
    s4 = state.Project({1, 3, 4, 6}).Serialization()
    value = problem.db3[s3] + problem.db4[s4]
    if max < value:
        max = value
    return max


class TilesProblem:
    def __init__(self, scrambles=100, goal=list(range(9))):
        self.scrambles = scrambles
        self.numTiles = len(goal) - 1
        self.actions = {'up', 'down', 'left', 'right'}
        self.goal = State(goal)
        self.LoadDatabases()  # TODO commentare questa riga prima dell'esecuzione di DBLoader nel caso si voglia riprodurre i database

    def __copy__(self):
        return TilesProblem(self.scrambles, self.goal.Array())

    def LoadDatabases(self):
        self.db1 = pickle.load(open('DB1.txt', 'rb'))
        self.db2 = pickle.load(open('DB2.txt', 'rb'))
        self.db3 = pickle.load(open('DB3.txt', 'rb'))
        self.db4 = pickle.load(open('DB4.txt', 'rb'))

    def GetInstance(self, state):
        self.initialState = State(state)

    def SetHeuristic(self, heuristic):
        self.heuristic = heuristic

    def RandomState(self):
        state = self.goal.__copy__()
        actions = []
        for a in self.actions:
            actions.append(a)
        for i in range(self.scrambles):
            j = random.randrange(0, len(actions))
            a = actions[j]
            if a in self.Actions(state):
                state = self.Result(state, a)
        return state.Array()

    def GetKey(self, state):
        return state.Serialization()

    def Heuristic(self, state):
        if self.heuristic == 'Manhattan':
            return ManhattanDistance(state, self)
        if self.heuristic == 'Linear Conflicts':
            return LinearConflicts(state, self)
        if self.heuristic == 'Disjoint Pattern Databases':
            return DisjointPatternDatabases(state, self)
        if self.heuristic == 'Disjoint + Reflected':
            return DisjointAndReflected(state, self)
        if self.heuristic == 'None':
            return 0

    def Actions(self, state):
        actions = self.actions.copy()
        d = math.ceil(math.sqrt(self.numTiles + 1))
        pos = state.pos[0]
        x = pos // d
        y = pos - d * x
        if (x == 0):
            actions.remove('up')
        if (y == 0):
            actions.remove('left')
        if (x == d - 1):
            actions.remove('down')
        if (y == d - 1):
            actions.remove('right')
        return actions

    def Result(self, s, action):
        state = s.__copy__()
        d = math.ceil(math.sqrt(self.numTiles + 1))
        pos = state.pos[0]
        tile = 0
        move = 0
        occuped = False
        if action == 'up':
            move = -1 * d
        if action == 'down':
            move = d
        if action == 'left':
            move = -1
        if action == 'right':
            move = 1
        if pos + move in state.table:
            tile = state.table[pos + move]
            occuped = True
        state.pos[0] = pos + move
        state.table[pos + move] = 0
        if occuped:
            state.pos[tile] = pos
            state.table[pos] = tile
        else:
            del state.pos[tile]
            del state.table[pos]
        return state

    def GoalTest(self, state):
        s = state.Array()
        sGoal = self.goal.Array()
        for i in range(len(s)):
            if s[i] != sGoal[i]:
                return False
        return True

    def Cost(self, state, action, newState):
        return 1


class ReverseProblem:
    def __init__(self, problem, tiles):
        self.problem = problem
        self.initialState = problem.goal.Project(tiles)
        self.db = {}

    def Actions(self, state):
        return self.problem.Actions(state)

    def Result(self, s, action):
        return self.problem.Result(s, action)

    def Cost(self, state, action, newState):
        if newState.FringeTiles() == state.FringeTiles():
            return 0
        else:
            return 1

    def GetKey(self, state):
        return state.Serialization()
