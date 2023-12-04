import sys

class ScratchCard:
    def __init__(self, s):
        self.score = 0
        self.cardNo, lists = s.split(':')
        winners, haves = lists.split('|')
        self.winners = [int(x) for x in winners.strip().split(' ') if x != '']
        self.have  = [int(x) for x in haves.strip().split(' ') if x != '']
        self.computeScore()

    def __str__(self):
        s = ''
        s += self.cardNo + '\n'
        s += f"\t{self.winners}|{self.have}\n"
        s += f"\t{self.score}"
        return s
    
    def computeScore(self):
        self.score = 0
        winnerSet = set(self.winners)
        count = 0
        for x in self.have:
            if x in winnerSet:
                count += 1
        if (count > 0):
            self.score = 2**(count - 1)

def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield ScratchCard(l)


if __name__ == "__main__":
    cards = [x for x in readLines(sys.argv[1])]
    scores = list(map(lambda x: x.score, cards))
    print(sum(scores))
