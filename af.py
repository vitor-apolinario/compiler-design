import csv
arquivo = list(open('tokens.txt'))

simbolos    = []
estados     = []
inalcan     = []
mortos      = []
gramatica   = {}
tabela      = {}
epTransicao = {}
repeticao = 0

def eliminarEpTransicao():
    for regra in tabela:
        if tabela[regra]['*'] != []:
            if regra not in epTransicao:
                epTransicao[regra] = tabela[regra]['*']
            else:
                epTransicao[regra] += tabela[regra]['*']

    for x in epTransicao:
        for y in epTransicao:
#            print(y.split(), epTransicao[x])
            if y in epTransicao[x]:
                epTransicao[x] += epTransicao[y]

    print("\n\nEp: ", epTransicao)
    for conjunto in epTransicao:
        for tran in tabela[conjunto]:
            for epT in epTransicao[conjunto]:
                tabela[conjunto][tran] += tabela[epT][tran]
                if tran == '*':
                    tabela[conjunto][tran] = [ ]
    print("Tab2: ", tabela)

def criarAF():
    for x in gramatica:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['*'] = []       # coluna do epsilon verificar
#    print('Tabela: ', tabela)

    for regra in gramatica:
        for transicao in gramatica[regra]:
            #print("T: ", transicao)
            if len(transicao) == 1 and transicao.islower():                                                             # somente 1 terminal
                tabela[regra][transicao].append('X')
            elif transicao[0] == '<':                                                                                   # somente 1 regra (epsilon transição)
                tabela[regra]['*'].append(transicao.split('<')[1][:-1])
            elif transicao != '*':                                                                                      # caso geral
                tabela[regra][transicao[0]].append(transicao.split('<')[1][:-1])

    print('\nTabela: ', tabela)


def criaSn(S):
    global repeticao
    if 'S' + str(repeticao) in gramatica:                                                                               # se já houver Sn na gramatica abortar
        return
    gramatica['S' + str(repeticao)] = S.replace('\n','').split(' ::= ')[1].replace('>',str(repeticao)+'>').split(' | ')


def trataEstS(sentenca, op, proxregra):
    global repeticao
    repeticao += 1
    sentenca = sentenca.replace('\n','')
    if 'S' in gramatica and op == 'G':
        gramatica['S'] += sentenca.split(' ::= ')[1].replace('>',str(repeticao)+'>').split(' | ')
    elif 'S' not in gramatica and op == 'G':
        gramatica['S'] =  sentenca.split(' ::= ')[1].replace('>',str(repeticao)+'>').split(' | ')
    elif 'S' in gramatica and op == 'T':
        gramatica['S'] += str(sentenca + proxregra).split()
    elif 'S' not in gramatica and op == 'T':
        gramatica['S'] = str(sentenca + proxregra).split()
    # print("GP: ", gramatica)
    

def trataGram(gram , S):                                                                                                # Função usada para tratar gramáticas
    for x in gram.split(' ::= ')[1].replace('\n', '').split(' | '):
        if x[0] not in simbolos and x[0].islower():
            simbolos.append(x[0])
    regra = gram.split(' ::= ')[0].replace('>', str(repeticao)).replace('<', '')                                        # Adiciona o nome da regra à gramática

    if '<S> ::=' in gram:
        trataEstS(gram, 'G', 'essa string nao eh usada')
        if '<S>' in gram.replace('\n', '').split(' ::= ')[1]:
            criaSn(S)
    else:
        if '<S>' in gram.replace('\n', '').split(' ::= ')[1]:
            criaSn(S)
        gramatica[regra] = gram.replace('\n','').split(' ::= ')[1].replace('>',str(repeticao)+'>').split(' | ')         # Adiciona as transições à gramática
#    print('Gramática: ', gramatica)


def trataToken(token):                                                                                                  # Função usada para tratar tokens
    cop = token.replace('\n','')
    token = list(token)
    if '\n' in token:
        token.remove('\n')
    for x in range(len(token)):
        # print("Token: ", token[x])
        if token[x] not in simbolos and token[x].islower():                                                             # Se o símbolo ainda não existe, adiciona
            simbolos.append(token[x])
            
        if x == 0:
            regra = '<' + cop.upper() + '1>'
        else:
            regra = '<' + cop.upper() + str(x) + '>'

        # é possível um token onde |token| = 1? se sim, falta tratar
        if x == 0 and x != len(token)-1:                                                                                # Se for o primeiro e não último
            trataEstS(token[x], 'T', regra)
        elif x == len(token)-1:                                                                                         # Se for o ultimo, é terminal e não leva à outro estado
            gramatica[regra] = str(token[x] + '<' + cop.upper() + '*>').split()
            gramatica['<' + cop.upper() + '*>'] = []
        # pelo que me parece o caso abaixo não deve acontecer
        elif regra in gramatica:                                                                                        # (??) Se a regra já existir será concatenada com simbolo+SIMBOLO+repeticao (??)
            gramatica[regra] += str(token[x] + token[x].upper() + str(repeticao)).split()
        else:                                                                                                           # se for um token entre o primeiro e o ultimo => token+proximaregra
            gramatica[regra] = str(token[x]+ '<' + cop.upper() + str(x+1) + '>' ).split()


def criarArquivo():
    with open('afnd.csv', 'w', newline='') as f:
        # fields = ['nomeregra'] + list(tabela['S'].keys())
        w = csv.writer(f)
        copydict = tabela.copy()
        w.writerow(list(copydict['S'].keys()) + ['regra'])
        for x in copydict:
            copydict[x]['nomeregra'] = x
            w.writerow(copydict[x].values())


def main():
    estadoinicial = ''
    for x in arquivo:
        if '<S> ::=' in x:
            estadoinicial = x
        if '::=' in x:
            trataGram(x, estadoinicial)
#           print('Gramática: ', x)
        else:
#           print("Token: ", x)
            trataToken(x)
    criarAF()
    eliminarEpTransicao()


    print('Simbolos')
    print(simbolos)
    print('Estados')
    print(estados)
    print('Gramática')
    print(gramatica)
    # print('Tabela')
    # print(tabela)

    criarArquivo()


main()


# gramatica exemplo
# if
# <S> ::= a<A> | b<B>
# <A> ::= x
# <B> ::= z
# else

# se
# entao
# senao
# <S> ::= a<A> | e<A> | i<A> | o<A> | u<A>
# <A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | *

#se
#entao
#senao
#<S> ::= a<A> | e<A> | i<A> | o<A> | u<A> | <A>
#<A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | *

#<S> ::= a<S> | <A>
#<A> ::= b<A> | <B>
#<B> ::= c<B> | *