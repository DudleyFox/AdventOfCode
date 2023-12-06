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
        # print(f"{x}:{timeLeft}:{distance} - {raceTime}:{currentBest}")
        if (distance > currentBest):
            wins += 1
        speed += 1
    return wins


if __name__ == "__main__":
    lines = [x for x in readLines(sys.argv[1])]
    time =  int(lines[0].replace(' ','').split(':')[1])
    distance = int(lines[1].replace(' ','').split(':')[1])

    wins = calculateWaysToWin(time,distance)
    print (wins)
    