

def readSums():
    with open('input.txt','r') as f:
        sum = 0
        for l in f.readlines():
            line = l.strip()
            if line:
                sum += int(line)
            else:
                yield sum
                sum = 0



if __name__ == '__main__':
    m = 0
    for s in readSums():
        m = max(m, s)

    print(m)