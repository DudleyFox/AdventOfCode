
keyWords = set((
'AND',
'OR',
'NOT',
'RSHIFT',
'LSHIFT',
'->'
))


# grammar
# <expression> ::= <input> '->' <wire>
# <input> ::= <wire> <bgate> <number> | <wire> <bgate> <wire> | <ugate> <wire> | <number>
# <bgate> ::= 'AND' | 'OR' | 'RSHIFT' | 'LSHIFT'
# <ugate> ::= 'NOT'
# <wire> ::= [a-z]+
# <number> ::= [0-9]+


