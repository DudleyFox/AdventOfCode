
x = 1

def buildInstuctions():
    with open('input.txt', 'r') as f:
        for i in f.readlines():
            l = i.strip()
            if l == 'noop':
                yield 0
            else:
                yield 0
                yield int(l.split(' ')[1])




cycle = 0
screen = []
for i in buildInstuctions():
    
    # draw
    if abs((cycle % 40) - x) < 2:
        screen.append('#')
        # print(x, cycle, '#')
    else:
        screen.append('.')
        # print(x, cycle, '.')
    # complete instruction
    cycle += 1
    x += i


for index in range(len(screen)):
    print(screen[index], end='')
    if (index + 1) % 40 == 0:
        print()


