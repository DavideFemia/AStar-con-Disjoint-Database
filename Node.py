
class Node:
    def __init__(self, state, key, priority):
        self.state = state
        self.key = key
        self.priority = priority
        self.parent = None
        self.action = None
        self.pathCost = 0

    def child(self, problem, action):
        state = problem.result(self.state, action)
        key = state.__str__()
        g = self.pathCost + problem.stepCost(self.state, action, state)
        priority = g + problem.heuristic(state)
        child = Node(state, key, priority)
        child.parent = self
        child.action = action
        child.pathCost = g
        return child

    def solution(self):
        solution = []
        node = self
        while node.parent != None:
            solution.insert(0,node.action)
            node = node.parent
        return solution
