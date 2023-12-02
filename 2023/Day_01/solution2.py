
digits = set('0123456789')
words = {
    'one':'1',
    'two':'2',
    'three':'3',
    'four':'4',
    'five':'5',
    'six':'6',
    'seven':'7',
    'eight':'8',
    'nine':'9'
}

wordSet = set(words.keys())

def isWord(w,s,i):
    return w == s[i:i+len(w)]

def getFirstDigit(s):
    for i in range(len(s)):
        c = s[i]
        if c in digits:
            return c
        for w in words.keys():
            if isWord(w,s,i):
                return words[w]

def getLastDigit(s):
    for i in range(len(s)-1,-1,-1):
        c = s[i]
        if c in digits:
            return c
        for w in words.keys():
            if isWord(w,s,i-((len(w)-1))):
                return words[w]



def readLines():
    with open('input.txt', 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield l


if __name__ == "__main__":
    coordinates = []
    for l in readLines():
        coordinates.append(int(getFirstDigit(l)+getLastDigit(l)))

    # print(coordinates)
    print (sum(coordinates)) 
