import sys

def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield l

def calculateWaysToWin(raceTime, currentBest):
    speed = 0
    wins = 0
    for x in range(raceTime + 1):
        timeLeft = raceTime - x
        distance = timeLeft * speed
        print(f"{x}:{timeLeft}:{distance} - {raceTime}:{currentBest}")
        if (distance > currentBest):
            wins += 1
        speed += 1
    return wins


if __name__ == "__main__":
    lines = [x for x in readLines(sys.argv[1])]
    times = [int(x) for x in lines[0].split(':')[1].split(' ') if x != '']
    distances = [int(x) for x in lines[1].split(':')[1].split(' ') if x != '']
    wins = 1
    for x in range(len(times)):
        wins = wins * calculateWaysToWin(times[x],distances[x])
    print (wins)
    