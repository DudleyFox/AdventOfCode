import sys

            
class Range:
    def __init__(self, dStart, sStart, length):
        self.destStart = dStart
        self.srcStart = sStart
        self.srcEnd = sStart + length - 1

    def hasMapping(self, input):
        return input >= self.srcStart and input <= self.srcEnd
    
    def findMapping(self, input):
        if self.hasMapping(input):
            output = (input - self.srcStart) + self.destStart
            print(f'Mapped {input} to {output} with {self}')
            return output
        return input
    
    def __str__(self):
        return f'Range {self.srcStart}-{self.srcEnd}: {self.destStart}'

class Map:
    def __init__(self, f):
        self.name = f.readline().strip()
        line = f.readline().strip()
        self.ranges = []
        while line:
            d, s, l = line.split(' ')
            self.ranges.append(Range(int(d), int(s), int(l)))
            line = f.readline().strip()

    def doMapping(self, input):
        output = input
        for r in self.ranges:
            if (r.hasMapping(input)):
                return r.findMapping(input)
        return output

    def __str__(self):
        return self.name + str(len(self.ranges))


def readData(fileName):
    seeds = []
    maps = []
    with open(fileName, 'r') as f:
        junk, rawSeeds = f.readline().strip().split(':')
        seeds = [int(x) for x in rawSeeds.split(' ') if x != '']
        f.readline()
        for x in range(7):
            maps.append(Map(f))
    return seeds, maps

def findMinimumLocation(seed, maps):
    tmp = seed
    for m in maps:
        tmp = m.doMapping(tmp)
    return tmp


if __name__ == "__main__":
    seeds, maps = readData(sys.argv[1])
    print (seeds)
    locations = []
    for s in seeds:
        locations.append(findMinimumLocation(s, maps))
    print (locations)
    locations.sort()
    print(locations[0])