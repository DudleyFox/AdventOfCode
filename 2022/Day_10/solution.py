
interestingCycles = set([20, 60, 100, 140, 180, 220])
x = 1

def buildInstuctions():
    with open('input.txt', 'r') as f:
        for i in f.readlines():
            l = i.strip()
            if l == 'noop':
                yield 0
            else:
                yield 0
                yield int(l.split(' ')[1])




cycle = 0
signal = 0
for i in buildInstuctions():
    cycle += 1
    x += i
    if cycle in interestingCycles:
        signal += cycle * x


print(signal)


