class Node:
    def __init__(self, state):
        self.state = state.__copy__()
        self.action = None
        self.parent = None
        self.depth=0
        self.pathCost = 0

    def Solution(self):
        actionSequence = []
        x = self
        while x.parent is not None:
            actionSequence.insert(0, x.action)
            x = x.parent
        return actionSequence

    def Child(self, problem, action):
        child = Node(problem.Result(self.state, action))
        child.parent = self
        child.depth=self.depth+1
        child.action = action
        child.pathCost = self.pathCost + problem.Cost(self.state, action, child.state)
        return child