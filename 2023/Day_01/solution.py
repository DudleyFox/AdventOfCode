
digits = set('0123456789')

def getFirstDigit(s):
    for c in s:
        if c in digits:
            return c

def getLastDigit(s):
    return getFirstDigit(s[::-1])



def readLines():
    with open('input.txt', 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield l


if __name__ == "__main__":
    coordinates = []
    for l in readLines():
        print(l)
        coordinates.append(int(getFirstDigit(l)+getLastDigit(l)))

    print (sum(coordinates)) 
