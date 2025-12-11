import sys
import math


class Diagram:
    
    def __init__(self, lineToParse):
        self.lights = []
        self.buttons = []
        self.joltages = []
        for d in lineToParse:
            if d[0] == '[': # targets
                self.lights = [x for x in d[1:-1]]
            elif d[0] == '(': # buttons
                self.buttons.append(eval(d))
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


def readDiagrams(filename):
    points = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            diagrams = line.split(" ")
            yield Diagram(diagrams)


if __name__ == "__main__":
    diagrams = list(readDiagrams(sys.argv[1]))
    for d in diagrams:
        print(d)
    


