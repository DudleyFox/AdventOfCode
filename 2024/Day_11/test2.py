import sys
from functools import reduce


def shouldSplit(n):
    sLen = len(str(n))
    return sLen % 2 == 0

def splitInTwo(n):
    s = str(n)
    l = len(s);
    result = []
    result.append(int(s[0:l//2]))
    result.append(int(s[l//2:]))
    return result

def countDigits(n):
    return len(str(n));

def add(a,b):
    return a + b;

def blink(input):
    print("");
    print("Blinking:", input);
    max = 75
    count = 0
    t = list(input)
    newStones = []
    print(",".join([str(x) for x in t]), f"({len(t)})")
    while count < max:
        for x in t:
            if x == 0:
                newStones.append(1)
            elif shouldSplit(x):
                r = splitInTwo(x)
                newStones.append(r[0])
                newStones.append(r[1])
            else:
                newStones.append(x*2024)
        t = newStones
        newStones = []
        if len(t) < 10:
            print(",".join([str(x) for x in t]), f"({len(t)})")
        else:
            print(f"{count} ({len(t)})")

        total = reduce(add, list(map(countDigits, t)))
        if total == len(t): return # all values have one digit
        count += 1





if __name__ == "__main__":
        blink([int(sys.argv[1]),])


