# Firewall Inteligente com Árvore de Decisão

## Sobre o Projeto

Desenvolvi um firewall inteligente em Python que utiliza Árvore de Decisão com Machine Learning para classificar tráfego de rede. Este projeto foi desenvolvido para a disciplina de Estudos Avançados em Segurança da Informação, sob orientação do professor Fábio Henrique Cabrini.

Diferente de firewalls tradicionais baseados em regras fixas, este sistema aprende padrões a partir de dados históricos. O sistema classifica o tráfego em três categorias de segurança:

- NORMAL -> libera a conexão
- SUSPEITO -> monitora o tráfego
- MALICIOSO -> bloqueia a conexão

## Funcionalidades

A interface possui três funcionalidades principais:

1. Teste manual - usuário informa porta, pacotes e erros para classificação
2. Escaneamento simulado - digita IP ou site para análise
3. Visualização do Dashboard - exibe a árvore de decisão explicando cada regra

## Tecnologias Utilizadas

- Machine Learning: scikit-learn (DecisionTreeClassifier)
- Dados: pandas e numpy
- Visualização: matplotlib e plot_tree
- Codificação de porta: LabelEncoder
- Simulação de rede: socket

## Resultados Alcançados

- Tratamento de erro: entradas inválidas não quebram o sistema
- Interface organizada e de fácil utilização
- Dashboard mostra a lógica de decisão visualmente
- Sistema robusto que trata entradas inválidas sem falhas

## Como Executar

```bash
python FIREWALL.py
