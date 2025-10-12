# Sistema de Controle de Colheita de Cana-de-Açúcar

## Problema do Agronegócio

Este sistema foi criado para ajudar produtores de cana-de-açúcar a controlar e reduzir as perdas durante a colheita.

### Contexto

O Brasil é líder mundial na produção de cana-de-açúcar, colhendo cerca de 620 milhões de toneladas por safra. Porém, as perdas durante a colheita são muito altas:
- Colheita manual: até 5% de perda
- Colheita mecânica: até 15% de perda

### Impacto das Perdas

Segundo a SOCICANA, as perdas na colheita mecanizada chegam a comprometer seriamente a produtividade:
- No estado de São Paulo, com 3 milhões de hectares plantados
- Produtividade média de 100 toneladas por hectare
- As perdas de 15% equivalem a R$ 20 milhões de prejuízo anual apenas em São Paulo
- Além do prejuízo para o produtor, o governo também perde em arrecadação

### Como o Sistema Resolve o Problema

Ao registrar sistematicamente os dados de cada colheita, o produtor consegue:
1. Identificar padrões de perda em diferentes propriedades
2. Comparar a eficiência entre colheita manual e mecânica
3. Calcular o impacto financeiro real das perdas
4. Tomar decisões baseadas em dados concretos sobre qual método usar
5. Identificar as propriedades com melhores práticas e replicar o sucesso

## Solução

Sistema completo de gestão de colheitas que permite:

### Cadastro e Consulta
- Cadastrar dados de cada colheita (propriedade, data, tipo, toneladas, preço)
- Listar todas as colheitas com detalhes
- Visualizar dados em formato de tabela de memória

### Cálculos Automáticos
- Calcular automaticamente perdas baseadas no tipo de colheita
- Calcular prejuízo financeiro em reais
- Gerar relatórios com totais e estatísticas

### Análises e Comparações
- Comparar desempenho entre colheita manual e mecânica
- Calcular economia potencial ao mudar o método de colheita
- Identificar propriedades com melhor desempenho
- Análise estatística completa usando pandas

### Persistência de Dados
- Salvar dados em arquivo JSON e CSV
- Gerar relatórios formatados em arquivo TXT
- Armazenar dados em banco Oracle para análise histórica
- Carregar dados salvos anteriormente

## Exemplo de Fluxo de Trabalho

1. Cadastrar colheitas realizadas na semana
2. Visualizar relatório total para entender o impacto geral
3. Comparar tipos de colheita para ver qual teve melhor desempenho
4. Verificar estatísticas por propriedade para identificar melhores práticas
5. Calcular economia potencial se mudar o método de colheita
6. Salvar dados em arquivo e banco para histórico
7. Gerar relatório em TXT para apresentar aos gestores

## Como usar

Execute o arquivo principal:
```
python sistema.py
```

## Requisitos

- Python 3.x
- Biblioteca pandas: `pip install pandas`
- Biblioteca oracledb (para banco de dados): `pip install oracledb`
