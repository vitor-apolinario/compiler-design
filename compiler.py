import xml.etree.ElementTree as ET
import csv

arquivo = list(open('config/tokens.txt'))
codigo  = list(open('config/codigo.txt'))
tree = ET.parse('config/tabParsing.xml')
root = tree.getroot()

simbolos, estados, alcan, finais, vivos, tS, fitaSaida, fita, escopo, block = [], [], [], [], [], [], [], [], [], []
gramatica, tabela, epTransicao, idxSymbolRedux = {}, {}, {}, {}
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


def analisador_lexico():
    separadores = [' ', '\n', '\t', '+', '-', '{', '}', '~', '.']
    espacadores = [' ', '\n', '\t']
    operadores  = ['+', '-', '~', '.']
    id = 0
    for idx, linha in enumerate(codigo):
        E = 'S'
        string = ''
        for char in linha:
            if char in operadores and string:                                 # Se lemos um operador e temos uma string não vazia
                if string[-1] not in operadores:                              # Se o ultimo caractere reconhecido não é um operador:
                    if E in finais:                                           # O operador lido atualmente é um separador
                        tS.append({'Line': idx, 'State': E, 'Label': string}) # Logo devemos reconhecer a string anterior e continuar a leitura
                        fitaSaida.append(E)
                    else:
                        tS.append({'Line': idx, 'State': 'Error', 'Label': string})
                        fitaSaida.append('Error')
                    E = tabela['S'][char][0]                                    # É iniciado o mapeamento da próxima estrutura de operadores
                    string = char
                    id += 1
                else:                                                         # Caso o último caractere reconhecido seja um operador
                    string += char                                            # continuamos o mapeamento normalmente
                    if char not in simbolos:
                        E = '€'
                    else:
                        E = tabela[E][char][0]
            elif char in separadores and string:
                if E in finais:
                    tS.append({'Line': idx, 'State': E, 'Label': string})
                    fitaSaida.append(E)
                else:
                    tS.append({'Line': idx, 'State': 'Error', 'Label': string})
                    fitaSaida.append('Error')
                E = 'S'
                string = ''
                id += 1
            else:
                if char in espacadores:
                    continue
                if char not in separadores and char not in operadores and string:
                    if string[-1] in operadores:
                        if E in finais:                                             # O operador lido atualmente é um separador
                            tS.append({'Line': idx, 'State': E, 'Label': string})
                            fitaSaida.append(E)
                        else:
                            tS.append({'Line': idx, 'State': 'Error', 'Label': string})
                            fitaSaida.append('Error')
                        E = 'S'
                        string = ''
                        id += 1
                string += char
                if char not in simbolos:
                    E = '€'
                else:
                    E = tabela[E][char][0]
    tS.append({'Line': idx, 'State': 'EOF', 'Label': ''})
    fitaSaida.append('EOF')
    erro = False
    for linha in tS:
        if linha['State'] == 'Error':
            erro = True
            print('Erro léxico: linha {}, sentença "{}" não reconhecida!'.format(linha['Line']+1, linha['Label']))
    if erro:
        exit()


# Função que inicialmente troca na fitaSaida os estados S1 e S2 por VAR e NUM, respectivamente
# Por fim, altera o estados que eram nomes pelo indice para ser reconhecido no analisador sintático
def mapeamento(symbols):
    symbols_indexes = {}    # faz um "mapeamento reverso" { 'SymbolName': 'SymbolIndex' }
    for index, symbol in enumerate(symbols):
        symbols_indexes[symbol['Name']] = str(index)
        idxSymbolRedux[str(index)] = symbol['Name']
    for fta in fitaSaida:
        if fta == 'S1' or fta == 'ENQUANTO1:S1' or fta == 'IGUAL1:S1':
            fta = 'VAR'
        elif fta == 'S2':
            fta = 'NUM'
        elif fta == '$':
            fta = 'EOF'
        fita.append(symbols_indexes[fta])

    for line in tS:
        if line['State'] == 'S1' or line['State'] == 'ENQUANTO1:S1' or line['State'] == 'IGUAL1:S1':
            line['State'] = 'VAR'
        elif line['State'] == 'S2':
            line['State'] = 'NUM'
        elif line['State'] == '$':
            line['State'] = 'EOF'


def analisador_sintatico():
    redux_symbol, symbols, productions, lalr_table, pilha  = [], [], [], [], ['0']

    def charge():
        xml_symbols = root.iter('Symbol')
        for symbol in xml_symbols:
            symbols.append({
                'Index': symbol.attrib['Index'],
                'Name': symbol.attrib['Name'],
                'Type': symbol.attrib['Type']
            })

        xml_productions = root.iter('Production')
        for production in xml_productions:
            productions.append({
                'NonTerminalIndex': production.attrib['NonTerminalIndex'],
                'SymbolCount': int(production.attrib['SymbolCount']),
            })

        lalr_states = root.iter('LALRState')
        for state in lalr_states:
            lalr_table.append({})
            for action in state:
                lalr_table[int(state.attrib['Index'])][str(action.attrib['SymbolIndex'])] = {
                    'Action': action.attrib['Action'],
                    'Value': action.attrib['Value']
                }

    def parser():
        idx = 0
        while True:
            ultimo_fita = fita[0]
            try:
                action = lalr_table[int(pilha[0])][ultimo_fita]
            except:
                print('Erro sintático: linha {}, sentença "{}" não reconhecida!'.format(tS[idx]['Line']+1, tS[idx]['Label']))
                exit()
                break

            if action['Action'] == '1':
                pilha.insert(0, fita.pop(0))
                pilha.insert(0, action['Value'])
                idx += 1
            elif action['Action'] == '2':
                size = productions[int(action['Value'])]['SymbolCount'] * 2
                while size:
                    pilha.pop(0)
                    size -= 1
                redux_symbol.append(productions[int(action['Value'])]['NonTerminalIndex'])
                pilha.insert(0, productions[int(action['Value'])]['NonTerminalIndex'])
                pilha.insert(0, lalr_table[int(pilha[1])][pilha[0]]['Value'])
            elif action['Action'] == '3':
                print('salto')
            elif action['Action'] == '4':
                break

    def catch_statements():
        pilha_aux = [1]
        id = 1
        for symbol in redux_symbol:
            if idxSymbolRedux[symbol] == 'CONDS':
                id += 1
                pilha_aux.insert(0, id)
                block.append(pilha_aux[1])
            elif idxSymbolRedux[symbol] == 'REP' or idxSymbolRedux[symbol] == 'COND':
                pilha_aux.pop(0)
            elif idxSymbolRedux[symbol] == 'RVAR':
                escopo.append(pilha_aux[0])

    def complete_ts():
        for token in tS:
            if token['State'] == 'VAR':
                token['Scope'] = escopo.pop(0)

    charge()
    mapeamento(symbols)
    parser()
    catch_statements()
    complete_ts()


def analisador_semantico():
    var_scope = {}
    error = False

    def check_scope(scope_use, scope_dec):
        if scope_use == scope_dec:
            return True
        elif scope_use == 1:
            return False
        else:
            return check_scope(block[scope_use-2], scope_dec)


    for index, token in enumerate(tS):
        if token['State'] == 'VAR' and tS[index-1]['State'] == 'BIN':
            if token['Label'] in var_scope:
                error = True
                print('Erro semântico: linha {}, variável "{}" já declarada!'.format(token['Line']+1, token['Label']))
            else:
                var_scope[token['Label']] = token['Scope']

        if token['State'] == 'VAR' and tS[index-1]['State'] != 'BIN':
            if token['Label'] in var_scope:
                if not check_scope(token['Scope'], var_scope[token['Label']]):
                    error = True
                    print('Erro semântico: linha {}, variável "{}" escopo inválido!'.format(token['Line']+1, token['Label']))
            else:
                error = True
                print('Erro semântico: linha {}, variável "{}" não declarada!'.format(token['Line']+1, token['Label']))
    if error:
        exit()

def codigo_intermediario():
    ts_code = []
    int_code = []

    def encontra_operacoes():
        flag = False
        operacao = []
        for idx, token in enumerate(tS):
            if token['State'] == 'VAR' and tS[idx+1]['State'] == '~' and tS[idx+1]['State'] != '.':
                operacao.append(token['Label'])
                flag = True
            elif token['State'] == '.' and tS[idx-2]['State'] != 'BIN':
                ts_code.append(operacao)
                operacao = []
                flag = False
            elif flag:
                operacao.append(token['Label'])


    def gera_temp(operacao, temp):
        flag = False
        cod, copy = [], []
        copy.extend(operacao)

        for idx in range(len(operacao)-1):
            if operacao[idx+1] == '\\' or operacao[idx+1] == '/':
                for i in range(-1, 2):
                    cod.insert(0, copy[idx])
                    copy.pop(idx)
                copy.insert(idx, 'T' + str(temp))
                flag = True
                break

        if not flag:
            for idx in range(len(operacao)-1):
                if operacao[idx+1] == '+' or operacao[idx+1] == '-':
                    for i in range(-1, 2):
                        cod.insert(0, copy[idx])
                        copy.pop(idx)
                    copy.insert(idx, 'T' + str(temp))
                    break

        cod.insert(0, '~')
        cod.insert(0, 'T'+str(temp))
        return copy, cod

    def gera_codigo():
        temp = 1
        for operacao in ts_code:
            while True:

                if len(operacao) == 3:
                    cod = []
                    for x in range(len(operacao)):
                        cod.append(operacao[x])

                    int_code.append(cod)
                    break

                operacao, cod = gera_temp(operacao, temp)
                temp += 1
                int_code.append(cod)

    def exporta_codigo():
        file = open('config/code_inter.txt', 'w+')
        for x in int_code:
            file.write(str(x).replace('[','').replace(']','').replace("'",'').replace(',','') +'\n')

    encontra_operacoes()
    gera_codigo()
    exporta_codigo()


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
    analisador_lexico()
    analisador_sintatico()
    analisador_semantico()
    codigo_intermediario()
    print('Código compilado com sucesso!')

print('\n' * 60)
main()
