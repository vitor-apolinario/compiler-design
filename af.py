import xml.etree.ElementTree as ET
import csv

arquivo = list(open('config/tokens.txt'))
codigo  = list(open('config/codigo.txt'))
tree = ET.parse('config/tabParsing.xml')
root = tree.getroot()

simbolos = []
estados = []
alcan = []
gramatica = {}
tabela = {}
finais = []
vivos = []
epTransicao = {}
repeticao = 0


def eliminar_mortos():
    mortos = []
    for x in tabela:
        if x not in vivos and x != '€':
            mortos.append(x)
    
    for x in mortos:
        del tabela[x]


def buscar_vivos():    
    mudou = False

    for regra in tabela:
        for simbolo in tabela[regra]:
            if tabela[regra][simbolo][0] in vivos and regra not in vivos:
                vivos.append(regra)
                mudou = True

    if mudou:
        buscar_vivos()


def eliminar_incal():
    loop = {}
    loop.update(tabela)
    for regra in loop:
        if regra not in alcan:
            del tabela[regra]
                

def buscar_alcan(estado):
    if estado not in alcan:         
        alcan.append(estado)
        for simbolo in tabela[estado]:
            if tabela[estado][simbolo] \
                    and tabela[estado][simbolo][0] not in alcan:
                buscar_alcan(tabela[estado][simbolo][0])


def encontrar_eps_set(e_transicoes):
    for x in e_transicoes:
        for y in tabela[x]['*']:
            if y not in e_transicoes:
                e_transicoes.append(y)
    return e_transicoes


def eliminar_et():
    for regra in tabela:
        et_set = encontrar_eps_set(tabela[regra]['*'])
        for estado in et_set:
            if estado in finais:
                finais.append(regra)
            for simbolo in tabela[estado]:
                for transicao in tabela[estado][simbolo]:
                    if transicao not in tabela[regra][simbolo]:
                        tabela[regra][simbolo].append(transicao)
        tabela[regra]['*'] = []


def criar_novos(nstates):
    for x in nstates:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['*'] = []

    for state in nstates:
        estadosjuntar = sorted(state.split(':'))
        for x in estadosjuntar:
            if x in finais and state not in finais:
                finais.append(state)
            for simbolo in simbolos:
                for transition in tabela[x][simbolo]:
                    if not tabela[state][simbolo].__contains__(transition):
                        tabela[state][simbolo].append(transition)
    determizinar()


def determizinar():
    novosestados = []
    for regra in tabela:
        for producao in tabela[regra]:
            if len(tabela[regra][producao]) > 1:
                novo = []
                for estado in tabela[regra][producao]:
                    if ':' in estado:
                        for aux in estado.split(':'):
                            if aux not in novo:
                                novo.append(aux)
                    else:
                        if estado not in novo:
                            novo.append(estado)

                if novo:
                    novo = sorted(novo)
                    novo = ':'.join(novo)

                if novo and novo not in novosestados and novo not in list(tabela.keys()):
                    novosestados.append(novo)
                tabela[regra][producao] = novo.split()
    if novosestados:
        criar_novos(novosestados)
    

def criar_af():
    for x in gramatica:
        tabela[x] = {}
        estados.append(x)
        for y in simbolos:
            tabela[x][y] = []
        tabela[x]['*'] = []

    for regra in gramatica:
        for producao in gramatica[regra]:
            if len(producao) == 1 and producao.islower() and regra not in finais:
                finais.append(regra)
            elif producao == '*' and regra not in finais:
                finais.append(regra)
            elif producao[0] == '<':
                tabela[regra]['*'].append(producao.split('<')[1][:-1])
            elif producao != '*':
                tabela[regra][producao[0]].append(producao.split('<')[1][:-1])


def criar_sn(s):
    global repeticao
    if 'S' + str(repeticao) in gramatica:
        return
    gramatica['S' + str(repeticao)] = s.replace('\n', '').split(' ::= ')[1].replace('>', str(repeticao) + '>').split(' | ')


def tratar_gramatica(gram, s):
    global repeticao
    gram = gram.replace('\n', '')
    for x in gram.split(' ::= ')[1].replace('<', '').replace('>', '').split(' | '):
        if x[0] not in simbolos and not x[0].isupper():
            simbolos.append(x[0])
    regra = gram.split(' ::= ')[0].replace('>', str(repeticao)).replace('<', '')

    if regra[0] == 'S':
        repeticao += 1
        gramatica['S'] += gram.split(' ::= ')[1].replace('>', str(repeticao) + '>').split(' | ')
    else:
        gramatica[regra] = gram.split(' ::= ')[1].replace('>', str(repeticao)+'>').split(' | ')

    if '<S>' in gram.split(' ::= ')[1]:
        criar_sn(s)


def tratar_token(token):
    token = token.replace('\n', '')
    cp_token = token
    token = list(token)
    for x in range(len(token)):
        if token[x] not in simbolos and not token[x].isupper():
            simbolos.append(token[x])

        if len(token) == 1:
            iniregra = '<' + cp_token.upper() + '>'
            gramatica['S'] += str(token[x] + iniregra).split()            
            gramatica[cp_token.upper()] = []
            finais.append(cp_token.upper())
        elif x == 0 and x != len(token)-1:
            iniregra = '<' + cp_token.upper() + '1>'
            gramatica['S'] += str(token[x] + iniregra).split()
        elif x == len(token)-1:
            finregra = '<' + cp_token.upper() + '>'
            gramatica[cp_token.upper() + str(x)] = str(token[x] + finregra).split()
            gramatica[cp_token.upper()] = []
            finais.append(cp_token.upper())
        else:
            proxregra = '<' + cp_token.upper() + str(x+1) + '>'
            gramatica[cp_token.upper() + str(x)] = str(token[x] + proxregra).split()


def criar_csv():
    with open('afnd.csv', 'w', newline='') as f:
        w = csv.writer(f)
        copydict = {}
        copydict.update(tabela)
        w.writerow(list(copydict['S'].keys()) + ['regra'])
        for x in copydict:
            if x in finais:
                copydict[x]['nomeregra'] = x + '*'
            else:
                copydict[x]['nomeregra'] = x
            w.writerow(copydict[x].values())


def estado_erro():
    tabela['€'] = {}
    for y in simbolos:
        tabela['€'][y] = []
    tabela['€']['*'] = []
    for regra in tabela:
        for simbolo in tabela[regra]:
            if not tabela[regra][simbolo]:
                tabela[regra][simbolo] = ['€']

def analisadorLexico():
    tS = {}
    fitaSaida = []
    separadores = [' ', '\n', '\t', '+', '-', '#', '~', ';']
    operadores  = ['+', '-', '#', '~', ';']
    for idx, linha in enumerate(codigo):
        E = 'S'
        string = ''
        tS[idx] = [] 
        for char in linha:
            if char in separadores and string:
                if E in finais:
                    tS[idx].append(E + ':' + string)
                    fitaSaida.append(E)
                else:
                    tS[idx].append('€' + ':' + string)
                    fitaSaida.append('€')
                E = 'S'
                string = ''
            elif char in operadores and string:                             # Se lemos um operador e temos uma string não vazia
                if string[-1] not in operadores:                            # Se o ultimo caractere reconhecido não é um operador:
                    if E in finais:                                             # O operador lido atualmente é um separador
                        tS[idx].append(E + ':' + string)                        # Logo devemos reconhecer a string anterior e continuar a leitura
                        fitaSaida.append(E)
                    else:
                        tS[idx].append('€' + ':' + string)
                        fitaSaida.append('€')
                    E = tabela['S'][char][0]                               # É iniciado o mapeamento da próxima estrutura de operadores
                    string = char
                else:                                                      # Caso o último caractere reconhecido seja um operador
                    string += char                                           # continuamos o mapeamento normalmente
                    if char not in simbolos:
                        E = '€'
                    else:
                        E = tabela[E][char][0]
            else:
                if char in separadores:
                    continue
                if char not in separadores and char not in operadores and string:
                    if string[-1] in operadores:
                        if E in finais:                                             # O operador lido atualmente é um separador
                            tS[idx].append(E + ':' + string)                        # Logo devemos reconhecer a string anterior e continuar a leitura
                            fitaSaida.append(E)
                        else:
                            tS[idx].append('€' + ':' + string)
                            fitaSaida.append('€')
                        E = 'S'
                        string = ''
                string += char
                if char not in simbolos:
                    E = '€'
                else:
                    E = tabela[E][char][0]
    fitaSaida.append('$')
    for linha in tS:
        for token in tS[linha]:
            if token and token[0] == '€':
                print('Erro léxico: linha {}, sentença "{}" não reconhecida!'.format(linha,token.split(':')[-1]))

def analisadorSintatico():
    alfabeto = {}
    LALRTable = {}

    simbolosTabela = root.iter('m_Symbol')
    for simbolo in simbolosTabela:
        for x in simbolo:
            alfabeto[x.attrib['Index']] = x.attrib['Name']

    LALR = root.iter('LALRTable')
    for table in LALR:
        for state in table:
            LALRTable[state.attrib['Index']] = {}
            for action in state:
                LALRTable[state.attrib['Index']][action.attrib['SymbolIndex']] = action.attrib['Action'], action.attrib['Value']

    print('\nAlfabeto: ', alfabeto)
    print('\nLALR: ', LALRTable)

def main():
    gramatica['S'] = []
    estadoinicial = ''
    for x in arquivo:
        if '<S> ::=' in x:
            estadoinicial = x
        if '::=' in x:
            tratar_gramatica(x, estadoinicial)
        else:
            tratar_token(x)
    criar_af()
    eliminar_et()
    determizinar()
    buscar_alcan('S')
    eliminar_incal()
    estado_erro()
    vivos.extend(finais)
    buscar_vivos()
    eliminar_mortos()
    criar_csv()
    analisadorLexico()
    analisadorSintatico()


print('\n' * 45)
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

# se
# entao
# senao
# <S> ::= a<A> | e<A> | i<A> | o<A> | u<A> | <A>
# <A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | *

# <S> ::= a<S> | <A>
# <A> ::= b<A> | <B>
# <B> ::= c<B> | *

# if
# <S> ::= a<A> | b<B> | b | c<S> | c | *
# <A> ::= a<S> | a | b<C> | c<A>
# <B> ::= a<A> | c<B> | c<S> | c
# <C> ::= a<S> | a | c<A> | c<C>
# else

# <S> ::= a<A> | a | b | c<C> | b<D>
# <A> ::= a<B> | b<A> | c<B> | *
# <B> ::= a<A> | b<B> | c<A> | a | c
# <C> ::= a<C> | b<D> | c<C> | b
# <D> ::= a<D> | b<C> | c<C> | * | c | a
# <E> ::= a<C> | b<F> | a
# <F> ::= b<E> | c<B> | b
