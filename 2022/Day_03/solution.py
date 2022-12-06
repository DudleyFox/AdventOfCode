
sum = 0

def priority(c):
    o = ord(c)
    if o > 90:
        return o - 96
    return o - 38

with open('input.txt','r') as f:
        for l in f.readlines():
            line = l.strip()
            lgth = len(line)//2
            c1 = line[:lgth]
            c2 = line[lgth:]
            s1 = set(c1)
            s2 = set(c2)
            i = list(s1.intersection(s2))[0]
            sum += priority(i)

print(sum)