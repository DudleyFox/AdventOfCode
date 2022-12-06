"""
A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
For example:

ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
jchzalrnumimnmhp is naughty because it has no double letter.
haegwjzuvuyypxyu is naughty because it contains the string xy.
dvszwmarrgswjxmb is naughty because it contains only one vowel.
How many strings are nice?
"""

sum = 0
vowels = set(('a','e','i','o','u'))
forbiddenPairs = set(('ab', 'cd', 'pq', 'xy'))

def isVowel(v):
    return (v in vowels and 1) or 0

def isNice(s):
    vowelCount = 0
    hasDouble = False
    last = ''
    for c in s:
        vowelCount += isVowel(c)
        hasDouble = hasDouble or last == c
        if last + c in forbiddenPairs:
            return 0
        last = c

    return (hasDouble and vowelCount >= 3 and 1) or 0



with open('input.txt','r') as f:
    for l in f.readlines():
        sum += isNice(l.strip())

print (sum)

print(f'ugknbfddgicrmopn: { isNice("ugknbfddgicrmopn") }')
print(f'aaa: { isNice("aaa") }')
print(f'jchzalrnumimnmhp: {isNice("jchzalrnumimnmhp")}') # is naughty because it has no double letter.
print(f'haegwjzuvuyypxyu: {isNice("haegwjzuvuyypxyu")}') # is naughty because it contains the string xy.
print(f'dvszwmarrgswjxmb: {isNice("dvszwmarrgswjxmb")}') # is naughty because it contains only one vowel.