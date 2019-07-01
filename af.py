arquivo = list(open('tokens.txt'))

simbolos = []
estados  = [] 
gramatica = {}
tabela = {}
repeticao = 0

def criarAFND(): 
    for x in gramatica:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
#    print('Tabela: ', tabela)

    for regra in gramatica:
        for transicao in gramatica[regra]:
            if len(transicao) == 1 and transicao.islower():
                tabela[regra][transicao].append('X')
            elif transicao != '*':
                tabela[regra][transicao[0]].append(transicao[1]+str(repeticao))
    print('\nTabela: ', tabela)
    

def trataEstS(sentenca, op):            # Função utilizada para acoplar todos os estados iniciais em um só, a distinção é realizada com o valor REPETIÇÃO
    global repeticao
    repeticao += 1
    if 'S' in gramatica and op == 'G':
        gramatica['S'] += sentenca.replace('\n','').split(' ::= ')[1].split(' | ')
    elif 'S' not in gramatica and op == 'G':
        gramatica['S'] = sentenca.replace('\n','').split(' ::= ')[1].split(' | ')
    elif 'S' in gramatica and op == 'T':
        gramatica['S'] += str(sentenca+sentenca.upper()+str(repeticao)).split()
    elif 'S' not in gramatica and op == 'T':
        gramatica['S'] = str(sentenca+sentenca.upper()+str(repeticao)).split()
#    print("GP: ", gramatica)    
    

def trataGram(gram):                                                            # Função usada para tratar gramáticas
    for x in gram.split(' ::= ')[1].replace('\n', '').split(' | '):             # Adiciona os símbolos de 1 gramática
        if x[0] not in simbolos and x[0].islower():
            simbolos.append(x[0])
    regra = gram.split(' ::= ')[0].replace('<', '').replace('>', '')+str(repeticao) # Adiciona o nome da regra à gramática
    if '<S> ::=' in gram:
        trataEstS(gram, 'G')
    else:
        gramatica[regra] = gram.replace('\n','').split(' ::= ')[1].split(' | ')         # Adiciona as transições à gramática  

#    print('Gramática: ', gramatica)



def trataToken(token):                                                            # Função usada para tratar tokens
    token = list(token)
    token.remove('\n')
    for x in range(len(token)):
        print("Token: ", token[x])
        if token[x] not in simbolos and token[x].islower():                                 # Se o símbolo ainda não existe, adiciona
            simbolos.append(token[x])
            
        regra = token[x-1].upper()+str(repeticao)                                           # Nome da regra é o anterior em Maiusculo + Repeticao
        if x == 0:                                                                          # Se for o primeiro, pertence ao estado S
            trataEstS(token[x], 'T')
        elif x == len(token)-1:                                                             # Se for o ultimo, é terminal e não leva à outro estado
            gramatica[regra] = token[x].split()
        elif regra in gramatica:                                                            # Se a regra já existir será concatenada com simbolo+SIMBOLO+repeticao
            gramatica[regra] += str(token[x]+token[x].upper()+str(repeticao)).split()
        else:                                                                               # Se a regra não existir será criada com simbolo+SIMBOLO+repeticao
            gramatica[regra] = str(token[x]+token[x].upper()+str(repeticao)).split()

def main():
    for x in arquivo:
        if '::=' in x:          
            trataGram(x)
#            print('Gramática: ', x)
        else:
 #           print("Token: ", x)
            trataToken(x)
#    print('Simbol: ', simbolos)
#    criarAFND()


main()
