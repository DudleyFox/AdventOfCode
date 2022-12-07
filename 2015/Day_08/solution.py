
# 1448 too high
# 1312 too low

def readData():
    # return '"""abc""aaa\\"aaa""\\x27""\\\\"'
    data = ''
    with open('input.txt', 'r') as f:
        data = f.read().replace('\n','')
    return data

def cleanData(data):
    cleaned = []
    skip = 0
    last = ''
    for x in data:
        if skip > 0:
            skip -= 1
        elif x == 'x' and last == '\\':
            skip = 2
            cleaned.append('h') # just for the count, we should really grab the next two characters 
        elif x == '"' and last == '\\':
            cleaned.append(x)
        elif x == '\\' and last == '\\':
            cleaned.append(x)
            x = '' # so we don't accidently escape the next character
        elif x == '\\' or x == '"':
            pass
        else:
            cleaned.append(x)
        last = x
    return ''.join(cleaned)


def computeDifference(data):
    codeLength = len(data)
    clean = cleanData(data)
    cleanLength = len(clean)
    print(data)
    print('***************************')
    print(clean)
    return codeLength - cleanLength

if __name__ == '__main__':
    diff = computeDifference(readData())
    print(diff)