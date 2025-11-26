# FarmTech Solutions - PARTE 1
## Assistente Agrícola Inteligente com Machine Learning

Este projeto implementa um sistema de Machine Learning para previsão de rendimento agrícola usando regressão linear e um dashboard interativo desenvolvido com Streamlit.

## 📋 Descrição

A PARTE 1 do projeto consiste em:
- Pipeline completo de Machine Learning usando Scikit-Learn
- Modelo de regressão linear múltipla para prever rendimento agrícola
- Dashboard interativo em Streamlit para visualização de métricas, correlações e previsões em tempo real

## 🚀 Como Usar

### 1. Instalação das Dependências

Primeiro, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 2. Treinar o Modelo

Execute o script de pipeline de Machine Learning para gerar os dados e treinar o modelo:

```bash
python ml_pipeline.py
```

Este script irá:
- Gerar dados agrícolas simulados (200 amostras)
- Treinar um modelo de regressão linear
- Salvar o modelo em `modelos/modelo_regressao.pkl`
- Salvar os dados em `dados_agricolas.csv`
- Salvar as métricas em `metricas_modelo.csv`

### 3. Executar o Dashboard

Após treinar o modelo, execute o dashboard Streamlit:

```bash
streamlit run dashboard.py
```

O dashboard será aberto automaticamente no seu navegador (geralmente em `http://localhost:8501`).

## 📊 Funcionalidades do Dashboard

O dashboard possui 4 seções principais:

### 🏠 Visão Geral
- Estatísticas gerais dos dados
- Resumo dos dados coletados
- Estatísticas descritivas

### 📈 Métricas de Desempenho
- **MAE** (Mean Absolute Error): Erro médio absoluto
- **MSE** (Mean Squared Error): Erro quadrático médio
- **RMSE** (Root Mean Squared Error): Raiz do erro quadrático médio
- **R²** (Coeficiente de Determinação): Qualidade do modelo

### 🔍 Análise de Correlação
- Mapa de calor de correlação entre todas as variáveis
- Gráficos de dispersão (Umidade vs Rendimento, pH vs Rendimento)
- Análise do impacto dos nutrientes NPK no rendimento

### 🔮 Previsões
- Interface interativa para fazer previsões em tempo real
- Sliders para ajustar umidade e pH
- Checkboxes para indicar presença de nutrientes (N, P, K)
- Recomendações baseadas nos valores inseridos

## 📁 Estrutura de Arquivos

```
parte1/
├── ml_pipeline.py          # Script de pipeline ML e treinamento
├── dashboard.py            # Dashboard Streamlit
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── modelos/               # Pasta criada automaticamente
│   └── modelo_regressao.pkl
├── dados_agricolas.csv    # Dados gerados (criado após executar ml_pipeline.py)
└── metricas_modelo.csv    # Métricas do modelo (criado após executar ml_pipeline.py)
```

## 🔬 Variáveis do Modelo

O modelo utiliza as seguintes variáveis para prever o rendimento:

- **Umidade do Solo** (0-100%): Nível de umidade do solo
- **pH do Solo** (0-14): Acidez/alcalinidade do solo
- **Nitrogênio (N)** (0 ou 1): Presença ou ausência de nitrogênio
- **Fósforo (P)** (0 ou 1): Presença ou ausência de fósforo
- **Potássio (K)** (0 ou 1): Presença ou ausência de potássio

**Variável Alvo:**
- **Rendimento** (kg/hectare): Produtividade esperada da cultura

## 📚 Bibliotecas Utilizadas

- **pandas**: Manipulação e análise de dados
- **numpy**: Operações numéricas
- **scikit-learn**: Machine Learning (regressão linear)
- **streamlit**: Interface web interativa
- **matplotlib**: Visualizações básicas
- **seaborn**: Visualizações estatísticas avançadas
- **joblib**: Salvamento e carregamento de modelos

## 🎓 Conceitos Aplicados

Este projeto demonstra:
- **Regressão Linear Múltipla**: Modelo de ML supervisionado
- **Divisão de Dados**: Treino e teste (80/20)
- **Métricas de Avaliação**: MAE, MSE, RMSE, R²
- **Visualização de Dados**: Gráficos de correlação e dispersão
- **Interface Interativa**: Dashboard para gestores agrícolas

## ⚠️ Observações

- Este é um projeto educacional de nível introdutório
- Os dados são simulados para fins didáticos
- O modelo é simples e adequado para aprendizado básico de ML
- Para uso em produção, seriam necessários dados reais e modelos mais sofisticados

## 👨‍💻 Autor

Projeto desenvolvido para a Fase 4 - Capítulo 1 do curso FIAP ON AI.

## 📝 Licença

Este projeto é para fins educacionais.

