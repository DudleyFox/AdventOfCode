
def cleanCrates(c):
    return [x.strip().replace('[','').replace(']','') for x in c]

def readCrates(f):
    for l in f.readlines():
        crates = []
        if l.find('1') == -1:
            for x in range(0, len(l) - 1, 4):
                crates.append(l[x:x+4])
            yield crates
        else:
            return

def insertCrate(key, c, stacks):
    if c != '': # only insert if we have a crate
        if key in stacks:
            stacks[key].append(c)
        else:
            stacks[key] = [c]

def readInstructions(f):
    for l in f.readlines():
        line = l.strip()
        if line.startswith('move'):
            yield line

def followInstruction(instruction, stacks):
    m, count, f, key1, t, key2 = instruction.split(' ')
    count = int(count)
    key1 = int(key1)
    key2 = int(key2)
    for x in range(count):
        stacks[key2].append(stacks[key1].pop())


if __name__ == "__main__":
    crates = []
    instructions = []
    
    with open('input.txt', 'r') as f:
        for c in readCrates(f):
           crates.append(cleanCrates(c))
    with open('input.txt', 'r') as f:
        instructions = [x for x in readInstructions(f)]

    stacks = {}
    while len(crates) > 0:
        index = 0
        for c in crates.pop():
            index += 1
            insertCrate(index, c, stacks)

    for i in instructions:
        followInstruction(i, stacks)

    keys = list(stacks.keys())
    keys.sort()
    for k in keys:
        print(stacks[k][-1], end='')
    print()