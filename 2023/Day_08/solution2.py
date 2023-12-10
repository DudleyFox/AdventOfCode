import sys


class Navigator:
    def __init__(self, input):
        self.stepCount = 0
        self.directions = input
        self.length = len(input)

    def getNextStep(self):
        index = self.stepCount % self.length
        self.stepCount += 1
        return self.directions[index]
    
class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def addLeft(self, left):
        self.left = left

    def addRight(self, right):
        self.right = right

class NodeMapBuilder:
    def __init__(self):
        self.nodes = {}

    def addNode(self, nodeData):
        print(nodeData)
        name, left, right = nodeData
        self.nodes[name] = (Node(name), nodeData)

    def connectNodes(self):
        # print(self.nodes)
        for node, nodeData in self.nodes.values():
            name, left, right = nodeData
            node.addLeft(self.nodes[left][0])
            node.addRight(self.nodes[right][0])

    def getStartingNodes(self):
        nodes = []
        for x in self.nodes.keys():
            if x[-1:] == 'A':
                nodes.append(self.nodes[x][0])
        return nodes


def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            if l != '':
                yield l

def readData(fileName):
    first = True
    navigator = 0
    nodeMapBuilder = NodeMapBuilder()
    for x in readLines(fileName):
        if first:
            navigator = Navigator(x)
            first = False
        else:
            nodeData = tuple(x.replace('(','').replace(')','').replace(',','=').replace(' ','').split('='))
            nodeMapBuilder.addNode(nodeData)
    return navigator, nodeMapBuilder

def notAtEnd(nodes):
    for x in nodes:
        if x.name[-1:] != 'Z':
            return True
    return False

def navigate(nodes, navigator):
    ns = [n for n in nodes]
    while notAtEnd(ns):
        if navigator.getNextStep() == 'L':
            ns = [n.left for n in ns]
        else:
            ns = [n.right for n in ns]
        if navigator.stepCount % 10000000 == 0 or ns[5].name[2] == 'Z':
            print(navigator.stepCount)
            names = [x.name for x in ns]
            print(", ".join(names))

    
    
    return navigator.stepCount

if __name__ == "__main__":
    navigator, nodeMapBuilder = readData(sys.argv[1])
    nodeMapBuilder.connectNodes()
    nodes = nodeMapBuilder.getStartingNodes()
    for x in nodes:
        print(x.name)    
    print(navigate(nodes, navigator))