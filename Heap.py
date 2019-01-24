import math


def Left(i):
    return (i << 1) + 1


def Right(i):
    return (i + 1) << 1


def Parent(i):
    return (i - 1) >> 1


class Element:
    def __init__(self, node, priority):
        self.node = node
        self.priority = priority


class MinHeap:
    def __init__(self):
        self.Heap = []
        self.HeapSize = 0

    def MinHeapify(self, i, d):
        def _MinHeapify(i, d):
            l = Left(i)
            r = Right(i)
            if l <= self.HeapSize and self.Heap[l].priority < self.Heap[i].priority:
                min = l
            else:
                min = i
            if r <= self.HeapSize and self.Heap[r].priority < self.Heap[min].priority:
                min = r
            if min != i:
                d[self.Heap[min].node[1]] = i
                tmp = self.Heap[min]
                self.Heap[min] = self.Heap[i]
                self.Heap[i] = tmp
                _MinHeapify(min, d)
            else:
                d[self.Heap[i].node[1]] = i

        _MinHeapify(i, d)

    def Min(self):
        return self.Heap[0].node

    def Pop(self):
        if self.HeapSize < 1:
            return None
        d = {}
        min = self.Heap[0]
        self.Heap[0] = self.Heap[self.HeapSize - 1]
        self.HeapSize = self.HeapSize - 1
        self.MinHeapify(0, d)
        return (min.node, d)

    def DecreasePriority(self, i, priority):
        d = {}
        if priority <= self.Heap[i].priority:
            self.Heap[i].priority = priority
            while i > 0 and self.Heap[Parent(i)].priority > self.Heap[i].priority:
                d[self.Heap[Parent(i)].node[1]] = i
                tmp = self.Heap[i]
                self.Heap[i] = self.Heap[Parent(i)]
                self.Heap[Parent(i)] = tmp
                i = Parent(i)
        d[self.Heap[i].node[1]] = i
        return d

    def Push(self, node, priority):
        e = Element(node, priority)
        e.priority = math.inf
        if self.HeapSize == len(self.Heap):
            self.Heap.append(e)
        else:
            self.Heap[self.HeapSize] = e
        self.HeapSize = self.HeapSize + 1
        return self.DecreasePriority(self.HeapSize - 1, priority)
