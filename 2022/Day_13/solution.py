# 3898 too low
# 5221
# 4983
# 5196

import sys

def readPairs(filename):
    lines = []
    with open(filename, 'r') as f:
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

def listify(t):
    if type(t) is list:
        return (t,False)
    return ([t],True)

isInt = lambda x : type(x) is int

def compareInts(l,r, depth):
    print('ints:', l,r,depth)
    if l < r:
        return ('valid', l, r)
    elif l > r:
        return ('invalid', l, r)
    return ('unknown', l, r)

def compare(tup, depth):
    status, l, r = tup
    if isInt(l) and isInt(r):
        return compareInts(l,r,depth)
    # if they are not ints, then they have to be lists:
    tl, leftListified = listify(l)
    tr, rightListified = listify(r)
    index = 0
    while index < len(tl):
        if index >= len(tr): # ran out on the right side first
            return ('invalid', l, r)
        result = compare(('', tl[index], tr[index]), depth+1)
        print(result)
        if result[0] != 'unknown':
            return result
        index += 1
    if index < len(tr):
        return ('valid', l, r)
    if depth == 0:
        return ('valid', l, r)
    return ('unknown', l, r)
    
    
sum = 0
if __name__ == '__main__':
    for i,l,r in readPairs(sys.argv[1]):
        result = compare(('',l,r), 0)
        print(i, result, l,r)
        if result[0] == 'valid' or result[0] == 'unknown':
            sum += i
        print('**************************')
        # data = input("Continue?")
            
    print(sum)
