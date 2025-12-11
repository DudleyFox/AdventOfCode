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
                button = [int(x) for x in d[1:-1].split(",")]
                self.buttons.append(tuple(button))
            elif d[0] == '{': # joltages
                self.joltages = [int(x) for x in d[1:-1].split(",")]
            else:
                raise "Unrecognized Diagram"
        self.transformButtons()


    def transformButtons(self):
        # the buttons as written are the number of the joltage that
        # is incremented, for example (0,2,5). We can transform that
        # to [1,0,1,0,0,1] assuming we have 6 joltages. Then it just becomes
        # a math problem
        # for instance from the test in input we have
        #     [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        # we can turn that into
        #   1x + 0y + 1z + 1v + 0w + -7 = 0
        #   0x + 0y + 0z + 1v + 1w + -5 = 0
        #   1x + 1y + 0z + 1v + 1w + -12 = 0
        #   1x + 1y + 0z + 0v + 1w + -7 = 0
        #   1x + 0y + 1z + 0v + 1w + -2 = 0
        #
        # Now I just need to write the program for that...

        newButtons = []
        for b in self.buttons:
            template = [0 for x in self.joltages]
            for x in b:
                template[x] = 1
            newButtons.append(tuple(template))
        self.buttons = newButtons

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
        print(d)
    


