def readFile():
    s = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            s.append(l.strip())
    return s


class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.size = 0
        self.files = set()
        self.dirs = {}

    def addFile(self, size, filename):
        if filename not in self.files:
            self.files.add(filename)
            self.size += size
    
    def addDir(self, name):
        if name not in self.dirs:
            self.dirs[name] = Directory(name, self)

    def cd(self, name):
        if name == '..':
            return self.parent
        if name in self.dirs:
            return self.dirs[name]
        if name == self.name and name == '/':
            return self # special case for the first line of the script
        raise Exception(f'No dir by {name} found in {self.name}')

    def getSize(self):
        # our size is the sum of all files + the sum of all our children's files
        sum = 0
        for x in self.dirs.values():
            sum += x.getSize()
        return self.size + sum 

    def print(self, indent=0):
        prefix = ' '*indent
        slash = '/'
        if self.name == slash:
            slash = ''
        print(f'{prefix}{slash}{self.name}')
        d = list(self.dirs.keys())
        d.sort()
        for dir in d:
            self.dirs[dir].print(indent+2)
        for f in self.files:
            prefix = ' '*(indent+2)
            print(f'{prefix}{f}')

def handleCommand(dir, command):
    s = command.split(' ')
    if len(s) == 3: # this is the cd command:
        return dir.cd(s[2])
    return dir # the ls command doesn't change the directory

def handleListing(dir, item):
    i1, i2 = item.split(' ')
    if i1 == 'dir':
        dir.addDir(i2)
    else:
        dir.addFile(int(i1), i2)

def buildDirectoryTree(script):
    root = Directory('/', None)
    currentDir = root
    for x in script:
        if x[0] == '$':
            currentDir = handleCommand(currentDir, x)
        else:
            handleListing(currentDir, x)
    return root

def getSizesR(root, sizes):
    sizes.append(root.getSize())
    for d in root.dirs.values():
        getSizesR(d, sizes)

def getSizes(root):
    sizes = []
    getSizesR(root, sizes)
    return sizes


if __name__ == '__main__':
    root = buildDirectoryTree(readFile())
    sizes = getSizes(root)
    rightSizes = [x for x in sizes if x < 100001]
    total = sum(rightSizes)
    print(total)



        


        
