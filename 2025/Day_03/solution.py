import sys


def readBatteries(filename):
    with open(filename,'r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            yield [int(x) for x in line]

def getHighest(bank):
    h = 0
    i = 0
    for x in range(len(bank)):
        t = bank[x]
        if t > h:
            h = t
            i = x
    return (i, h)

def getSecondHighest(bank, ignore):
    h = 0
    i = 0
    for x in range(len(bank)):
        t = bank[x]
        if t > h and x != ignore and (x > ignore or ignore == len(bank) -1 ):
            h = t
            i = x
    return (i, h)

def setJoltage(bank):
    highest = getHighest(bank)
    second = getSecondHighest(bank, highest[0])
    if highest[0] < second[0]:
        return highest[1] * 10 + second[1]
    return highest[1] + second[1] * 10




if __name__ == "__main__":
    total = 0
    for x in readBatteries(sys.argv[1]):
        joltage = setJoltage(x)
        total += joltage
        print(x, joltage, total)


