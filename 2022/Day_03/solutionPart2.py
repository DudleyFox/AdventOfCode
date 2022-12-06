
sum = 0

def priority(c):
    o = ord(c)
    if o > 90:
        return o - 96
    return o - 38

def read3Lines():
    lines = []
    index = 1
    with open('input.txt','r') as f:
        for l in f.readlines():
            lines.append(l.strip())
            if index % 3 == 0:
                yield lines
                lines = []
            index += 1





for l1,l2,l3 in read3Lines():
    s1 = set(l1)
    s2 = set(l2)
    s3 = set(l3)
    i = list(s1.intersection(s2).intersection(s3))[0]
    sum += priority(i)

            

print(sum)