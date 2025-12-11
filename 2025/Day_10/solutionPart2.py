import sys
import math


def generate(elements, index):
    tIndex = index
    length = len(elements)
    result = []
    while tIndex > -1:
        s = elements[tIndex % length]
        result.append(s)
        tIndex = tIndex // length
        tIndex -= 1
    return result

def compareLists(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return len(l1) == len(l2)

class Diagram:
    
    def __init__(self, lineToParse):
        self.lights = []
        self.buttons = []
        self.joltages = []
        for d in lineToParse:
            if d[0] == '[': # targets
                self.lights = [x for x in d[1:-1]]
            elif d[0] == '(': # buttons
                button = [int(x) for x in d[1:-1].split(",")]
                self.buttons.append(tuple(button))
            elif d[0] == '{': # joltages
                self.joltages = [int(x) for x in d[1:-1].split(",")]
            else:
                raise "Unrecognized Diagram"

    def __str__(self):
        s = []
        lights = f"[{"".join([x for x in self.lights])}]"
        s.append(lights)
        for b in self.buttons:
            s.append(str(b))
        joltages = f"{{{",".join([str(x) for x in self.joltages])}}}"
        s.append(joltages)
        return " ".join(s)

    def findButtonSequence(self):
        index = 0
        while True:
            buttonsToTest = generate(self.buttons, index)
            result = self.applyButtons(buttonsToTest)
            if compareLists(result, self.joltages):
                return buttonsToTest
            index += 1

    def applyButtons(self, buttons):
        joltages = [0] * len(self.joltages)
        for button in buttons:
            for i in button:
                joltages[i] += 1
        return joltages


def readDiagrams(filename):
    points = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            diagrams = line.split(" ")
            yield Diagram(diagrams)


if __name__ == "__main__":
    diagrams = list(readDiagrams(sys.argv[1]))

    total = 0
    for d in diagrams:
        sequence = d.findButtonSequence()
        total = total + len(sequence)
        print()
        print(total, sequence)
    


