import re

# reading file and removing non useful lines

with open('grammar.txt') as file:
    Lines = file.readlines()

Lines.remove('\n')
Lines.remove('producoes\n')

prod_list = []

# get variables from file

for line in Lines:
    # to remove every tab, space and new line
    line = re.sub(r'[\n\t\s]*', '', line)

    if line.startswith('variaveis'):
        line = line.replace('variaveis','')
        line = line.replace(':','')
        nonterminal = line.split(',')

    elif line.startswith('inicial'):
        start = start.replace('inicial','')
        start = start.replace(':','')

    elif line.startswith('terminais'):
        terminal = line.strip()
        terminal = terminal.replace('terminais','')
        terminal = terminal.replace(':','')
        terminal = terminal.split(',')
    elif line:
        prod_list.append(line.strip())

productions = {}
prod_list = tuple(prod_list)

for prod in prod_list:
    if prod.startswith(prod_list):
        prod = prod.split(':')
        productions.setdefault(prod[0], [])
        productions[prod[0]].append(prod[1])

# nonterminal is a list with nonterminal symbols
# start is the starting nonterminal symbol
# terminal is a list of the terminal symbols
# productions is a dict of all the possible productions