# FarmTech Solutions - Assistente Agrícola Inteligente

Sistema de Machine Learning para previsão de variáveis agrícolas e recomendações de ações de manejo.

## Descrição

Sistema completo que utiliza regressão linear múltipla para prever:
- Rendimento agrícola (kg/hectare)
- Umidade do solo (%)
- pH do solo
- Volume de irrigação necessário (litros/hectare)
- Necessidade de fertilização (0-10)

Inclui dashboard interativo em Streamlit e banco de dados SQLite para armazenamento de dados dos sensores.

## Instalação e Uso

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Treinar Modelos

```bash
python ml_pipeline.py
```

Este comando gera os dados, cria o banco de dados e treina todos os modelos de Machine Learning.

### 3. Executar Dashboard

```bash
streamlit run dashboard.py
```

## Funcionalidades do Dashboard

- **Visão Geral**: Estatísticas e resumo dos dados
- **Métricas de Desempenho**: MAE, MSE, RMSE e R² de todos os modelos
- **Análise de Correlação**: Matriz de correlação e gráficos de dispersão
- **Previsões de Rendimento**: Interface para prever rendimento baseado em condições do solo
- **Previsões de Umidade e pH**: Previsão baseada em nutrientes e rendimento
- **Ações Agrícolas**: Recomendações de irrigação e fertilização com prioridades
- **Análise de Ações**: Visualizações das ações recomendadas

## Estrutura do Projeto

```
Fase 4/Capitulo 1/
├── ml_pipeline.py              # Pipeline de treinamento
├── dashboard.py                # Dashboard Streamlit
├── utils.py                    # Funções auxiliares
├── banco_dados.py              # Gerenciamento do banco SQLite
├── requirements.txt            # Dependências
│
├── dados/                      # Dados gerados
│   ├── dados_agricolas.csv
│   ├── dados_sensores.db
│   └── dados_com_acoes.csv
│
├── modelos/                    # Modelos treinados
│   ├── modelo_rendimento.pkl
│   ├── modelo_umidade.pkl
│   ├── modelo_ph.pkl
│   ├── modelo_irrigacao.pkl
│   └── modelo_fertilizacao.pkl
│
└── metricas/                   # Métricas dos modelos
    ├── metricas_previsao.csv
    └── metricas_acoes.csv
```

## Modelos Implementados

Todos os modelos utilizam regressão linear múltipla do Scikit-Learn:

1. **Modelo de Rendimento**: Previsão baseada em umidade, pH e nutrientes
2. **Modelo de Umidade**: Previsão baseada em nutrientes e rendimento
3. **Modelo de pH**: Previsão baseada em nutrientes e rendimento
4. **Modelo de Irrigação**: Previsão de volume necessário
5. **Modelo de Fertilização**: Previsão de necessidade de fertilização

## Métricas de Avaliação

Todos os modelos são avaliados com:
- **MAE** (Mean Absolute Error)
- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **R²** (Coeficiente de Determinação)

## Banco de Dados

Banco de dados SQLite (`dados_sensores.db`) armazena:
- Timestamp
- Umidade do solo
- pH do solo
- Presença de nutrientes (N, P, K)
- Rendimento

## Sistema de Recomendações

O sistema gera recomendações automáticas com três níveis de prioridade:
- **Alta**: Ações urgentes necessárias
- **Média**: Ações moderadas recomendadas
- **Baixa**: Monitoramento contínuo
