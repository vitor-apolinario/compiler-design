import csv
import copy
arquivo = list(open('tokens.txt'))

simbolos    = []
estados     = []
alcan       = []
mortos      = []
novos       = []
gramatica   = {}
tabela      = {}
epTransicao = {}
repeticao = 0

def eliminarInal():                         # Percorre a tabela e remove quem não estiver na lista de alcançáveis
    loop = {}
    loop.update(tabela)
    for regra in loop:
        if regra not in alcan:
            del tabela[regra];
                

def buscarAlcan(estado):                    # Percorre os estados da tabela recursivamente e se em suas transações ainda tiver um estado que não está em alcan
    if estado not in alcan:         
        alcan.append(estado)
        for tran in tabela[estado]:
            if str(tabela[estado][tran])[2:-2] != '':
                buscarAlcan(str(tabela[estado][tran])[2:-2])


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


def criaNovos(nstates):
    loop = []
    loop.extend(nstates)                                                         # Necessário para evitar o problema de alterar o for in e não percorrer todos os valores
    for x in loop:
        altera = 1                                                               # Identificador para saber se um novo estado já está na tabela
        for regra in tabela:                                                    
            if x in regra:                                                       # Se o novoEstado estiver na tabela, não será alterado nada e ele será removido da lista
                altera = 0
                nstates.remove(x)
        if altera:                                                               # Se o estado não existe na tabela, será criado
            tabela[x] = {}
            estados.append(x)
            for y in simbolos:
                tabela[x][y] = []
            tabela[x]['*'] = []

    for state in nstates:                                                        # Para os estados ainda não criados
        estadosjuntar = sorted(state.split(':'))
        for x in estadosjuntar:
            if x == 'X':                                                         # X ainda não nos é útil
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
            if len(tabela[regra][producao]) > 1:                                     # Caso tenho indeterminismo
                novo = []                                                            # Estados individuais, que geram o indet
                for estado in tabela[regra][producao]:
                    if ':' in estado:                                                # Se tiver ':' será dividido e adicionado um à um
                        for aux in estado.split(':'):
                            if aux not in novo:
                                novo.append(aux)
                    else:                                                            # Se for na primeira vez, não tem ':', então o estado é adicionado à lista estados
                        if not estado in novo:
                            novo.append(estado)

                if novo:                                                             # se novo não for vazio
                    novo = sorted(novo)
                    novo = ':'.join(novo)                                            # Ex: ['A1', 'B1'] -> A1:B1

                if not novosestados.__contains__(novo) and novo:                     # (if '') retorna falso
                    novosestados.append(novo)
                tabela[regra][producao] = novo.split()
    if novosestados:
        criaNovos(novosestados)
    

def criarAF():
    for x in gramatica:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['*'] = []       # coluna do epsilon verificar

    for regra in gramatica:
        for producao in gramatica[regra]:
            if len(producao) == 1 and producao.islower():                                                             # somente 1 terminal
                tabela[regra][producao].append('X')
            elif producao[0] == '<':                                                                                   # somente 1 regra (epsilon transição)
                tabela[regra]['*'].append(producao.split('<')[1][:-1])
            elif producao != '*':                                                                                      # caso geral
                tabela[regra][producao[0]].append(producao.split('<')[1][:-1])

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
            regra = cop.upper() + '1'
        else:
            regra = cop.upper() + str(x)

        # é possível um token onde |token| = 1? se sim, falta tratar
        if x == 0 and x != len(token)-1:                                                                                # Se for o primeiro e não último
            trataEstS(token[x], 'T', '<' + regra + '>')
        elif x == len(token)-1:                                                                                         # Se for o ultimo, é terminal e não leva à outro estado
            gramatica[regra] = str(token[x] + '<' + cop.upper() + '>').split()
            gramatica[cop.upper()] = []
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
    print("\n\nAFND: ", tabela)
    eliminarEpTransicao()
    determizina()
    print("\n\nAFD: ", tabela)
    buscarAlcan('S')
    print('\n\nAlcan: ', alcan)
    eliminarInal()
    print("\n\nVIVOS: ", tabela)
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