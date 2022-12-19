# 3898 too low
# 5221
# 4983
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
    tl,listifiedLeft = listify(l)
    tr,listifiedRight = listify(r)
    print(f'lists:\n\t{l}\n\t{r}\n\t{depth}')
    for x in range(len(tl)):
        if x > len(tr) - 1:
            if listifiedRight: # we had to turn an element into a list, so we haven't run out
                return ('unknown', l, r)
            else:
                return ('invalid', l, r)
        result = compare(('', tl[x], tr[x]), depth+1)
        if result[0] != 'unknown':
            return result
    if depth == 0 or (len(tl) < len(tr) and not listifiedLeft):
        return ('valid', l, r)
    else:
        return ('unknown', l, r)
   
    
    
sum = 0
if __name__ == '__main__':
    for i,l,r in readPairs():
        result = compare(('',l,r), 0)
        print(i, result, l,r)
        if result[0] == 'valid' or result[0] == 'unknown':
            sum += i
        print('**************************')
        # data = input("Continue?")
            
    print(sum)
