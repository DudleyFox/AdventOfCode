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

def countPaths(deviceMap, start):
    print("Counting:", start)
    count = 0
    if start == 'out': # we made it
        return 1
    for x in deviceMap[start]:
        count += countPaths(deviceMap, x)
    return count


if __name__ == "__main__":
    deviceMap = readConnections(sys.argv[1])

    for key in deviceMap:
        print(f'{key}: {" ".join(deviceMap[key])}')

    print(countPaths(deviceMap, 'you'))

    


