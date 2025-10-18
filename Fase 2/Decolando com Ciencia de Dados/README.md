# Analise de Dados de Producao Agricola

## Descricao

Analise exploratoria de dados sobre producao agricola no Brasil usando R.

## Base de Dados

O arquivo `dados_producao_agricola.csv` contem 32 linhas com informacoes sobre producao agricola:

### Variaveis

- **area_plantada** (quantitativa discreta): Area plantada em hectares
- **producao** (quantitativa continua): Producao em toneladas
- **regiao** (qualitativa nominal): Regiao do Brasil
- **tamanho_propriedade** (qualitativa ordinal): Pequena, Media ou Grande

Outras variaveis: cultura, produtividade, qualidade

## Analises Realizadas

### Analise Quantitativa (Producao)

- Medidas de Tendencia Central: media, mediana, moda
- Medidas de Dispersao: variancia, desvio padrao, amplitude, coeficiente de variacao
- Medidas Separatrizes: quartis, amplitude interquartil
- Graficos: histograma, boxplot, dispersao, densidade

### Analise Qualitativa (Cultura)

- Distribuicao de frequencia
- Grafico de barras
- Grafico de pizza

## Como Executar

No R, execute:

```r
source("analise.R")
```
