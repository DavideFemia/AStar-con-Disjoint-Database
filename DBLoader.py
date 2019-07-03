from timeit import default_timer as timer
import pickle
from Node import Node
from Frontier import AStarFrontier
from SubProblem import SubProblem

def generateDB(problem):
    node = Node(problem.initialState, str(problem.initialState), 0)
    frontier = AStarFrontier()
    frontier.push(node)
    db = {}
    while frontier.size != 0:
        node = frontier.pop()
        db[node.key] = node.pathCost
        for action in problem.actions(node.state):
            child = node.child(problem, action)
            if not (child.key in db) and not (frontier.search(child)):
                frontier.push(child)
            elif frontier.isBetter(child):
                frontier.fixup(child)
    return db


n = 16

#TODO define here a partition of a (n-1)-tiles problem!
#TODO if you change these values make sure to change also the variables in the function disjointDatabase of the TilesProblem module
tiles1 = {1, 5, 9, 13, 2}
tiles2 = {6, 10, 14, 3, 7}
tiles3 = {11, 15, 4, 8, 12}

#TODO define here a partition of a (n-1)-tiles problem!
#TODO if you change these values make sure to change also the variables in the function disjointAndReflected of the TilesProblem module
tiles4 = {1, 2, 3, 4, 5}
tiles5 = {6, 7, 8, 9, 10}
tiles6 = {11, 12, 13, 14, 15}

problem = SubProblem(n, tiles1)
print('DB1 Generation:')
print('Tiles: '+str(tiles1))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB1.txt', 'wb'))
print('==============================DB1 LOADED!!=============================')
print()

problem = SubProblem(n, tiles2)
print('DB2 Generation:')
print('Tiles: '+str(tiles2))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB2.txt', 'wb'))
print('==============================DB2 LOADED!!=============================')
print()

problem = SubProblem(n, tiles3)
print('DB3 Generation:')
print('Tiles: '+str(tiles3))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB3.txt', 'wb'))
print('==============================DB3 LOADED!!=============================')
print()

problem = SubProblem(n, tiles4)
print('DB4 Generation:')
print('Tiles: '+str(tiles4))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB4.txt', 'wb'))
print('==============================DB4 LOADED!!=============================')

problem = SubProblem(n, tiles5)
print('DB5 Generation:')
print('Tiles: '+str(tiles5))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB5.txt', 'wb'))
print('==============================DB5 LOADED!!=============================')

problem = SubProblem(n, tiles6)
print('DB6 Generation:')
print('Tiles: '+str(tiles6))
db = generateDB(problem)
pickle.dump(db, open('DB-15Tiles\\DB6.txt', 'wb'))
print('==============================DB6 LOADED!!=============================')
