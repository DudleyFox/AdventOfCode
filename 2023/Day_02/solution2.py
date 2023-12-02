import sys
from functools import reduce

def buildMaxColors(s):
    maxColors = {
        'red':0,
        'green':0,
        'blue':0
    }
    draws = [d.strip() for d in s.split(',')]
    for x in draws:
        count, color = x.split(' ')
        count = int(count)
        maxColors[color] = max(count, maxColors[color])
    return maxColors
    

def buildGameInfo(g):
    game, games = g.split(':')
    gameId = int(game[5:])
    games = games.replace(';',',')
    maxColors = buildMaxColors(games)
    power = 1
    for x in maxColors.keys():
        power = power * maxColors[x]
    return gameId, power



def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield l


if __name__ == "__main__":
    # print(sys.argv[1])
    gInfo = [buildGameInfo(x) for x in readLines(sys.argv[1])]
    # print(gInfo)
    gameIndices = map(lambda x: x[1], gInfo)
    print(sum(gameIndices))