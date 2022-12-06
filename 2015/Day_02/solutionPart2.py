

sum = 0

def cubicFeet(s):
    product = 1
    for x in s:
        product *= x
    return product

with open('input.txt','r') as f:
    for l in f.readlines():
        sides = []
        line = l.strip()
        length, width, height = (int(x) for x in line.split('x'))
        sides.append(length)
        sides.append(width)
        sides.append(height)
        sides.sort()
        sum += sides[0]*2 + sides[1]*2 + cubicFeet(sides)

print(sum)
        