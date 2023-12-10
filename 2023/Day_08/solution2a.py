import sys


class Navigator:
    def __init__(self, input):
        self.stepCount = 0
        self.directions = input
        self.length = len(input)
        self.marks = []

    def getNextStep(self):
        index = self.stepCount % self.length
        self.stepCount += 1
        return self.directions[index]
    
    def addNode(self, node):
        self.node = node

    def getNodeName(self):
        return self.node.name
    
    def tick(self):
        s = self.getNextStep()
        if s == 'L':
            self.node = self.node.left
        else:
            self.node = self.node.right
        
    def mark(self):
        if (len(self.marks)) < 2:
            self.marks.append(self.stepCount)

    def getMarks(self):
        return self.marks
    
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

def notAtEnd(navs):
    for x in navs:
        if len(x.getMarks()) < 2:
            return True
    return False

def navigate(navigators):
    navs = [n for n in navigators]
    
    while notAtEnd(navs):
        for n in navs:
            n.tick()
            if n.getNodeName()[-1:] == 'Z':
                n.mark()

    for x in navs:
        first, second = tuple(x.getMarks())
        print(f'{first}, {second}, {second//first}')

    return navs

def notLeast(pairs):
    numbers = [x[0] for x in pairs]
    last = numbers[0]
    for x in numbers:
        if last != x:
            return True
        last = x
    return False

def findLeastCommonMultiple(numbers):
    pairs = [ (x,x) for x in numbers]
    while notLeast(pairs):
        pairs.sort(key=lambda x: x[0])
        selected = pairs[0]
        selected = (selected[0] + selected[1], selected[1])
        pairs[0] = selected

    for x in pairs:
        print(x)
    
    

if __name__ == "__main__":
    navigator, nodeMapBuilder = readData(sys.argv[1])
    nodeMapBuilder.connectNodes()
    nodes = nodeMapBuilder.getStartingNodes()
    navigators = []
    for x in nodes:
        print(x.name)
        navigator = Navigator(navigator.directions)
        navigator.addNode(x)
        navigators.append(navigator)
    
    navs = navigate(navigators)
    cycleTimes = [x.getMarks()[0] for x in navs]
    product = 1
    for x in cycleTimes:
        product *= x
    print (product)
    findLeastCommonMultiple(cycleTimes)

# 47 281
# 71 281
# 53 281
# 43 281
# 73 281
# 79 281