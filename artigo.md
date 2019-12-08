# Projeto e implementação das etapas de compilação para uma linguagem de programação hipotética.

Vitor Antonio Apolinário
Willian Bordignon Genero

## Resumo

O presente trabalho busca projetar e implementar um algoritmo, capaz de realizar todas as etapas de compilação: análise léxica, sintática, semântica, código intermediário e otimização. Para isso, serão usados alguns arquivos fontes que contém tokens e gramáticas regulares, a linguagem hipotética, um código e uma tabela de parsing.

## Introdução

Um compilador é um programa que traduz um código de alto nível descrito por um programador para um código equivalente em linguagem de máquina. O compilador consiste em analisar cada símbolo do código fonte se o mesmo é permitido pela linguagem, posteriormente verifica se as estruturas são válidas e se existem incôerencias semânticas. Se nenhum erro for encontrado o código será transformado em operações baseadas em três endereços e então otimazadas.
Esse trabalho utiliza um autômato finito como base que anteriormente foi implementado no componente curricular Linguagens Formais e Autômatos, outra ferramenta utilizada é o programa GoldParser que dada uma gramática livre de contexto que representa a linguagem hipotética irá fornecer um arquivo .xml contendo a tabela LALR responsável pela análise sintática.
A seguir será apresentada a metodologia seguida para o desenvolvimento assim como explicação para cada etapa construída, por fim a conclusão e o referencial bibliográfico.

## Implentação

### Metodologia

A linguagem de programação utilizada para desenvolver a aplicação foi Python, devido a disponibilidade de diferentes estruturas de dados. O versionamento de código é feito usando git, e o repositório pode ser encontrado em <github.com/vitor-apolinario/compiler-design>. A construção do compilador foi em sequência com os conteúdos apresentados no componente curricular:

1. Ajustes no autômato finito determinístico desenvolvido anteriormente assim como nos tokens e gramáticas regulares permitidos.

2. Criado um arquivo que pode ser manipulado e representa o código escrito pelo programador.

3. Implementado o analisador léxico.

4. Definida a gramática livre de contexto que define as estruturas permitidas na linguagem.

5. Instalado o GoldParser e usando a GLC anterior gerado a tabela de parsing.

6. Construído o mapeamento que resolve as divergências entre o autômato finito e o GoldParser.

7. Implementado o analisador sintático com base na tabela de parsing.

8. Implememtado o analisador semântico sobre a característica de escopo nas variáveis.

### Arquivos de entrada

