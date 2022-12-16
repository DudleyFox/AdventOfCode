
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

def listify(t):
    if type(t) is list:
        return t
    return [t]

def compare(tup):
    status, l, r, index = tup
    if type(l) is int and type (r) is int:
        # print('ints:', l,r,index)
        if l < r:
            return ('valid', l, r, index)
        elif l > r:
            return ('invalid', l, r, index)
        return ('unknown', l, r, index)
    if type(l) is list and type(r) is list:
        # print('lists:', l,r,index)
        for x in range(len(l)):
            if x > len(r) - 1:
                return ('invalid', l, r, index)
            result = compare(('', l[x], r[x], index))
            if result[0] != 'unknown':
                return result
        return ('unknown', l, r, index)
    tl = listify(l)
    tr = listify(r)
    return compare(('', tl, tr, index))
    
sum = 0
if __name__ == '__main__':
    for i,l,r in readPairs():
        result = compare(('',l,r,i))
        print(i, result, l,r)
        if result[0] == 'valid' or result[0] == 'unknown':
            sum += result[3]
            
    print(sum)
