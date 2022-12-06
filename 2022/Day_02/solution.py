"""
"The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
"""

rock = 'rock'
paper = 'paper'
scissors = 'scissors'

symbols = {
    'A':rock,
    'B':paper,
    'C':scissors,
    'X':rock,
    'Y':paper,
    'Z':scissors,
}

pointValues = {
    rock: 1,
    paper: 2,
    scissors: 3,

    (rock,rock): 3,
    (rock,scissors): 0,
    (rock,paper): 6,

    (scissors,scissors): 3,
    (scissors,rock): 6,
    (scissors,paper): 0,

    (paper,paper): 3,
    (paper,rock): 0,
    (paper,scissors): 6,
}

def translateSymbol(s):
    return symbols[s]

def scoreRound(p1,p2):
    return pointValues[p2] + pointValues[(p1,p2)]

def readAndTranslate():
    with open('input.txt', 'r') as f:
        for x in f.readlines():
            p1, p2 = x.strip().split(' ')
            yield (translateSymbol(p1), translateSymbol(p2))


if __name__ == '__main__':
    sum = 0
    for p1, p2 in readAndTranslate():
        sum += scoreRound(p1,p2)
    print(sum)