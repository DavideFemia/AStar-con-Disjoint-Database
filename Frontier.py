import sys

def left(i):
    return (i << 1) + 1

def right(i):
    return (i + 1) << 1

def parent(i):
    return (i - 1) >> 1

#TODO the elements stored in frontier MUST have a key and a priority attribute!
class AStarFrontier:
    def __init__(self):
        self.handle = {}
        self.heap = []
        self.size = 0

    def minHeapify(self,i):
        size = len(self.heap)-1
        l = left(i)
        r = right(i)
        if l <= size and self.heap[l].priority < self.heap[i].priority:
            min = l
        else:
            min = i
        if r <= size and self.heap[r].priority < self.heap[min].priority:
            min = r
        if min != i:
            self.handle[self.heap[min].key] = i
            self.handle[self.heap[i].key] = min
            tmp = self.heap[i]
            self.heap[i] = self.heap[min]
            self.heap[min] = tmp
            self.minHeapify(min)

    def pop(self):
        if len(self.heap) > 1:
            min = self.heap[0]
            self.heap[0] = self.heap.pop()
            self.handle[self.heap[0].key] = 0
            del self.handle[min.key]
            self.minHeapify(0)
        else:
            min = self.heap.pop()
            del self.handle[min.key]
        self.size -= 1
        return min

    def decreasePriority(self, i, priority):
        if priority <= self.heap[i].priority:
            self.heap[i].priority = priority
            while i > 0 and self.heap[parent(i)].priority > self.heap[i].priority:
                self.handle[self.heap[i].key] = parent(i)
                self.handle[self.heap[parent(i)].key] = i
                tmp = self.heap[parent(i)]
                self.heap[parent(i)] = self.heap[i]
                self.heap[i] = tmp
                i = parent(i)

    def push(self, node):
        priority = node.priority
        node.priority = sys.maxsize
        size = len(self.heap)
        self.handle[node.key] = size
        self.heap.append(node)
        self.decreasePriority(size, priority)
        self.size += 1

    def search(self, node):
        return node.key in self.handle

    def isBetter(self, node):
        if node.key in self.handle:
            return node.priority < self.heap[self.handle[node.key]].priority
        return False

    def fixup(self,node):
        pos = self.handle[node.key]
        priority = node.priority
        node.priority = sys.maxsize
        self.heap[pos] = node
        self.decreasePriority(pos, priority)