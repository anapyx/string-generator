import re
import sys
from pathlib import Path

if len(sys.argv) <= 1:
  print("Passe o caminho do arquivo de teste corretamente")
  exit()
file_to_open = sys.argv[1]

with open(file_to_open) as file:
    Lines = file.readlines()

Lines.remove('\n')
Lines.remove('producoes\n')

print('leu o arquivo')
print(Lines)

prod_list = [] 
variables = None # list with non terminals symbols
initial_var = None
terminals = None
productions = {}
start_read_productions = False

# get variables from file

for line in Lines:
    # to remove every tab, space and new line
    line = re.sub(r'[\n\t\s]*', '', line)

    if line.startswith('variaveis'):
        line = line.replace('variaveis','')
        line = line.replace(':','')
        variables = line.split(',')

    elif line.startswith('inicial'):
        initial_var = line.replace('inicial','')
        initial_var = initial_var.replace(':','')

    elif line.startswith('terminais'):
        terminals = line.strip()
        terminals = terminals.replace('terminais','')
        terminals = terminals.replace(':','')
        terminals = terminals.split(',')
    elif line:
        prod_list.append(line.strip())

print('separou as partes')
print(variables)
print(initial_var)
print(prod_list)


prod_list = tuple(prod_list)

for prod in prod_list:
    if prod.startswith(prod_list):
        prod = prod.split(':')
        productions.setdefault(prod[0], [])
        productions[prod[0]].append(prod[1])

print('gerou producoes')
print(productions)

def validEntries():
    flags = []
    output = True

    if len(variables) < 1:
       flags.append(1)
       output = False

    if (not initial_var.isalpha()) and (not(initial_var in variables)) and (not len(initial_var) == 1):
       flags.append(2)
       output = False

    if len(terminals) < 1:
       flags.append(3)

    for key in productions.keys():
       if key not in variables:
          flags.append(4)
          output = False

    return output, flags

validation, validation_flags = validEntries()
print(validation)
print(validation_flags)

# FAST MODE


def fast_mode():
    continue_fast_mode = True
    while continue_fast_mode:
        chain = ""
        chain_path = []
        chain_path.append("epsilon")
        epsilon_possibility = None
        for x in productions:
            for y in productions[x]:
                if y == "epsilon":
                    chain_path.append(x)
                    break
            if len(chain_path) != 0:
                break   
        i = 1

        while chain_path[i - 1] != initial_var:
            for x in productions:
                for y in productions[x]:
                    if chain_path[i - 1] in y:
                        chain_path.append(x)
                        i += 1
                        break
                if chain_path[i - 1] == initial_var:
                    break 

        print("Derivacao:")
        chain_sub_str = []
        chain_sub_str.append(str(chain_path[len(chain_path) - 1]) + " -> ")
        chain += chain_sub_str[0]
        j = 0
        for i in range(len(chain_path)-1, 0, -1):
            for x in productions[chain_path[i]]:
                if chain_path[i - 1] in x:
                    match = re.search(r'(.*?)(?= ->)', chain_sub_str[j])
                    if match:
                        if "epsilon" in x:
                            x = ""
                            aux = match.group(0).replace(chain_path[i], x, 1)
                            chain_sub_str.append(aux)
                        else:
                            aux = match.group(0).replace(chain_path[i], x, 1)
                            chain_sub_str.append(aux + " -> ")
                        j += 1
                        chain += chain_sub_str[j]   

        print(chain)    
        print("Cadeia gerada:")
        print(chain_sub_str[len(chain_sub_str) - 1])  

        print("\nDeseja gerar outra cadeia? (s/n)")
        keep = input()
        if keep.lower() != 's':
            continue_fast_mode = False


# DETAILED MODE    
def detailed_mode():
    chain_sub_str = initial_var + " -> "
    chain = chain_sub_str
    current_variable = None
    print("Derivacao:")
    print(chain)    

    while any(j.isupper() for j in chain_sub_str):
        for i in chain_sub_str:
          if i.isupper():
            current_variable = i
            break
        print(f"\nEscolha a operacao de {current_variable}: ")
        print(productions[current_variable])
        operation = input()
        operacao_valida = False
        for x in productions[current_variable]:
            if operation in x:
                operacao_valida = True
                break
        if operacao_valida:
            match = re.search(r'(.*?)(?= ->)', chain_sub_str)
            if match:
                if operation == "epsilon":
                  operation = ""
                aux = match.group(0).replace(current_variable, operation, 1)
                chain_sub_str = aux + " -> "
                chain += chain_sub_str
                print(chain)
        else:
            print("Operacao invalida!") 

    print("\nCadeia gerada:")
    print(chain_sub_str[:-4])    


# MENU 

running = True
while running:
    print('\n----- Gerador de Gramáticas Livres de Contexto -----\n')
    print('Selecione o path do seu arquivo e escolha o modo do gerador:')
    print('1. Modo rapido')
    print('2. Modo detalhado')
    print('3. Sair')
    menu = input()

    if menu == '1':
        print ('\n--- Modo Rápido ---')
        fast_mode()
    if menu == '2':
        print ('\n--- Modo Detalhado ---')
        detailed_mode()
    if menu == '3':
       running = False
