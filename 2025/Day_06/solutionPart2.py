import sys
import re
import functools

def safeInt(s):
    if s:
        return int(s)
    return 0

def readLines(filename):
    with open(filename,'r') as f:
        return [l[:-1] for l in f.readlines()]

def getColumnWidths(lines):
    lastline = lines[len(lines) - 1] # this should be all the operations, they can tell us how long the line is.
    columnIndex = -1
    currentCount = 0
    columnWidths = {}
    for x in lastline:
        if x in ['+','*']:
            columnWidths[columnIndex] = currentCount - 1 # ignore the separator
            currentCount = 0
            columnIndex += 1
        currentCount += 1
        lastX = x

    columnWidths[columnIndex] = currentCount # no separator to ignore here

    columnWidths.pop(-1, None)

    return columnWidths



def combineNumbers(old, new):
    if new > 0:
        return old * 10 + new
    return old

def tupletize(lines, columnWidths):
    # get the columns in order from the dictionary
    columns = list(columnWidths.keys())
    columns.sort()
    rows = []
    width = 0
    for x in columns:
        print(x, columnWidths[x])
        row = []
        for l in lines:
            row.append(l[width:columnWidths[x]+width])
        row.append(columnWidths[x])
        rows.append(row)
        width = width + 1 + columnWidths[x]

    tuplets = []
    for row in rows:
        # tuple of (operator, width, data)
        # eg ('*', 3, ['332', '453', '89 ']))
        tuplets.append((row[-2:-1][0].strip(), row[-1:][0], row[:-2]))

    return tuplets

    
def transformTuples(inputTuples):
    """
    Take the tuple data problems that look like this:
        ('*  ', 3, ['123', ' 45', '  6'])
        ('+  ', 3, ['328', '64 ', '98 '])
        ('*  ', 3, [' 51', '387', '215'])
        ('+  ', 3, ['64 ', '23 ', '314'])

    and then run them into a list of tuples like this
        (*, [356, 24, 1])
        (+, [248, 369])
        (*, [175, 581, 32])
        (+, [4, 431, 623])
    """
    finalList = []

    for operation, width, data in inputTuples:
        newData = [0 for x in range(width)]
        newDataIndex = 0
        for i in range(width-1, -1, -1):
            for d in data:
                newData[newDataIndex] = combineNumbers(newData[newDataIndex], safeInt(d[i].strip()))
            newDataIndex += 1

        finalList.append((operation, newData))

                
    print(finalList)
    return finalList

def operate(mathProblem):
    operation, data = mathProblem
    if operation == '+':
        return functools.reduce(lambda x, y: x+y, data, 0)
    elif operation == '*':
        return functools.reduce(lambda x, y: x*y, data, 1)
    else:
        raise f"Unrecognized operation {operation}"

    



           
if __name__ == "__main__":
    lines = readLines(sys.argv[1])
    print(lines)
    columnWidths = getColumnWidths(lines)
    print(columnWidths)
    tuplets = tupletize(lines, columnWidths)
    for t in tuplets:
        print(t)
    finalTuples = transformTuples(tuplets)
    for f in finalTuples:
        print(f)

    total = 0
    for f in finalTuples:
        total += operate(f)

    print(total)

    




