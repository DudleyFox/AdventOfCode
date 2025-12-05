import sys


def readIngredients(filename):
    ranges = []
    ingredients = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            if '-' in line: # we have a range
                start, stop = [int(x) for x in line.split("-")]
                stop += 1
                ranges.append(range(start, stop))
            elif line != "":
                ingredients.append(int(line))
    return ranges, ingredients

           
if __name__ == "__main__":
    fresh = 0
    ranges, ingredients = readIngredients(sys.argv[1])
    for i in ingredients:
        for r in ranges:
            if i in r:
                fresh += 1
                break

    print(fresh)


