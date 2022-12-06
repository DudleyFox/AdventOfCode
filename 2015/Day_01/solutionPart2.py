

def getInput():
    with open('input.txt', 'r') as f:
        return f.read().strip()


floor = 0
map = {
    '(': 1,
    ')': -1
}
position = 0
for e in getInput():
    position += 1
    floor += map[e]
    if floor < 0:
        print(position)
        exit()

print(floor)
