import sys


def readRotations(filename):
    with open(filename,'r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            operation = l[0]
            amount = int(l[1:])
            yield (operation,amount)

current = 50
zeroCount = 0
dialSize = 100

for operation, amount in readRotations(sys.argv[1]):
    workingAmount = amount
    tZero = workingAmount // dialSize
    remainder = workingAmount % dialSize
    if operation == "L":
        if current != 0 and current - remainder <= 0:
            tZero += 1
        workingAmount = dialSize - remainder
    else: # operation has to be R
        if current + remainder >= dialSize:
            tZero += 1
    print(operation, amount, workingAmount, tZero, zeroCount, current)
    current = (current + workingAmount) % dialSize
    zeroCount += tZero
    print(current, zeroCount, workingAmount)
    print()


print(zeroCount)
