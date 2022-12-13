
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

class Operation:
    def __init__(self, file):
        s = file.readline().strip().split('=')[1].strip()
        operations = {
            '+': lambda x,y: x+y,
            '*': lambda x,y: x*y,
            '-': lambda x,y: x-y,
            '/': lambda x,y: x//y # integer math
        }

        old, op, i = s.split(' ')
        self.operation = operations[op]
        if i == 'old':
            self.operand = i
        else:
            self.operand = int(i)
    
    def operate(self, x):
        if self.operand == 'old':
            return self.operation(x,x) // 3
        return self.operation(x, self.operand) // 3 # let this worry down the item

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
        return s

if __name__ == '__main__':
    monkeys = {}
    monkeyList = []
    with open('input.txt') as f:
        for m in range(8):
            monkeyList.append(Monkey(f, monkeys))

    
    for x in range(20):
        for m in monkeyList:
            print(m)
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        for m in monkeyList:
            m.inspectItems(monkeys)
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

    for m in monkeyList:
        print(m)
    activity = [x.inspections for x in monkeyList]
    activity.sort()
    print(activity)
    m1, m2 = activity[-2:]
    print (m1*m2)
