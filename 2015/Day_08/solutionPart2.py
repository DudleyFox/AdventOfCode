
# 1448 too high
# 1312 too low

def readData():
    # return '"""abc""aaa\\"aaa""\\x27""\\\\"'
    # return ['""','"abc"','"aaa\\"aaa"','"\\x27"']
    data = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            data.append(l.strip())
    return data

def expandData(data):
    expandedData = []
    for x in data:
        ex = '"' + x.replace('\\',r'\\').replace('"','\\"') + '"'
        expandedData.append(ex)
    return expandedData

def countData(d):
    return sum([len(x) for x in d])

def computeDifference(data):
    dataLength = countData(data)
    expandedData = expandData(data)
    eLength = countData(expandedData)
    print(dataLength)
    print(eLength)
    return eLength - dataLength

if __name__ == '__main__':
    diff = computeDifference(readData())
    print(diff)