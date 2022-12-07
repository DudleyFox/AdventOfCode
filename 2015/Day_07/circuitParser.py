
keyWords = set((
'AND',
'OR',
'NOT',
'RSHIFT',
'LSHIFT',
'->'
))

def readSpec(filename):
    spec = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            spec.append(l.strip())
    return spec

def NumberResolver(n, key):
    def resolver(circuit):
        print(f'Resolve {key}: {n}')
        return int(n)
    return resolver

def WireResolver(wire, key):
    def resolver(circuit):
        print(f'Resolve {key}: {wire}')
        return circuit.signal(wire)
    return resolver

def NotResolver(wire, key):
    def resolver(circuit):
        print(f'Resolve {key}: NOT {wire}')
        return ~(circuit.signal(wire))
    return resolver

def RshiftResolver(wire, n, key):
    def resolver(circuit):
        print(f'Resolve {key}: {wire} >> {n}')
        return circuit.signal(wire) >> int(n)
    return resolver

def LshiftResolver(wire, n, key):
    def resolver(circuit):
        print(f'Resolve {key}: {wire} << {n}')
        return circuit.signal(wire) << int(n)
    return resolver

def AndResolver(wire1, wire2, key):
    if wire1.isdigit():
        def nResolver(circuit):
            print(f'Resolve {key}: {wire1} AND {wire2}')
            return int(wire1) & circuit.signal(wire2)
        return nResolver 
    def resolver(circuit):
        print(f'Resolve {key}: {wire1} AND {wire2}')
        return circuit.signal(wire1) & circuit.signal(wire2)
    return resolver

def OrResolver(wire1, wire2, key):
    def resolver(circuit):
        print(f'Resolve {key}: {wire1} OR {wire2}')
        return circuit.signal(wire1) | circuit.signal(wire2)
    return resolver

def buildResolver(exp, key):
    s = exp.split(' ')
    l = len(s)
    if l == 1:
        n = s[0]
        if n.isdigit():
            return NumberResolver(n, key)
        else:
            return WireResolver(n, key)
    if l == 2:
        return NotResolver(s[1], key)
    
    op = s[1]
    if op == 'AND':
        return AndResolver(s[0], s[2], key)
    if op == 'OR':
        return OrResolver(s[0], s[2], key)
    if op == 'RSHIFT':
        return RshiftResolver(s[0], s[2], key)
    if op == 'LSHIFT':
        return LshiftResolver(s[0], s[2], key)
    raise "Oops" 


def parseSpecLine(line):
    expression, wire = [x.strip() for x in line.split(' -> ')]
    resolver = buildResolver(expression, wire)
    return wire, resolver

def buildMap(spec):
    map = {}
    for x in spec:
        wire, resolver = parseSpecLine(x)
        map[wire] = resolver
    return map

class Circuit:
    def __init__(self, map):
        self.map = map
        self.memoCache = {}

    def signal(self, wire):
        if wire not in self.memoCache:
            self.memoCache[wire] = self.map[wire](self) & 0x0000ffff
        return self.memoCache[wire]

def buildCircuit(filename):
    spec = readSpec(filename)
    map = buildMap(spec)
    return Circuit(map)


    


# grammar
# <expression> ::= <input> '->' <wire>
# <input> ::= <wire> <bgate> <number> | <number> <bgate> <wire> | <wire> <bgate> <wire> | <ugate> <wire> | <number>
# <bgate> ::= 'AND' | 'OR' | 'RSHIFT' | 'LSHIFT'
# <ugate> ::= 'NOT'
# <wire> ::= [a-z]+
# <number> ::= [0-9]+


