import sys

def readBatteries(filename):
    with open(filename,'r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            yield [int(x) for x in line]

def makeNumber(sequence):
    total = 0
    for x in sequence:
        total = total * 10 + x;
    return total

def compress(bank, size):
    if len(bank) > size:
        for x in range(len(bank)-1):
            if bank[x] < bank[x+1]:
                bank.pop(x)
                return bank
        return bank[0:size]
    return bank

def setJoltage(bank):
    # find 12 digits in order that make the largest joltage
    workingSet = []
    for x in bank:
        workingSet.append(x)
        workingSet = compress(workingSet, 12)
    return makeNumber(workingSet)
        


if __name__ == "__main__":
    total = 0
    for x in readBatteries(sys.argv[1]):
        joltage = setJoltage(x)
        total += joltage
        print(x, joltage, total)


