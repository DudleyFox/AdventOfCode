# 3898 too low
# 5197 wrong
# 5041 wrong
def readPairs():
    lines = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            t = l.strip()
            if t:
                lines.append(t)
    length = len(lines)
    index = 1
    for x in range(0, length, 2):
        left = eval(lines[x])
        right = eval(lines[x+1])
        yield (index, left, right)
        index += 1

isInt = lambda x : type(x) is int

def buildChild(parent, node):
    if isInt(node):
        return TreeNode(parent, 'leaf', node, [])
    if type(node) is list:
        return TreeNode(parent, 'branch', None, node)

class TreeNode:
    def __init__ (self, parent, nodeType, nodeValue, children):
        self.parent = parent
        self.type = nodeType
        self.value = nodeValue
        self.children = []
        for child in children:
            self.children.append(buildChild(self, child))
        self.visited = False
        self.firstVisit = True

    def __str__(self):
        s = ''
        s += f'Node:\n'
        s += f'\tType: {self.type}\n'
        s += f'\tValue: {self.value}\n'
        return s


def getNext(node):
    if not node:
        return node
    print(node)
    if node.type == 'branch':
        if node.firstVisit:
            node.firstVisit = False
            return node
        for child in node.children:
            if not child.visited:
                return getNext(child)
        node.visited = True
        return node.parent
    if node.type == 'leaf':
        node.visited = True
        return node


def compareInts(l,r):
    print('ints:', l,r)
    if l < r:
        return ('valid', l, r)
    elif l > r:
        return ('invalid', l, r)
    return ('unknown', l, r)



def compare(tup, depth):
    status, l, r = tup
    leftTree = TreeNode(None, 'branch', None, l)
    rightTree = TreeNode(None, 'branch', None, r)
    while True:
        lnode = getNext(leftTree)
        rnode = getNext(rightTree)
        if lnode and not rnode: # right side ran out first
            print('No more elements from right')
            return ('invalid', l, r)
        if not lnode: # left side ran out first
            return ('valid', l, r)
        if lnode.type == 'branch' and rnode.type == 'branch':
            continue
        if lnode.type == 'leaf' and rnode.type == 'branch':
            while rnode.type == 'branch':
                rnode = getNext(rightTree)
                if not rnode:
                    print('No more elements from right tree')
                    return ('invalid',l,r)

        if lnode.type == 'branch' and rnode.type == 'leaf':
            while lnode.type == 'branch':
                lnode = getNext(leftTree)
                if not lnode:
                    return ('valid',l,r)

        result = compareInts(lnode.value, rnode.value)
        if result[0] != 'unknown':
            return result
        
   
    
    
sum = 0
if __name__ == '__main__':
    for i,l,r in readPairs():
        result = compare(('',l,r), 0)
        print(f'lists:\n\t{l}\n\t{r}')
        print(i, result, l,r)
        if result[0] == 'valid' or result[0] == 'unknown':
            sum += i
        # print()
        # input('Continue?')
            
    print(sum)
