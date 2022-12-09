# The initial solution is really static analysis when you get
# down to it, and cannot handle the wire values actually changing.
# I want to write a simulator than can actually handle the wire
# values changing.
import sys
from functools import reduce

def readSpec(filename):
    spec = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            spec.append(l.strip())
    return spec

class CircuitBase:
    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.value = None

    def connectInput(self, input):
        input.connectOutput(self)

    def connectOutput(self, output):
        if self.value != None:
            output.setInput(self.value, self.name)
        self.outputs.append(output)

    def triggerOutput(self):
        for o in self.outputs:
            o.setInput(self.value, self.name)

    def setInput(self, value, name):
        v = value & 0x0000ffff
        # print(f'{self.name} received input {v} from {name}')
        if v != self.value:
            self.value = v
            self.triggerOutput()

class ConstantValue(CircuitBase):
    def __init__(self, name, value):
        CircuitBase.__init__(self, name)
        self.value = value    

class Wire(CircuitBase):
    pass


class Gate(CircuitBase):
    def __init__(self, name, operation, minInputs, inputs = []):
        CircuitBase.__init__(self, name)
        self.inputs = {}
        self.operation = operation
        self.minInputs = minInputs
        for i in inputs:
            self.connectInput(i)

    def connectInput(self, input):
        # print(f'Connecting {input.name}')
        self.inputs[input.name] = None
        CircuitBase.connectInput(self, input)

    def setInput(self, value, name):
        # print(f'{self.name} received input {value & 0x0000ffff} from {name}')
        self.inputs[name] = value
        values = list(map(lambda x: x != None, self.inputs.values()))
        ready = reduce(lambda x,y: x and y, values, True)
        if ready and len(self.inputs) >= self.minInputs:
            # print(f'**** {self.inputs}')
            self.value = self.operation(list(self.inputs.values()))
            self.triggerOutput()

def andOp(v):
    return v[0] & v[1]

def orOp(v):
    return v[0] | v[1]

def rShift(v):
    # print(v)
    result = v[0] >> v[1]
    # print(f'****rshift: {result}') 
    return result

def lShift(v):
    return v[0] << v[1]

def notOp(v):
    return ~v[0]

class Circuit:
    def __init__(self, spec):
        self.wires = {}
        self.gates = {}

        self.parseSpec(spec)

    def parseSpec(self, spec):
        for s in spec:
            self.parseSpecLine(s)

    def parseSpecLine(self, line):
        expression, wire = [x.strip() for x in line.split(' -> ')]
        output = self.buildWire(wire)
        input = self.buildInput(expression)
        output.connectInput(input)

    def buildWire(self, wireName):
        if wireName.isdigit():
            return ConstantValue(wireName, int(wireName))

        if wireName not in self.wires:
            self.wires[wireName] = Wire(wireName)
        return self.wires[wireName]

    def addGate(self, gate):
        self.gates[gate.name] = gate
        return gate

    def buildInput(self, expression):
        s = expression.split(' ')
        l = len(s)
        if l == 1:
            n = s[0]
            return self.buildWire(n)
        if l == 2:
            n = s[1]
            return self.addGate(Gate(f'NOT({n})', notOp, 1, [self.buildWire(n)]))
        
        op = s[1]
        w1 = self.buildWire(s[0])
        w2 = self.buildWire(s[2])
        name = f'{w1.name}-{op}-{w2.name}'
        if op == 'AND':
            return self.addGate(Gate(name, andOp, 2, [w1, w2]))
        if op == 'OR':
            return self.addGate(Gate(name, orOp, 2, [w1, w2]))
        if op == 'RSHIFT':
            return self.addGate(Gate(name, rShift, 2, [w1, w2]))
        if op == 'LSHIFT':
            return self.addGate(Gate(name, lShift, 2, [w1, w2]))
        raise "Oops"

    def signal(self, name):
        return self.wires[name].value & 0x0000ffff 
            

if __name__ == '__main__':
    spec = readSpec('input.txt')
    c = Circuit(spec)
    print(c.signal('a'))
    v = c.signal('a')
    c.wires['b'].setInput(v, ' a to b ')
    print(c.signal('a'))
    