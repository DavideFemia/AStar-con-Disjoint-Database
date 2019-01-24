from Heap import MinHeap


class AStarFrontier:
    def __init__(self):
        self.d = {}
        self.priorityQueue = MinHeap()
        self.dim = 0

    # da qui in avanti per list intendo un dizionario con chiave le configurazioni che sono state cambiate di posizione nell'Heap dai metodi Push o da Pop

    def Push(self, element, key, priority):
        list = self.priorityQueue.Push((element, key), priority)
        for keys in list:
            self.d[keys] = list[keys]
        self.dim += 1

    def Pop(self):
        elementWrapper = self.priorityQueue.Pop()  # ((node,key),list)
        list = elementWrapper[1]
        for keys in list:
            self.d[keys] = list[keys]
        element = elementWrapper[0]  # element è un node wrapper
        del self.d[element[1]]
        self.dim -= 1
        return element[0]

    def Search(self, key):
        return key in self.d

    def Fixup(self, node, key, priority):
        pos = self.d[key]
        redundantPriority = self.priorityQueue.Heap[pos].priority
        if redundantPriority > priority:
            self.priorityQueue.Heap[pos].node = (node, key)
            list = self.priorityQueue.DecreasePriority(pos, priority)  # cambia la priorità
            for keys in list:
                self.d[keys] = list[keys]
