

def isFullyContained(p1, p2):
    r0, r1 = p1
    s0, s1 = p2
    if r0 <= s0 and r1 >= s1:
        return 1
    if s0 <= r0 and s1 >= r1:
        return 1
    return 0

def readPairs():
    with open('input.txt','r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            p1, p2 = line.split(',')
            # no make them into tuples
            p1 = [int(x) for x in p1.split('-')]
            p2 = [int(x) for x in p2.split('-')]
            yield (p1,p2)

sum = 0
for p1, p2 in readPairs():
    sum += isFullyContained(p1, p2)

print(sum)
