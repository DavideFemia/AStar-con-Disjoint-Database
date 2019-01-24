import pickle
from Node import Node
from Frontier import AStarFrontier
from TilesProblem import ReverseProblem, TilesProblem
from timeit import default_timer as timer


def CreateDB(problem):  # ricerca su grafo ottima verso tutti gli stati possibili a partire dallo stato goal
    maxDepth = 0
    time = 0
    start = timer()
    n = Node(problem.initialState)
    frontier = AStarFrontier()
    frontier.Push(n, problem.GetKey(n.state), n.pathCost)
    explored = {}
    while frontier.dim != 0:
        node = frontier.Pop()
        end = timer()
        time += end - start
        if time > 1800:
            print(str(frontier.dim) + ' nodes in frontier')
            time = 0
        start = timer()
        if node.depth > maxDepth:
            maxDepth += 1
            print('Reached Depth: ' + str(maxDepth))
        problem.db[problem.GetKey(node.state)] = node.pathCost
        explored[problem.GetKey(node.state)] = node.state
        for a in problem.Actions(node.state):
            child = node.Child(problem, a)
            if problem.GetKey(child.state) not in explored and not frontier.Search(problem.GetKey(child.state)):
                frontier.Push(child, problem.GetKey(child.state), child.pathCost)
            else:
                # se in frontiera ci sta un'altro nodo con lo stato di child
                if frontier.Search(problem.GetKey(child.state)):
                    # valuta se scambiare child con quel nodo
                    frontier.Fixup(child, problem.GetKey(child.state), child.pathCost)


tiles1 = {1, 2, 3, 4}
tiles2 = {5, 6, 7, 8}
tiles3 = {2, 5, 7, 8}
tiles4 = {1, 3, 4, 6}

problem1 = ReverseProblem(TilesProblem(), tiles1)
CreateDB(problem1)
pickle.dump(problem1.db, open('DB1.txt', 'wb'))
print('=====================DB1 Loaded!!!=============================')

problem2 = ReverseProblem(TilesProblem(), tiles2)
CreateDB(problem2)
pickle.dump(problem2.db, open('DB2.txt', 'wb'))
print('=====================DB2 Loaded!!!=============================')

problem3 = ReverseProblem(TilesProblem(), tiles3)
CreateDB(problem3)
pickle.dump(problem3.db, open('DB3.txt', 'wb'))
print('=====================DB3 Loaded!!!=============================')

problem4 = ReverseProblem(TilesProblem(), tiles4)
CreateDB(problem4)
pickle.dump(problem4.db, open('DB4.txt', 'wb'))
print('=====================DB4 Loaded!!!=============================')
