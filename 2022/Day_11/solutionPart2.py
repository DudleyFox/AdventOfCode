import math

monkeyNames = [
    'Brass',
    'Tin',
    'Gold',
    'Silver',
    'Lead',
    'Wolfram',
    'Iron',
    'Mercury'
]

primes = [2,3]
while len(primes) < 50000:
    candidate = primes[-1] + 2
    sqc = math.sqrt(candidate)
    flag = True
    while flag:
        for prime in primes:
            if prime > sqc:
                primes.append(candidate)
                flag = False
                break
            elif candidate % prime == 0:
                candidate += 2
                sqc = math.sqrt(candidate)
                break

################# Sample Monkey
# Monkey 0:
#   Starting items: 63, 57
#   Operation: new = old * 11
#   Test: divisible by 7
#     If true: throw to monkey 6
#     If false: throw to monkey 2

def parseName(s):
    nameIndex = int(s[7])
    return monkeyNames[nameIndex]

def parseTrueFalse(s):
    nameIndex = int(s.split(' ')[5])
    return monkeyNames[nameIndex]

def parseItems(s):
    items = s.split(':')[1].split(', ')
    items = [int(x) for x in items]
    return items

def printThrow(i, t, b, m1, m2, item):
    print(f'{m1} throws {item} to {m2}\t{i}:{t}:{b}')
    pass

def getFactors(n):
    factors = []
    t = n
    index = 0
    sqt = math.sqrt(t)
    while t != 1:
        factor = primes[index]
        if (t % factor) == 0: 
            factors.append(factor)
            t = t // factor
            sqt = math.sqrt(t)
        else:
            index += 1
            factor = primes[index]
            if factor > sqt:
                factors.append(t)
                return factors
    return factors

class Operation:
    def __init__(self, file):
        s = file.readline().strip().split('=')[1].strip()
        operations = {
            '+': lambda x,y: x+y,
            '*': lambda x,y: x*y,
        }

        old, op, i = s.split(' ')
        self.operation = operations[op]
        if i == 'old':
            self.operand = i
        else:
            self.operand = int(i)
    
    def operate(self, x):
        maxFactors = set((2,3,5,7,11,13,17,19,23))
        t = 0
        if self.operand == 'old':
            t = self.operation(x,x)
        else:
            t = self.operation(x, self.operand)
        factors = set(getFactors(t))
        newFactors = [x for x in factors if x in maxFactors]
        product = 1
        for x in newFactors:
            product *= x
        t2 = product * 29
        print(t,t2,factors,newFactors)
        return t2

class Monkey:
    def __init__(self, file, monkeys):
        # Read the name
        self.name = parseName(file.readline().strip())
        self.items = parseItems(file.readline().strip())
        self.operation = Operation(file)
        self.test = int(file.readline().strip().split(' ')[3])
        self.trueMonkey = parseTrueFalse(file.readline().strip())
        self.falseMonkey = parseTrueFalse(file.readline().strip())
        file.readline() # read the trailing line, so the next monkey starts where expected.
        self.inspections = 0
        monkeys[self.name] = self

    def catch(self, i):
        self.items.append(i)

    def inspectItems(self, monkeys):
        for i in self.items:
            wl = self.operation.operate(i)
            if wl % self.test == 0:
                printThrow(i, self.test, 'true', self.name, self.trueMonkey, wl)
                monkeys[self.trueMonkey].catch(wl)
            else:
                printThrow(i, self.test, 'false', self.name, self.falseMonkey, wl)
                monkeys[self.falseMonkey].catch(wl)
            self.inspections +=1
        self.items = [] # all done

    def __str__(self):
        s = 'Monkey:\n'
        s += f'\tName: {self.name}\n'
        s += f'\tInspections: {self.inspections}\n'
        s += f'\tItems: {", ".join([str(x) for x in self.items])}\n'
        s += f'\tTest: {self.test}\n'
        s += f'\ttrueMonkey: {self.trueMonkey}\n'
        s += f'\tfalseMonkey: {self.falseMonkey}\n'
        return s

if __name__ == '__main__':
    monkeys = {}
    monkeyList = []
    with open('test-input.txt') as f:
        for m in range(4):
            monkeyList.append(Monkey(f, monkeys))

    
    for x in range(1000):
        for m in monkeyList:
            m.inspectItems(monkeys)
        print(x)

    for m in monkeyList:
        print(m)
    activity = [x.inspections for x in monkeyList]
    activity.sort()
    print(activity)
    m1, m2 = activity[-2:]
    print (m1*m2)
