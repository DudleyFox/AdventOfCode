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

for operation, amount in readRotations(sys.argv[1]):
    print(operation, amount, current, zeroCount)
    workingAmount = amount
    if operation == 'L':
        workingAmount = 100 - amount
    current = (current + workingAmount) % 100
    if current == 0:
        zeroCount += 1

print(zeroCount)
