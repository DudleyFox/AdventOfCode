import sys
import re
import functools


def readMathProblems(filename):
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            line = re.sub(r' +', ' ', line)
            yield line.split(' ')

def transformMathProblems(problemsAsColumns):
    """
    Take the columnar problems that look like this:

        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   + 
    
    and turn them into a list of tuples like this
        (*, [123, 45, 6])
        (+, [328, 64, 98])
        (*, [51, 387, 215])
        (+, [64, 23, 314])
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
        tupleList.append((x[-1:][0], [int(y) for y in x[:-1]]))
    print(tupleList)
    return tupleList

def operate(mathProblem):
    operation, data = mathProblem
    if operation == '+':
        return functools.reduce(lambda x, y: x+y, data, 0)
    elif operation == '*':
        return functools.reduce(lambda x, y: x*y, data, 1)
    else:
        raise f"Unrecognized operation {operation}"

    



           
if __name__ == "__main__":
    problemsAsColumns = list(readMathProblems(sys.argv[1]))
    tupleList = transformMathProblems(problemsAsColumns)
    total = 0
    for problem in tupleList:
        total += operate(problem)

    print(total)


