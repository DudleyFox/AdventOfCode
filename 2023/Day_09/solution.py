import sys

def readSequences(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            if l != '':
                yield [int(x) for x in l.split(' ')]


def getNextNumber(sequence):
    print(sequence)
    if sequence[-1:][0] == 0:
        return 0
    last = sequence[0]
    newSeq = []
    for x in sequence[1:]:
        newSeq.append(x - last)
        last = x
    return last + getNextNumber(newSeq)

if __name__ == "__main__":
    sequences = readSequences(sys.argv[1])
    lasts = []
    for s in sequences:
        lasts.append(getNextNumber(s))
    print(sum(lasts))

