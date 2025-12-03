

import sys


def readRanges(filename):
    with open(filename,'r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            for span in l.split(","):
                start, stop = span.split("-")
                yield (int(start), int(stop)+1)

def allPartsEqual(anArray):
    last = anArray[0]
    for x in anArray:
        if x != last:
            return False
        last = x
    print("Found:", anArray)
    return True

def isInvalid(toTest):
    id = str(toTest)
    half = len(id) // 2
    for x in range(1, half+1):
        parts = [id[i:i+x] for i in range(0, len(id), x)]
        if allPartsEqual(parts):
            return True
    return False


invalidIds = []

for start, stop in readRanges(sys.argv[1]):
    for x in range(start, stop):
        if isInvalid(x):
            invalidIds.append(x)
            print("Found:", x)

total = 0
for t in invalidIds:
    total += t

print(total)

