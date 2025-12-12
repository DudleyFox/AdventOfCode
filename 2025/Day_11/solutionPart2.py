import sys
import math

def readConnections(filename):
    deviceMap = {}
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            key, outputs = line.split(": ")
            deviceMap[key] = []
            for output in outputs.split(" "):
                deviceMap[key].append(output)
    return deviceMap

def cloneSet(aSet):
    return set([x for x in aSet])

def cloneList(aList):
    return [x for x in aList]

def buildSeenKey(start, end):
    return f"{start}->{end}"

def countPaths(deviceMap, start, end, currentPath, listPath, depth, seen):
    if start in currentPath:
        print("Loop")
        exit(0)
        return 0 # circular
    listPath.append(start)
    currentPath.add(start)
    count = 0
    if start == 'out' and end != 'out':
        return 0
    if start == end: # we made it
        return 1
    outputs = deviceMap[start]
    print("Testing:", listPath)
    seenKey = buildSeenKey(start, end)
    if seenKey in seen:
        return seen[seenKey]
    for x in outputs:
        result = countPaths(deviceMap, x, end, cloneSet(currentPath), cloneList(listPath), depth + 1, seen)
        count += result
    seen[seenKey] = count
    return count


if __name__ == "__main__":
    deviceMap = readConnections(sys.argv[1])

    for key in deviceMap:
        print(f'{key}: {" ".join(deviceMap[key])}')

    srvToFft = countPaths(deviceMap, 'svr', 'fft', set(), [], 0, {})
    fftToDac = countPaths(deviceMap, 'fft', 'dac', set(), [], 0, {})
    dacToOut = countPaths(deviceMap, 'dac', 'out', set(), [], 0, {})
    print(f'srv->fft({srvToFft}) fft->dac({fftToDac}) dac->out({dacToOut}): {srvToFft*fftToDac*dacToOut}')

    


