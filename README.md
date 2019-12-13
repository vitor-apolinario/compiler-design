# Projeto e implementação das etapas de compilação para uma linguagem de programação hipotética.

Vitor Antonio Apolinário e Willian Bordignon Genero

## Análise Léxica

* Implementar analisador léxico;
* Gerar informações na tabela de símbolos para uso posterior;
* Contém arquivo de entrada com cadeia de símbolos ou gramáticas regulares;
* Como saída, uma fita contendo estados válido ou de erro dos tokens e a tabela de símbolos;
* Em caso de erros léxicos, deve ser exibida uma mensagem informativa.

## Análise Sintática

* Construir as regras sintáticas da linguagem;
* Eliminar inúteis e inalcançáveis;
* Construção do conjunto de itens válidos, transições e follow;
* Construção da tabela de parsing SLR ou LALR;
* Implementação do algoritmo de mapeamento da tabela para reconhecimento sintático;
* Gerenciamento da tabela de símbolos;
* Tratamento de erros, adição de atributos aos símbolos e valores.

## Análise Semântica

* Definir característica semântica;
* Implementar essa característica.

## Geração código intermediário

* Cada redução de uma produção é seguida de uma chamada a uma ação que gera o correspondente trecho de código intermediário com os respectivos rótulos dos identificadores e constantes;

* Aplicar a geração de código intermediário para uma das regras sintáticas.

## Otimização

* Aplicar uma estratégia de otimização de código sobre o código intermediário gerado.

### Situação atual

* [X] Análise léxica.
* [X] Análise sintática.
* [X] Análise semântica.
* [X] Geração de código intermediário.
* [ ] Otimização de código.
