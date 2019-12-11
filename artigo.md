# Projeto e implementação das etapas de compilação para uma linguagem de programação hipotética

Vitor Antonio Apolinário  
Willian Bordignon Genero

## Resumo

O presente trabalho busca projetar e implementar um algoritmo, capaz de realizar todas as etapas de compilação: análise léxica, sintática, semântica, código intermediário e otimização. Para isso, serão usados alguns arquivos fontes que contém tokens e gramáticas regulares, a linguagem hipotética, um código e uma tabela de parsing.

## Referencial Teórico

Linguagem formal: ​também conhecida como linguagem de programação,procuram eliminar toda ambigüidade possível,garantindo assim que um comando e  palavras reservadas tenham sempre o mesmo significado independentemente de onde apareçam no programa. Evita a ambiguidade existente em linguagens humanas e aabstração presente na linguagem de máquina.  
Forma normal de Backus: ​define que tudo entre ‘<’ e ‘>’ é uma variável que pode ser trocado por um outro símbolo posteriormente.  
Estadofinal:​ um estado é final se ele pode ser trocado por um símbolo terminal ou uma Epsilon produção.  
Transições: ​transição é quando estando em um estado e a partir de uma produção atingir outro estado.
Autômato determinístico: separa cada símbolo de entrada existe exatamente uma transição de saída de cada estado.  

## Introdução

Um compilador é um programa que traduz um código de alto nível descrito por um programador para um código equivalente em linguagem de máquina. O compilador consiste em analisar cada símbolo do código fonte se o mesmo é permitido pela linguagem, posteriormente verifica se as estruturas são válidas e se existem incôerencias semânticas. Se nenhum erro for encontrado o código será transformado em operações baseadas em três endereços e então otimazadas.
Esse trabalho utiliza um autômato finito como base que anteriormente foi implementado no componente curricular Linguagens Formais e Autômatos, outra ferramenta utilizada é o programa GoldParser que dada uma gramática livre de contexto que representa a linguagem hipotética irá fornecer um arquivo .xml contendo a tabela LALR responsável pela análise sintática.
A seguir será apresentada a metodologia seguida para o desenvolvimento assim como explicação para cada etapa construída, por fim a conclusão e o referencial bibliográfico.

## Implentação

### Metodologia

A linguagem de programação utilizada para desenvolver a aplicação foi Python, devido a disponibilidade de diferentes estruturas de dados. O versionamento de código é feito usando git, e o repositório pode ser encontrado em https://github.com/vitor-apolinario/compiler-design. A construção do compilador foi em sequência com os conteúdos apresentados no componente curricular:

1. Ajustes no autômato finito determinístico desenvolvido anteriormente assim como nos tokens e gramáticas regulares permitidos.

2. Criado um arquivo que pode ser manipulado e representa o código escrito pelo programador.

3. Implementado o analisador léxico.

4. Definida a gramática livre de contexto que define as estruturas permitidas na linguagem.

5. Instalado o GoldParser e usando a GLC anterior gerado a tabela de parsing.

6. Construído o mapeamento que resolve as divergências entre o autômato finito e o GoldParser.

7. Implementado o analisador sintático com base na tabela de parsing.

8. Implememtado o analisador semântico sobre a característica de escopo nas variáveis.

### Arquivos de entrada

- Um arquivo nomeado de "tokens.txt" pode ser preenchido com tokens e gramáticas regulares seguindo a forma normal de Backus, esse arquivo define quais símbolos podem ser construídos na linguagem.

- Um arquivo chamado de "codigo.txt" que armazena um programa qualquer escrito pelo programador.

- "tabParsing.xml" comporta as informações geradas pelo programa auxiliar GoldParser.

- "linguagem.bnf" é responsável por definir quais estruturas são permitidas na linguagem hipotética.

### Autômato Finito Determinístico

O autômato finito determinístico implementado no componente curricular Linguagens Formais e Autômatos é um modelo de máquina que reconhece um conjunto finito de estados, com um conjunto de transições que ocorrem a partir de símbolos de um alfabeto e tem a função de aceitar ou rejeitar uma cadeia de símbolos. Usamos como base o arquivo "tokens.txt" para sua construção.  
É livre de épsilon transições, estados inalcançáveis e estados mortos e sua saída é um dicionário de dicionários (estrutura de dados Python). Onde cada índice é um estado e seus valores são todos os símbolos do alfabeto que tem como valor o estado seguinte.  

### Código escrito pelo programador

No arquivo "codigo.txt" pode ser descrito qualquer símbolo e estrutura que o programador queira, esse código será realizado as análises e otimizações, se nenhum erro for encontrado o código será aceito. Caso seja encontrado um erro será em alguma etapa de análise que explicaremos a seguir.

### Análise léxica

Seu funcionamento é percorrer cada caracter do arquivo "codigo.txt" e verificar se eles ou sequência deles é permitida pela linguagem. Ao ler cada caracter será associado o que deve ser feito com ele seguindo as possibilidades abaixo:

- Se o caracter for um operador separador: é adicionado na tabela de símbolos e fita de saída a cadeia de símbolos antecessora e reiniciado a analise já com o caracter lido.

- Se o caracter for operador mas não separador: será continuada a leitura dos caracteres.

- Se o caracter for um separador e suceder uma cadeia de símbolos: a cadeia em questão é adicionada a tabela de símbolos e fita de saída e a análise é reiniciada sem nenhum caracter.

- Caso encontre o fim de um operador: o mesmo é adicionado à fita de saída e tabela de símbolos e reinicia o processo.

- Caso o caracter não seja nenhum dos descritos acima é lido o próximo caracter.

Quando chegar no fim do arquivo é adicionado o estado final na fita de saída e tabela de símbolos.  
Por fim, toda a tabela de símbolos é percorrida em busca de tokens com estado de erro, se encontrado uma mensagem de erro é exibida na tela contendo a linha e o próprio token.  
Duas estruturas são retornadas da análise léxica:

- Tabela de símbolos contendo linha, estado e rótulo para cada token.

- Fita de saída, vetor que armazena somente os estados dos tokens que será usada na analíse sintática.

### Análise sintática

Recebe como entrada a fita de saída obtida na etapa anterior. Tem objetivo principal de reconhecer se a estrutura sintática do código escrito pelo programador obedece as regras de produção especificadas pela gramática livre de contexto. Através da identificação das reduções consegue armazenar informações em uma estrutura auxiliar e posteriormente define o escopo de uso dos tokens, informações essas necessárias para validações da análise semântica.

#### Carga de informações apartir do xml gerado pelo GoldParser:
  - Informações dos símbolos (estrutura utilizada pelo analisador):
  
   ```   
   symbols = [
     {
      'Index': '12',
      'Name': 'ENQUANTO',
      'Type': '1'
     }, 
     ...
   ]
   ```

  - Informações das produções (estrutura utilizada pelo analisador):
  
   ```   
   productions = [
     {
      'NonTerminalIndex': '29
      'SymbolCount': 3
     }, 
     ...
   ]
   ```
   
  - A tabela LALR (estrutura utilizada pelo analisador):
  
  obs.: As ações podem ser 1, 2, 3 e 4, respectivamente empilhamento, redução, salto e aceite.
   ```   
   lalr_table = [
     {
      // índice do símbolo produzido
      '11': {
        // ação à ser realizada
        'Action': '1'
        'Value': '1'
      },
      ...      
     }, 
     ...
   ]
   ```
   
Com as informações estruturadas desta forma, podemos utilizar dados fornecidos pelo GoldParser de uma forma mais simples. Considerando o exemplo anterior, caso estivermos no estado 0 e encontrarmos o símbolo de índice '11' no topo da pilha, realizaremos a ação contida em lalr_table\[0]\['11'], que  diz que temos que realizar um empilhamento ('Action': '1'), removendo o símbolo '11' do início da fita colocando-o no topo da pilha, seguido do símbolo de índice '1' ('Value': '1').

#### Mapeamento
Nesta etapa é realizado o mapeamento de forma que os estados reconhecidos pelo nosso autômato tenham os identificador iguais aos gerados pelo GoldParser. Esta etapa ocorre através da fita de saída fornecida pelo analisador léxico, que é percorrida em busca de identificadores específicos. Se forem encontrados algum dos estados 'S1', 'ENQUANTO1:S1', 'IGUAL1:S1' os mesmos são são substituídos pelo estado 'VAR', porque os mesmos reconhecem variáveis, se for encontrado o estado 'S2', o mesmo é substituído por 'NUM', pois é o estado que reconhece os números binários do código. E finalmente o símbolo '$' é substituído pelo símbolo 'EOF'. Estes nomes fornecidos ('VAR', 'NUM', 'EOF') são meramente utilizados para o melhor entendimento, pois eles são mapeados pra índices e é assim que o GoldParser trabalha, um exemplo:

```
  <m_Symbol Count="30">
    [...]
    <Symbol Index="4" Name="." Type="1"/>
    <Symbol Index="7" Name="{" Type="1"/>
    <Symbol Index="8" Name="}" Type="1"/>
    <Symbol Index="16" Name="NUM" Type="1"/>
    <Symbol Index="17" Name="SE" Type="1"/>
    <Symbol Index="18" Name="VAR" Type="1"/>
    <Symbol Index="19" Name="A" Type="0"/>
    <Symbol Index="20" Name="ATR" Type="0"/>
    <Symbol Index="21" Name="COND" Type="0"/>    
    [...]
   </m_Symbol>

```
Os símbolos "Type":"1" são terminais e os "Type":"0" não terminais.

#### Reconhecimento

Aqui é onde de fato acontece o reconhecimento sintático, temos um vetor state=\['0'], que é a pilha e inicialmente contém só o estado zero, também temos a fita contendo os estados mapeados anteriormente, assim como informações da tabela de parsing e do tamanho das produções, é tudo que precisamos para realizar o reconhecimento.
  - A ação à ser realizada está contida em: 
  
  ```
  // A posição 0 da fita é o token encontrado e a posição 0 da pilha representa o estado atual.
  ultimo_fita = fita[0]
  action = lalr_table[int(state[0])][ultimo_fita]
  ```  
  
  Se lalr_table[int(state[0])][ultimo_fita] não existir, temos um erro sintático caso contrario:
  
   - Se a ação for um empilhamento: retiramos o símbolo do início da fita e inserimos no topo da pilha, e depois inserimos o valor especificado na action no topo da pilha;
  - Se a ação for uma redução: Supondo que a ação tenha o formato: {'Action': '2', 'Value': '25'}. Utilizamos a estrutura "productions" e buscamos a produção de índice 25 para pegar o seu tamanho, e removemos o dobro dessa quantidade de símbolos da pilha. Aqui acontece uma etapa muito importante que é adicionar a produção reduzida em uma lista "redux_symbol", a qual discutiremos depois. Também adicionaremos no topo da pilha a produção à qual reduzimos, assim como acontecerá um salto, olhando para o penúltimo símbolo da pilha como estado atual e topo da pilha como símbolo encontrado;
  - Se a ação for 4, o código é aceito.
  
#### Montagem da árvore de escopos

Aqui será utilizada a estrutura de reduções "redux_symbols" criada na etapa anterior. Ela contém todas as reduções realizadas em sequência no código. Como na análise semântica pretendemos tratar o escopo de uso das variáveis, a maneira de identificar um determinado escopo é obtida através de um olhar sobre as reduções realizadas. Um novo escopo sempre é iniciado de alguma das seguintes formas:

```
enquanto <CONDS> {
  /* código */
}
```

ou

```
se <CONDS> {
    /* código */
}
```

Onde "CONDS" representa uma condição que acontece exclusivamente nestes casos (antes de início de blocos), assim, é possível identificar que após cada redução de uma estrutura qualquer para <CONDS> temos o início de um novo bloco. Ainda olhando para as produções, é possível identificar que os blocos acima foram terminado quando olhamos para "redux_symbols" e encontramos um símbolo "REP" ou "COND", devido as produções da GLC que reconhecem estas estruturas:

```
<COND> ::= SE <CONDS> '{' <S> '}'
<REP> ::= ENQUANTO <CONDS> '{' <S> '}'
```

Sabendo identificar onde um escopo inicia e termina, decidimos montar uma árvore, em forma de vetor, onde a iésima posição do vetor contém o pai do elemento i, um exemplo, dada a estrutura de escopos abaixo:

```
ESCOPO1 (global)
  ESCOPO2
  ESCOPO3
    ESCOPO4
```
O vetor gerado será o seguinte \[0, 1, 1, 3], e significa que o escopo 1 (global) é a raíz, o escopo 2, é filho do escopo 1, o escopo 3 é filho do escopo 1, e o escopo 4 é filho do escopo 3. Esta "árvore de escopos" será utilizada posteriormente na análise semântica.
Assim como na identificação do início e final de escopos, foi criada uma regra na linguagem que sempre realiza uma redução quando encontra uma uma váriável, assim quando estamos montando a árvore de escopos e encontramos uma redução do tipo RVAR ::= VAR, sabemos que há o uso ou declaração de uma variável, assim devemos atribuír o escopo atual para o token encontrado. Desta forma qualquer token que seja uma variável vai ter um atributo denominado 'Scope' que informa o escopo no qual o mesmo está sendo utilizado.


### Análise semântica

Como características semânticas da nossa linguagem, resolvemos tratar o escopo de declaração e uso de variáveis não declaradas. 
- Uma variável declarada num escopo X, só é acessível em X ou em escopos filhos de X;
- Somente variáveis declaradas podem ser utilizadas. 

Resultado da análise sintática, temos duas estruturas, a "árvore de escopos", e o escopo de declaração das variáveis. Assim precisamos percorrer a tabela de símbolos, e pra cada utilização de uma variável (somente uso), verificamos inicialmente se aquela variável foi consta na estrutura de declaração das variáveis:
- Se não consta: Erro semântico de variável não declarada;
- Se consta: Devemos verificar se o escopo de uso é válido?
    - A verificação do escopo ocorre utilizando a árvore e um algoritmo recursivo, suponha o seguinte exemplo:
    ```
    ESCOPO1 (global)
      declaração var a
      ESCOPO2
      ESCOPO3
        ESCOPO4
        uso var a
    ```
    A árvore criada seria \[0, 1, 1, 3], a variável "a" foi declarada no escopo 1, e usada no escopo 4, este uso é permitido? chama-se a função recursiva verifica_escopo(4, 1).
```
verifica_escopo(escopo_uso, escopo_declarado)
    if escopo_uso == 0:
        uso válido
    if escopo_uso == escopo_declarado:
        uso inválido
    else:
        verifica_escopo(arvore[escopo_uso] - 1, escopo_declarado)
```
    
    
