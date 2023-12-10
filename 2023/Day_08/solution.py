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

    def getAAA(self):
        return self.nodes['AAA'][0]


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

def navigate(node, navigator):
    n = node
    while n.name != 'ZZZ':
        if navigator.getNextStep() == 'L':
            n = n.left
        else:
            n = n.right
    
    return navigator.stepCount

if __name__ == "__main__":
    navigator, nodeMapBuilder = readData(sys.argv[1])
    nodeMapBuilder.connectNodes()
    aaaNode = nodeMapBuilder.getAAA()    
    print(navigate(aaaNode, navigator))