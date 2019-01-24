from Node import Node
from Frontier import AStarFrontier
from timeit import default_timer as timer
import math


class AStarSolver:
    def __init__(self, heuristics='None'):
        self.heuristics = heuristics
        self.problems = []
        self.problemsDB = []

    def Solve(self, problem):
        self.problems = []
        for i in range(len(self.heuristics)):
            problem.SetHeuristic(self.heuristics[i])
            self.problems.append(AStar(problem))

    def MemoizeSolutions(self):
        self.problemsDB.append(self.problems)

    def SensitiveData(self):
        value = []
        nodes = []
        seconds = []
        allSolution = []
        for j in range(len(self.heuristics)):
            value.append(0)
            nodes.append(0)
            seconds.append(0)
            allSolution.append(0)
        for j in range(len(self.heuristics)):
            for i in range(len(self.problemsDB)):
                value[j] += self.problemsDB[i][j][0].value
                nodes[j] += self.problemsDB[i][j][0].numNodes
                seconds[j] += self.problemsDB[i][j][0].time
                allSolution[j] += self.problemsDB[i][j][-1].numNodes
            value[j] /= len(self.problemsDB)
            nodes[j] /= len(self.problemsDB)
            seconds[j] /= len(self.problemsDB)
            allSolution[j] /= len(self.problemsDB)
            print('Heuristic: ' + self.heuristics[j])
            print('Value: ' + str(value[j]))
            print('Nodes: ' + str(nodes[j]))
            print('Nodes/Sec: ' + str(nodes[j] / seconds[j]))
            print('Seconds: ' + str(seconds[j]))
            print('All Solutions: ' + str(allSolution[j]))
            print()
            print('==========================================================')

    def PrintSolutions(self):
        print('Initial State:')
        self.problems[0][0].problem.initialState.Print()
        print()
        for i in range(len(self.heuristics)):
            print('Heuristic: ' + self.heuristics[i])
            print('Value: ' + str(self.problems[i][0].value))
            print('Seconds: ' + str(self.problems[i][0].time))
            print('Nodes generated: ' + str(self.problems[i][0].numNodes))
            print(str(len(self.problems[i][0].sequence)) + ' Actions:')
            print(self.problems[i][0].sequence)
            print()
        print('===============================================')


class Solution:
    def __init__(self, sequence, time, numNodes, problem):
        self.problem = problem
        self.value = problem.Heuristic(problem.initialState)
        self.sequence = sequence
        self.time = time
        self.numNodes = numNodes


def AStar(problem):
    #    maxDepth=0
    goalDepth = math.inf
    solutions = []
    time = 0
    solutionFlag = False
    start = timer()
    frontier = AStarFrontier()
    explored = {}
    n = Node(problem.initialState)
    frontier.Push(n, problem.GetKey(n.state), problem.Heuristic(n.state) + n.pathCost)
    while frontier.dim != 0:
        n = frontier.Pop()
        if problem.GoalTest(n.state) and solutionFlag == False:
            end = timer()
            solutionFlag = True
            sequence = n.Solution()
            solutions.append(Solution(sequence, end - start, len(explored) + frontier.dim + 1, problem))
            time += end - start
            goalDepth = n.depth
            start = timer()
        if not problem.GoalTest(n.state):
            explored[problem.GetKey(n.state)] = n.state  # non devo inserirci il goal
        if n.depth < goalDepth:
            for a in problem.Actions(n.state):
                # se child è un goal va messo nella lista dopo che solutionflag diventa True
                child = n.Child(problem, a)
                if problem.GoalTest(child.state) and solutionFlag == True:
                    end = timer()
                    time += end - start
                    sequence = child.Solution()
                    solutions.append(
                        Solution(sequence, time, len(explored) + frontier.dim + len(solutions) + 1, problem))
                    start = timer()
                elif problem.GetKey(child.state) not in explored and not frontier.Search(problem.GetKey(child.state)):
                    frontier.Push(child, problem.GetKey(child.state), problem.Heuristic(child.state) + child.pathCost)
                else:
                    # se in frontiera ci sta un'altro nodo con lo stato di child
                    if frontier.Search(problem.GetKey(child.state)):
                        # valuta se scambiare child con quel nodo
                        frontier.Fixup(child, problem.GetKey(child.state),
                                       problem.Heuristic(child.state) + child.pathCost)
    if solutionFlag == False:
        end = timer()
        solutions.append(Solution(None, end - start, len(explored), problem))
        return solutions  # failure
    else:
        return solutions
