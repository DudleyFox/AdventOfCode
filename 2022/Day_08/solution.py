import itertools
def readRowsAndColumns():
    rows = []
    columns = []
    first = True
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            row = [int(x) for x in l.strip()]
            rows.append(row)
            
            if first:
                first = False
                for x in row:
                    columns.append([x])
            else:
                index = 0
                for x in row:
                    columns[index].append(x)
                    index += 1
    return rows, columns

def checkVisible(last, current, visible, x, y):
    if current > last:
        visible.add((x,y))
        return current
    return last

def findVisible(i, a, visible, isRow):
    last = a[0]
    for x in range(1, len(a)-1):
        if isRow:
            last = checkVisible(last, a[x], visible, i, x)
        else:
            last = checkVisible(last, a[x], visible, x, i)
        if last == 9:
            break # nothing taller than nine.
    last = a[-1]
    for x in range(len(a)-1, 0, -1):
        if isRow:
            last = checkVisible(last, a[x], visible, i, x)
        else:
            last = checkVisible(last, a[x], visible, x, i)
        if last == 9:
            break # nothing taller than nine.


if __name__ == '__main__':
    visible = set()
    rows, columns = readRowsAndColumns()
    rowCount = len(rows)
    colCount = len(columns)
    count = rowCount*2 + colCount*2 - 4 # get all the edges -4 so we don't over count corners
    for x in range(1, rowCount-1):
        findVisible(x, rows[x], visible, True)
    for y in range(1, colCount-1):
        findVisible(y, columns[y], visible, False)

    count += len(visible)
    print(count)
        

