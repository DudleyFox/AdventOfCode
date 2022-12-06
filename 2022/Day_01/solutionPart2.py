

def readSums():
    with open('input.txt','r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            if line:
                sum += int(line)
            else:
                yield sum
                sum = 0

def maxOfThree(l, i):
    l.sort()
    if i > l[0]:
        l[0] = i


if __name__ == '__main__':
    topThree = [0,0,0]
    for s in readSums():
        maxOfThree(topThree, s)

    print(topThree)
    sum = 0
    for x in topThree:
        sum += x
    print(sum)