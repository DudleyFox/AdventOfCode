"""
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
"""
    # rock: 1,
    # paper: 2,
    # scissors: 3,

pointValues = {
    ('A','X'): 3, # lose to Rock, play scissor, worth 3
    ('A','Y'): 1, # draw with rock, play rock, worth 1
    ('A','Z'): 2, # win against rock, play paper, worth 2
    ('B','X'): 1, # lose to paper, play rock, worth 1
    ('B','Y'): 2, # draw with paper, play paper, worth 2
    ('B','Z'): 3, # win against paper, play scissors, worth 3
    ('C','X'): 2, # lose to scissors, play paper, worth 2
    ('C','Y'): 3, # draw with scissors, play scissors, worth 3
    ('C','Z'): 1, # win against scissors, play rock, worth 1
    'X':0, # Lose
    'Y':3, # Draw
    'Z':6, # Win
}

def translateSymbol(s):
    return symbols[s]

def scoreRound(p1,p2):
    return pointValues[p2] + pointValues[(p1,p2)]

def readAndScore():
    with open('input.txt', 'r') as f:
        for x in f.readlines():
            p1, p2 = x.strip().split(' ')
            yield scoreRound(p1,p2)


if __name__ == '__main__':
    sum = 0
    for s in readAndScore():
        sum += s 
    print(sum)