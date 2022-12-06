
def parseXY(i):
    return [int(x) for x in i.split(',')]

def parseCommand(l):
    s = l.split(' ')
    if s[0] == 'toggle':
        x1,y1 = parseXY(s[1])
        x2,y2 = parseXY(s[3])
        return ('toggle', (x1,y1), (x2, y2))
    x1,y1 = parseXY(s[2])
    x2,y2 = parseXY(s[4])
    return (s[1], (x1,y1), (x2,y2))

def readCommandTuples():
    with open('input.txt','r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            yield parseCommand(l)

def initLights():
    lights = []
    for x in range(1000):
        lights.append([0 for y in range(1000)])
    return lights

def toggle(i):
    return i + 2

def on(i):
    return i + 1

def off(i):
    return max(0, i-1)

commandMap = {
    'toggle':toggle,
    'on':on,
    'off':off
}

def executeCommand(command, lights):
    x1, y1 = command[1]
    x2, y2 = command[2]
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            lights[x][y] = commandMap[command[0]](lights[x][y])


 

if __name__ == '__main__':
    lights = initLights()
    commands = [c for c in readCommandTuples()]
    for c in commands:
        executeCommand(c, lights)
    count = 0
    for x in range(1000):
        for y in range(1000):
            count += lights[x][y]

    print(count)



    
        