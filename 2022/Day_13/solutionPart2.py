# 3898 too low
# 5221
# 4983
# 5196

# 26462 wrong on part 2
# 22848 wrong on part 2 :(

import sys
import functools

def readPackets(filename):
    lines = []
    divider1 = [[2]]
    divider2 = [[6]]

    lines.append(divider1)
    lines.append(divider2)

    with open(filename, 'r') as f:
        for l in f.readlines():
            t = l.strip()
            if t:
                lines.append(eval(t))
    return lines
    

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
    print('lists', tl, tr)
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

def sortCompare(x,y):
    status, l, r = compare(('',x,y), 0)
    if status == 'valid':
        return -1
    if status == 'invalid':
        return 1
    return -1 # default to valid

def isDivider(l, val, index, oldIndex):
    try:
        if len(l) == 1 and len(l[0]) == 1 and l[0][0] == val:
            return index
        return oldIndex
    except:
        return oldIndex

    
    
sum = 0
if __name__ == '__main__':
    packets = readPackets(sys.argv[1])
    keyFunc = functools.cmp_to_key(sortCompare)
    sortedPackets = sorted(packets, key=keyFunc)

    divider1Index = 0
    divider2Index = 0
            
    for x in range(len(sortedPackets)):
        divider1Index = isDivider(sortedPackets[x], 2, x+1, divider1Index)
        divider2Index = isDivider(sortedPackets[x], 6, x+1, divider2Index)
        print(x+1, ':', sortedPackets[x])

    print(divider1Index, divider2Index, divider2Index * divider1Index)
