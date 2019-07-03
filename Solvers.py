from timeit import default_timer as timer
from Node import Node
from Frontier import AStarFrontier

class RandomAStarSolver:
    def __init__(self, problem, heuristics=['uniformCost']):
        self.heuristics = heuristics
        self.problem = problem
        self.values = []  #ogni elemento indica il valore delle euristiche sullo stato iniziale di un problema risolto
        self.nodes = []
        self.seconds = []

    def solveRandomProblem(self):
        self.values.append([])
        self.nodes.append([])
        self.seconds.append([])
        self.problem.setInitialState(self.problem.randomTable())
        print('INITIAL STATE:')
        print(str(self.problem.initialState))
        for i in range(len(self.heuristics)):
            self.problem.setHeuristic(self.heuristics[i])
            print()
            print('HEURISTIC '+str(i)+':')
            sequence = self.AStar()
            print('Moves: '+str(len(sequence)))
            print(sequence)
        print('=====================')


    def AStar(self):
        start = timer()
        initialHeuristic = self.problem.heuristic(self.problem.initialState)
        node = Node(self.problem.initialState, str(self.problem.initialState), initialHeuristic)
        frontier = AStarFrontier()
        frontier.push(node)
        explored = set()
        while frontier.size != 0:
            node = frontier.pop()
            if self.problem.goalTest(node.state):
                end = timer()
                print('Value: '+str(initialHeuristic))
                print('Seconds: '+str(end-start))
                length = len(self.values) - 1
                self.values[length].append(initialHeuristic)
                self.nodes[length].append(frontier.size+len(explored)+1)
                self.seconds[length].append(end-start)
                return node.solution()
            explored.add(node.key)
            for action in self.problem.actions(node.state):
                child = node.child(self.problem, action)
                if not (child.key in explored) and not (frontier.search(child)):
                    frontier.push(child)
                elif frontier.isBetter(child):
                    frontier.fixup(child)

    def getResults(self):
        numProblems = len(self.values)
        numHeuristics = len(self.heuristics)
        values=list()
        nodes=list()
        seconds=list()
        for i in range(numHeuristics):
            values.append(0)
            nodes.append(0)
            seconds.append(0)
        for i in range(numProblems):
            for j in range(numHeuristics):
                values[j] += self.values[i][j]
                nodes[j] += self.nodes[i][j]
                seconds[j] += self.seconds[i][j]
        for i in range(numHeuristics):
            values[i] /= numProblems
            nodes[i] /= numProblems
            seconds[i] /= numProblems
            print()
            print('HEURISTIC '+str(i)+':')
            print()
            print('value: '+str(values[i]))
            print('nodes: '+str(nodes[i]))
            print('nodes/sec: '+str(nodes[i]/seconds[i]))
            print('seconds: '+str(seconds[i]))
            print()
            print('================================================')


class AStarSolver:
    def __init__(self, problem, heuristics=['uniformCost']):
        self.heuristics = heuristics
        self.problem = problem

    def solveProblem(self, table):
        self.problem.setInitialState(table)
        print('INITIAL STATE:')
        print(str(self.problem.initialState))
        for i in range(len(self.heuristics)):
            self.problem.setHeuristic(self.heuristics[i])
            print()
            print('HEURISTIC '+str(i)+':')
            sequence = self.AStar()
            print('Moves: '+str(len(sequence)))
            print(sequence)
        print('=====================')

    def AStar(self):
        start = timer()
        initialHeuristic = self.problem.heuristic(self.problem.initialState)
        node = Node(self.problem.initialState, str(self.problem.initialState), initialHeuristic)
        frontier = AStarFrontier()
        frontier.push(node)
        explored = set()
        while frontier.size != 0:
            node = frontier.pop()
            if self.problem.goalTest(node.state):
                end = timer()
                print('Value: '+str(initialHeuristic))
                print('Seconds: '+str(end-start))
                return node.solution()
            explored.add(node.key)
            for action in self.problem.actions(node.state):
                child = node.child(self.problem, action)
                if not (child.key in explored) and not (frontier.search(child)):
                    frontier.push(child)
                elif frontier.isBetter(child):
                    frontier.fixup(child)
