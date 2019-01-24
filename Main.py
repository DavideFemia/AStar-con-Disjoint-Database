from Solvers import AStarSolver
from TilesProblem import TilesProblem

# senza argomenti non usa nessuna euristica(ricerca costo uniforme)
solver = AStarSolver(['Manhattan', 'Linear Conflicts', 'Disjoint Pattern Databases', 'Disjoint + Reflected'])
problem = TilesProblem(100)
for i in range(100):
    problem.GetInstance(problem.RandomState())
    solver.Solve(problem)
    solver.PrintSolutions()  # TODO commentare questa riga se non si vuole vedere i risultati delle singole istanze
    solver.MemoizeSolutions()
solver.SensitiveData()
