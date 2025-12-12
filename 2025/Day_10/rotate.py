
buttons = [
    (1, 0, 1, 1, 1),
    (0, 0, 1, 1, 0),
    (1, 0, 0, 0, 1),
    (1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1),
]

joltages = (7,5,12,7,2)

buttons = [
    (0,0,0,1),
    (0,1,0,1),
    (0,0,1,0),
    (0,0,1,1),
    (1,0,1,0),
    (1,1,0,0),
]

joltages = [3,5,4,7]

rotation = []
for x in range(len(joltages)):
    rotation.append([])
print(rotation)

variables = "xyzvwabcdefg"


for i in range(len(joltages)):
    vIndex = 0
    for b in buttons:
        rotation[i].append(str(b[i])+variables[vIndex])
        vIndex += 1

for i in range(len(joltages)):
    rotation[i].append(str(joltages[i]))

for r in rotation:
    print(f"{" + ".join(r)} = 0")

