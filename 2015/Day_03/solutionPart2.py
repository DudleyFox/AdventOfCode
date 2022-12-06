


visited = set()

def getInput():
    with open('input.txt', 'r') as f:
        return f.read().strip()


def nextHouse(current, direction):
    # >^<v
    x,y = current
    if direction == '^':
        y += 1
    elif direction == 'v':
        y -= 1
    elif direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    return (x,y)

santaCurrent = (0,0)
robotCurrent = (0,0)
visited.add(santaCurrent)

toggle = False
for x in getInput():
    if toggle:
        robotCurrent = nextHouse(robotCurrent, x)
        visited.add(robotCurrent)
    else:
        santaCurrent = nextHouse(santaCurrent, x)
        visited.add(santaCurrent)
    toggle = not toggle 
    

print(len(visited))
