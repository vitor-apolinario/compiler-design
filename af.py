arquivo = list(open('tokens.txt'))

simbolos  = []
estados   = []
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
                tabela[regra][transicao[0]].append(transicao.split('<')[1][:-1])
    print('\nTabela: ', tabela)


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
    

def trataGram(gram):                                                            # Função usada para tratar gramáticas
    for x in gram.split(' ::= ')[1].replace('\n', '').split(' | '):             # Adiciona os símbolos de 1 gramática
        if x[0] not in simbolos and x[0].islower():
            simbolos.append(x[0])
    regra = gram.split(' ::= ')[0].replace('>', str(repeticao)+'>')             # Adiciona o nome da regra à gramática
    if '<S> ::=' in gram:
        trataEstS(gram, 'G', 'essa string nao eh usada')
    else:
        gramatica[regra] = gram.replace('\n','').split(' ::= ')[1].split(' | ')         # Adiciona as transições à gramática
#    print('Gramática: ', gramatica)


def trataToken(token):                                                            # Função usada para tratar tokens
    cop = token.replace('\n','')
    token = list(token)
    if '\n' in token:
        token.remove('\n')
    for x in range(len(token)):
        # print("Token: ", token[x])
        if token[x] not in simbolos and token[x].islower():                                 # Se o símbolo ainda não existe, adiciona
            simbolos.append(token[x])
            
        if x == 0:
            regra = '<' + cop.upper() + '1>'
        else:
            regra = '<' + cop.upper() + str(x) + '>'

        # é possível um token onde |token| = 1? se sim, falta tratar
        if x == 0 and x != len(token)-1:                                                    # Se for o primeiro e não último
            trataEstS(token[x], 'T', regra)
        elif x == len(token)-1:                                                             # Se for o ultimo, é terminal e não leva à outro estado
            gramatica[regra] = token[x].split()
            # se os estados finais forem necessários use o bloco abaixo
            # gramatica[regra] = str(token[x] + '<' + cop.upper() + '*>').split()
            # gramatica['<' + cop.upper() + '*>'] = []
        # pelo que me parece o caso abaixo não deve acontecer
        elif regra in gramatica:                                                            # (??) Se a regra já existir será concatenada com simbolo+SIMBOLO+repeticao (??)
            gramatica[regra] += str(token[x] + token[x].upper() + str(repeticao)).split()
        else:                                                                               # se for um token entre o primeiro e o ultimo => token+proximaregra
            gramatica[regra] = str(token[x]+ '<' + cop.upper() + str(x+1) + '>' ).split()


def main():
    for x in arquivo:
        if '::=' in x:          
            trataGram(x)
#           print('Gramática: ', x)
        else:
#           print("Token: ", x)
            trataToken(x)
    criarAFND()
    print('Simbolos')
    print(simbolos)
    print('Estados')
    print(estados)
    print('Gramática')
    print(gramatica)
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
