import sys

class ScratchCard:
    def __init__(self, s):
        self.score = 0
        self.cardNo, lists = s.split(':')
        self.cardNo = int(self.cardNo.replace('Card', '')) - 1
        winners, haves = lists.split('|')
        self.winners = [int(x) for x in winners.strip().split(' ') if x != '']
        self.have  = [int(x) for x in haves.strip().split(' ') if x != '']
        self.computeCount()
        self.copies = 1 # always count yourself

    def __str__(self):
        s = ''
        s += self.cardNo + '\n'
        s += f"\t{self.winners}|{self.have}\n"
        s += f"\t{self.score}"
        return s
    
    def computeCount(self):
        winnerSet = set(self.winners)
        count = 0
        for x in self.have:
            if x in winnerSet:
                count += 1
        self.count = count

    def process(self, cards):
        for y in range(self.copies):
            for x in range(self.count):
                c = cards[self.cardNo+1+x]
                c.copies += 1

def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield ScratchCard(l)


if __name__ == "__main__":
    cards = [x for x in readLines(sys.argv[1])]
    for c in cards:
        c.process(cards)
    copies = list(map(lambda x: x.copies, cards))
    print(sum(copies))
