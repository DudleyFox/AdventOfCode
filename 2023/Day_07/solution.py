import sys
from functools import cmp_to_key

cardStrength = '23456789TJQKA'

def getCardStrength(c):
    return cardStrength.find(c)

def getStrength(hand):
    d = {}
    for c in hand:
        d[c] = d.get(c, 0) + 1
    count = len(d.keys())
    l = list(d.values())
    l.sort()
    t = tuple(l)
    if t == (5,):
        print('boom!')
        return 7
    elif t == (1,4):
        return 6
    elif t == (2,3):
        return 5
    elif t == (1,1,3):
        return 4
    elif t == (1,2,2):
        return 3
    elif t == (1,1,1,2):
        return 2
    return 1

def compareHands(a,b):
    if a[2] < b[2]:
        return -1
    if a[2] > b[2]:
        return 1
    for x in range(5):
        cs1 = getCardStrength(a[0][x])
        cs2 = getCardStrength(b[0][x])
        # print(f"{a[0][x]}:{cs1} {b[0][x]}:{cs2}")
        if cs1 < cs2:
            return -1
        if cs1 > cs2:
            return 1

    return 0
    


def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            if l != '':
                cards, bid = l.split(' ')
                yield (cards, int(bid))


if __name__ == "__main__":
    cards = [x for x in readLines(sys.argv[1])]
    cards = list(map(lambda c: (c[0], c[1], getStrength(c[0])), cards))
    cards.sort(key=cmp_to_key(compareHands))
    # print (cards)

    index = 1
    winnings = 0
    for c in cards:
        # print(c)
        winnings = winnings + index * c[1]
        index += 1

    print(winnings)