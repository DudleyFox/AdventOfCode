

def getInput():
    with open('input.txt', 'r') as f:
        return f.read().strip()


floor = 0
map = {
    '(': 1,
    ')': -1
}
for e in getInput():
    floor += map[e]

print(floor)
