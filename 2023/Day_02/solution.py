import sys
from functools import reduce

bagConstraint = {
    'red':12,
    'green':13,
    'blue':14
}

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
    possible = True
    for x in bagConstraint.keys():
        possible = possible and bagConstraint[x] >= maxColors[x]
    return gameId, possible



def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield l


if __name__ == "__main__":
    # print(sys.argv[1])
    gInfo = [buildGameInfo(x) for x in readLines(sys.argv[1])]
    # print(gInfo)
    possibleGames = filter(lambda x: x[1], gInfo)
    gameIndices = map(lambda x: x[0], possibleGames)
    print(sum(gameIndices))