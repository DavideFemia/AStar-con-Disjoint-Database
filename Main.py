from TilesProblem import TilesProblem
from Solvers import RandomAStarSolver, AStarSolver

n = 16  # TODO substitute n with the length of the table(9 for 8-tiles problem for example)

problem = TilesProblem(n)
randomSolver = RandomAStarSolver(problem, ['manhattan', 'linearConflicts', 'disjointDatabases', 'disjointAndReflected'])
for i in range(500):
    randomSolver.solveRandomProblem()
randomSolver.getResults()


# TODO uncomment the following row to test on a specific initial state of 15-tiles problem
# solver = AStarSolver(problem, ['manhattan', 'linearConflicts', 'disjointDatabases'])
# solver.solveProblem([1, 10, 7, 3, 5, 6, 4, 8, 13, 11, 12, 15, 14, 0, 9, 2])
