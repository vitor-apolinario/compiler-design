import csv
import copy
arquivo = list(open('tokens.txt'))

simbolos    = []
estados     = []
inalcan     = []
mortos      = []
novos       = []
gramatica   = {}
tabela      = {}
epTransicao = {}
repeticao = 0


def criaNovos(nstates):
    for x in nstates:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['*'] = []

    for state in nstates:
        estadosjuntar = sorted(state.split(':'))
        for x in estadosjuntar:
            if x == 'X':                                                                                                # X ainda não nos é útil
                continue
            for simbolo in simbolos:
                for transition in tabela[x][simbolo]:
                    if not tabela[state][simbolo].__contains__(transition):
                        tabela[state][simbolo].append(transition)
    determizina()


def determizina():
    novosestados = []
    for regra in tabela:
        for producao in tabela[regra]:
            if len(tabela[regra][producao]) > 1:
                print('indeterminismo em: regra', regra, '; produzindo', producao, ' -> ', tabela[regra][producao], 'ele virará um novo estado')
                novo = ''
                for estado in tabela[regra][producao]:                                                                  # concatena para saber o nome do novo estado
                    novo += estado  + ':'
                novo = novo[:-1]                                                                                        # remove : do final
                if not novosestados.__contains__(novo) and novo:                                                        # (if '') retorna falso
                    novosestados.append(novo)
                tabela[regra][producao] = novo.split()
    if novosestados:
        criaNovos(novosestados)


def eliminarEpTransicao():
    for regra in tabela:
        if tabela[regra]['*'] != []:
            if regra not in epTransicao:
                epTransicao[regra] = tabela[regra]['*']
            else:
                epTransicao[regra] += tabela[regra]['*']

    for x in epTransicao:
        for y in epTransicao:
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

    for regra in gramatica:
        for transicao in gramatica[regra]:
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


def trataToken(token):                                                                                                  # Função usada para tratar tokens
    cop = token.replace('\n','')
    token = list(token)
    if '\n' in token:
        token.remove('\n')
    for x in range(len(token)):
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
        copydict = copy.deepcopy(tabela)
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
        else:
            trataToken(x)
    criarAF()
    # eliminarEpTransicao()
    determizina()
    criarArquivo()
    # print('Simbolos')
    # print(simbolos)
    # print('Estados')
    # print(estados)
    # print('Gramática')
    # print(gramatica)
    # print('Tabela')
    # print(tabela)


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