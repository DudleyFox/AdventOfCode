
import sys


def readRanges(filename):
    with open(filename,'r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            for span in l.split(","):
                start, stop = span.split("-")
                yield (int(start), int(stop)+1)

def isInvalid(toTest):
    id = str(toTest)
    if len(id) % 2 == 1:
        return False
    half = len(id) // 2
    return id[0:half] == id[half:]


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

