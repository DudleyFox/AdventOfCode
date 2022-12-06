

sum = 0

with open('input.txt','r') as f:
    for l in f.readlines():
        sides = []
        line = l.strip()
        length, width, height = (int(x) for x in line.split('x'))
        sides.append(length*width)
        sides.append(length*height)
        sides.append(width*height)
        sides.sort()
        sum += sides[0]*3 + sides[1]*2 + sides[2] * 2

print(sum)
        