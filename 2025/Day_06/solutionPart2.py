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
        tuplets.append((row[-2:-1][0], row[-1:][0], row[:-2]))

    






def transformMathProblems(problemsAsColumns):
    """
    Take the columnar problems that look like this:

        123 32 .51 64.
        .45 64 387 23.
        ..6 98 215 314
        *   +  *.. +..
    
    and turn them into a list of tuples like this
        (*, [123, .45, ..6])
        (+, [32, 64, 98])
        (*, [.51, 387, 215])
        (+, [64., 23., 314])
    and then run them into a list of tuples like this
        (*, [356, 24, 1])
        (+, [248, 369])
        (*, [175, 581, 32])
        (+, [4, 431, 623])
    """
    columnCount = len(problemsAsColumns[0])
    rowList = [[] for x in range(columnCount)]

    for x in problemsAsColumns:
        columnIndex = 0
        for y in x:
            rowList[columnIndex].append(y)
            columnIndex += 1
        

    print(rowList)
    tupleList = []
    for x in rowList:
        tupleList.append((x[-1:][0].strip(), x[:-1]))
    print(tupleList)

    finalList = []

    for operation, data in tupleList:
        newData = [0 for x in data]
        newDataIndex = 0
        for i in range(2, -1, -1):
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
    t = tupletize(lines, columnWidths)
    print(t)
    




