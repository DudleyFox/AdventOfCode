import circuitParser
import sys



if __name__ == '__main__':
    c = circuitParser.buildCircuit('input2.txt')
    print(c.signal(sys.argv[1]))
