data = ''

def popcnt(i):
    # if 4 bits are set we have 4 unique letters
    return bin(i).count('1')

def letterToNumber(letter):
    # a is bit 0, b is bit 1, and so on.
    return 1 << (ord(letter) - ((ord('a'))))

with open('input.txt', 'r') as f:
    data = f.read().strip()

dataLength = len(data)

print('Datalength:', dataLength)

for index in range(3, dataLength):
    s = data[index-3:index+1]
    print(s)
    letters = 0
    for x in s:
        letters = letters | letterToNumber(x)
        if popcnt(letters) == 4:
            print(index+1)
            exit(0)