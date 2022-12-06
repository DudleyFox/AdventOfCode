"""
Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
For example:

qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.
How many strings are nice under these new rules?
"""

sum = 0

def hasPairs(s):
    pairs = {}
    for x in range(0, len(s) - 1):
        p = s[x:x+2]
        if p in pairs:
            pairs[p].add(x)
            pairs[p].add(x+1)
        else:
            pairs[p] = set((x, x+1))
    for k,v in pairs.items():
        if len(v) >= 4:
            return True
    return False

def repeatsApart(s):
    t = s + '00' # just pad the end
    for x in range(len(s)):
        if t[x] == t[x+2]:
            return True
    return False

def isNice(s):
    withPairs = hasPairs(s)
    return (withPairs and repeatsApart(s) and 1) or 0

with open('input.txt','r') as f:
    for l in f.readlines():
        sum += isNice(l.strip())

print (sum)

print(f'qjhvhtzxzqqjkmpb: { isNice("qjhvhtzxzqqjkmpb") }')
print(f'xxyxx: { isNice("xxyxx") }')
print(f'aaa: { isNice("aaa") }')
print(f'uurcxstgmygtbstg: {isNice("uurcxstgmygtbstg")}')
print(f'ieodomkazucvgmuy: {isNice("ieodomkazucvgmuy")}')