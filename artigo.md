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

- Inicialmente carrega algumas informações apartir do xml gerado pelo GoldParser:
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
