import sys

# Second guess: 351991007887524
344771884978261


def readIngredients(filename):
    ranges = []
    ingredients = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            if '-' in line: # we have a range
                start, stop = [int(x) for x in line.split("-")]
                ranges.append((start, stop))
            elif line != "":
                ingredients.append(int(line))
    return ranges, ingredients

def addRange(ranges, newRange):
    rangesLength = len(ranges)
    if rangesLength == 0:
        ranges.append(newRange)
    else:
        for x in range(rangesLength):
            start1, stop1 = ranges[x]
            start2, stop2 = newRange
            xStart = max(start1, start2)
            xStop = min(stop1, stop2)
            if xStop >= xStart: # we have overlap
                ranges[x] = (min(start1,start2), max(stop1,stop2))
                return
        # if we got here no overlaps
        ranges.append(newRange)


                

def compressRanges(ranges):
    newRanges = []
    for r in ranges:
        addRange(newRanges, r)
    if len(newRanges) != len(ranges): # try to compress it again
        newRanges = compressRanges(newRanges)
    return newRanges

           
if __name__ == "__main__":
    fresh = 0
    ranges, ingredients = readIngredients(sys.argv[1])
    ranges = compressRanges(ranges)
    for r in ranges:
        fresh += r[1]-r[0]+1
            

    print(fresh)


