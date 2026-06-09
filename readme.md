# FarmTech Solutions — FIAP ON | Inteligência Artificial

**Aluno:** Diego Filipe Pereira de Araujo — RM567064  
**Tutor(a):** Sabrina Otoni | **Coordenador(a):** André Godoi Chiovato  
**Curso:** Graduação em Inteligência Artificial — FIAP ON

---

## Visão Geral do Projeto

FarmTech Solutions é um sistema integrado de gestão agrícola inteligente construído ao longo de 7 fases do curso. A solução cobre desde o cálculo básico de insumos até visão computacional com redes neurais, passando por banco de dados relacional, IoT com ESP32, Machine Learning, cloud computing na AWS e um dashboard unificado com serviço de alertas.

---

## Estrutura de Pastas

```
FIAP-ON-AI/
├── Fase 1/
│   ├── ia-e-seu-mundo-de-possibilidades/   # Teachable Machine
│   └── play-na-sua-carreira-em-ia/         # Python + R agrícola
├── Fase 2/
│   ├── Python e Alem/                      # Sistema colheita cana + Oracle DB
│   ├── Decolando com Ciencia de Dados/     # Análise R produção agrícola
│   └── Um Mapa do Tesouro/                 # ESP32 + IoT irrigação
├── Fase 4/
│   └── Capitulo 1/                         # Dashboard Streamlit + ML pipeline
├── Fase 5/
│   └── Capitulo 1/                         # ML notebook + estimativa AWS
├── Fase 6/
│   └── Capitulo 1/                         # YOLO + CNN visão computacional
└── Fase_7/
    ├── dashboard.py                         # Dashboard integrado (entrega final)
    ├── alertas_aws.py                       # Módulo de alertas AWS SNS
    └── requirements.txt
```

---

## Fase 1 — Base de Dados Inicial

**Pasta:** `Fase 1/play-na-sua-carreira-em-ia/`

Sistema em Python (CLI) para gestão inicial de culturas agrícolas. O operador seleciona a cultura (Café ou Soja) e informa as dimensões da área; o sistema calcula área e insumos necessários e exporta os dados para CSV.

### Cálculos implementados

| Cultura | Geometria da área | Insumo calculado |
|---------|-------------------|------------------|
| Café    | Retângulo (comp × larg) | N: 150 kg/ha · P: 100 kg/ha · K: 150 kg/ha |
| Soja    | Triângulo (comp × larg / 2) | Água: 8.000 m³/ha |

### Análise estatística em R

O script `analise_farm_tech.r` processa o CSV gerado pelo Python e produz estatísticas descritivas e análise meteorológica via API pública. O arquivo `analise_metereologica_extra.r` aprofunda a análise climática com gráficos e métricas sazonais.

### Operações disponíveis no menu

- Calcular área de plantio
- Calcular manejo de insumos (e exportar para `dados_da_coleta.csv`)
- Alterar dados da cultura
- Escolher outra cultura

---

## Fase 2 — Banco de Dados Estruturado e IoT

### 2a — Sistema de Colheita de Cana-de-Açúcar

**Pasta:** `Fase 2/Python e Alem/`  
**Arquivo:** `sistema.py`

Sistema completo de controle de colheita com persistência múltipla:

- **Cadastro:** propriedade, data, tipo (manual / mecânica), toneladas, preço
- **Cálculo de perda:** 5% para manual, 15% para mecânica
- **Persistência:** JSON + CSV via pandas, e banco Oracle (FIAP) via `oracledb`
- **Análises:** comparação entre tipos, economia potencial, estatísticas por propriedade, análise completa com `pandas.groupby`

### 2b — Análise de Produção Agrícola em R

**Pasta:** `Fase 2/Decolando com Ciencia de Dados/`

Script R (`analise.R`) sobre `dados_producao_agricola.csv` com análise exploratória e estatísticas descritivas de produção.

### 2c — Sistema IoT de Irrigação (ESP32)

**Pasta:** `Fase 2/Um Mapa do Tesouro/codigo/`

Circuito ESP32 com sensores físicos para irrigação automatizada. Esta entrega cobre o conteúdo de IoT descrito na Fase 3 do projeto.

**Hardware:**

| Componente | Pino ESP32 | Função |
|---|---|---|
| DHT22 | GPIO 15 | Umidade do solo |
| LDR | GPIO 34 (ADC) | Proxy de pH (mapeado 0–14) |
| Botão N | GPIO 12 | Toggle Nitrogênio |
| Botão P | GPIO 14 | Toggle Fósforo |
| Botão K | GPIO 27 | Toggle Potássio |
| Relé bomba | GPIO 26 | Acionamento da irrigação |

**Lógica de irrigação (`sistema_irrigacao.ino`):**

A bomba é acionada quando **todas** as condições são atendidas simultaneamente:

1. Umidade < 60%
2. pH entre 5,5 e 7,0
3. N, P e K presentes

Se qualquer condição falha, a bomba permanece desligada e o motivo é impresso no Serial (115200 baud, ciclo de 2 s).

O arquivo `consulta_clima.py` integra a API Open-Meteo para leitura climática em tempo real, e `analise_irrigacao.r` processa os dados históricos do sensor.

---

## Fase 4 — Dashboard Interativo com Machine Learning

**Pasta:** `Fase 4/Capitulo 1/`

Dashboard Streamlit com pipeline de Machine Learning treinado em dados agrícolas sintéticos (200 amostras, `numpy.random.seed(42)`).

### Modelos treinados (scikit-learn LinearRegression)

| Modelo | Target | Features principais |
|---|---|---|
| Rendimento | kg/hectare | umidade, pH, N, P, K + interações |
| Volume irrigação | L/ha | umidade², pH distância, NPK |
| Necessidade fertilização | score 0–10 | ausência de nutrientes, pH ruim |
| Umidade prevista | % | NPK, rendimento normalizado |
| pH previsto | valor | NPK, rendimento normalizado |

### Funcionalidades da dashboard

- Previsão de rendimento interativa (sliders + checkboxes)
- Recomendações de irrigação e fertilização com nível de urgência
- Matriz de correlação (heatmap seaborn)
- Visualização dos dados de treinamento

### Como executar (Fase 4)

```bash
cd "Fase 4/Capitulo 1"
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Fase 5 — Cloud Computing e Segurança na AWS

**Pasta:** `Fase 5/Capitulo 1/`

### Entrega 1 — Machine Learning com crop_yield.csv

Notebook Jupyter com análise completa do dataset `crop_yield.csv`:

- EDA (análise exploratória de dados)
- Clusterização com K-Means para identificação de tendências e outliers
- Cinco modelos de regressão: Linear, Ridge, Árvore de Decisão, K-Vizinhos, Floresta Aleatória
- Métricas de avaliação: MAE, RMSE, R²

**Notebook:** [src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase5.ipynb](Fase%205/Capitulo%201/src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase5.ipynb)  
**Vídeo:** [Demonstração Entrega 1 — EDA e ML](https://youtu.be/WRL_nfjpBZo)

### Entrega 2 — Estimativa de Custos AWS

Comparação de custo mensal para hospedar o modelo (EC2 On-Demand, 2 vCPUs, 1 GiB RAM, 50 GB EBS, Linux):

| Região | Código | Custo mensal (USD) |
|--------|--------|--------------------|
| São Paulo | sa-east-1 | 14,08 |
| Virgínia do Norte | us-east-1 | 8,38 |

**Recomendação:** Virgínia do Norte para menor custo; São Paulo quando há restrições legais LGPD ou necessidade de baixa latência no Brasil.

**Vídeo:** [Demonstração Entrega 2 — calculadora AWS](https://youtu.be/9L8GuhoJf-Y)

---

## Fase 6 — Visão Computacional com Redes Neurais

**Pasta:** `Fase 6/Capitulo 1/`

### Entrega 1 — YOLO treinado do zero

Modelo YOLOv5 treinado para detecção de saúde das plantações:

- 80 imagens anotadas no Make Sense IA (split train/valid/test)
- Treino em 30 épocas e 60 épocas para comparação de convergência
- Métricas: mAP, precision, recall por classe

**Dataset YAML:** `data_fase6.yaml`

### Entrega 2 — Comparação de Abordagens

Três abordagens comparadas em quatro critérios (acurácia, tempo de treino, complexidade, generalização):

1. YOLO treinado na Entrega 1 (domínio específico)
2. YOLO pré-treinada no COCO (transfer learning)
3. CNN simples treinada do zero (baseline)

| Notebook | Google Colab |
|---|---|
| [Entrega 1](Fase%206/Capitulo%201/src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6.ipynb) | [Abrir no Colab](https://colab.research.google.com/drive/10TWiqWN55SFTNgBIh50atKXMN3rVP3Gw?usp=sharing) |
| [Entrega 2](Fase%206/Capitulo%201/src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6_entrega2.ipynb) | [Abrir no Colab](https://colab.research.google.com/drive/1lFFpfhOYb88yqfQx30W2wETNjt9kpI7R?usp=sharing) |

**Vídeo:** [Demonstração Fase 6](https://youtu.be/lEjT5GtKMig)

---

## Fase 7 — Dashboard Integrado e Alertas AWS

**Pasta:** `Fase_7/`

### Dashboard unificado

O arquivo `dashboard.py` consolida todas as fases em uma única aplicação Streamlit com navegação por sidebar:

| Página | Conteúdo integrado |
|---|---|
| Visão Geral | Métricas globais: colheitas, leituras de sensor, alertas ativos |
| Fase 1 — Área e Insumos | Cálculo interativo de área e insumos (Café/Soja) com tabela exportável |
| Fase 2 — Gestão de Colheita | CRUD de colheitas, download CSV, relatório comparativo por tipo |
| Fase 3 — Sensores IoT | Simulação de leituras DHT22/LDR, histórico de umidade e pH, lógica de bomba |
| Fase 4 — Previsões ML | Modelos LinearRegression em tempo real: rendimento, irrigação, fertilização |
| Fase 6 — Visão Computacional | Upload de imagem, análise por distribuição de cores (verde/amarelo/marrom), score de saúde |
| Alertas AWS | Composição e envio de alertas via AWS SNS (ou simulação offline) |

### Como executar

```bash
cd Fase_7
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Serviço de Mensageria AWS SNS

**Arquivo:** `Fase_7/alertas_aws.py`

O módulo implementa alertas automáticos via **AWS Simple Notification Service (SNS)**, integrando dados das Fases 1, 3 e 6 para notificação de operadores de campo por e-mail ou SMS.

### Funções disponíveis

```python
from alertas_aws import (
    alerta_umidade_critica,       # Fase 3 — DHT22 abaixo do limite
    alerta_ph_fora_faixa,         # Fase 3 — LDR fora de 6.0–8.0
    alerta_visao_computacional,   # Fase 6 — score de saúde crítico
    alerta_irrigacao_urgente,     # Fase 4 — ML indica volume urgente
)
```

### Exemplo de uso

```python
alerta_umidade_critica(
    topico_arn="arn:aws:sns:us-east-1:123456789012:farmtech-alertas",
    umidade_atual=32.5
)
```

A mensagem enviada contém timestamp, valor do sensor, limite de referência e ação corretiva recomendada.

### Configuração do tópico SNS

1. AWS Console → **SNS** → **Topics** → **Create topic** (tipo: Standard)
2. Adicionar subscription: Protocol **Email** ou **SMS** → inserir destinatário
3. Confirmar a assinatura via e-mail recebido
4. Configurar credenciais locais: `aws configure` (ou variáveis `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`)
5. Inserir o Topic ARN na dashboard na página **Alertas AWS**

### Por que não há prints da AWS Console nesta documentação

A solicitação original pede prints do SNS configurado na AWS. Optamos por não incluí-los por uma questão de **responsabilidade de custo e sustentabilidade**:

- Criar um tópico SNS ativo com subscription de e-mail/SMS e mantê-lo apenas para fins de documentação gera cobranças recorrentes (por publicação e por entrega), mesmo sem uso real em produção.
- O projeto é acadêmico e solo; provisionar infraestrutura AWS permanente para screenshots de documentação introduziria custos sem contrapartida operacional.
- O código em `alertas_aws.py` e a integração na dashboard são suficientes para demonstrar a arquitetura; a configuração do SNS é reproduzível a partir dos passos acima em menos de 5 minutos em qualquer conta AWS, incluindo o Free Tier para os primeiros 1.000 e-mails/mês.
- A **simulação offline** disponível na dashboard (botão "Simular (sem AWS)") permite validar o fluxo completo — composição de mensagem, templates de alerta, integração com leituras dos sensores — sem necessidade de credenciais AWS.

---

## Dependências

### Fase 4 e Fase_7 (dashboard e ML)

```
streamlit
pandas
numpy
matplotlib
seaborn
scikit-learn
Pillow
boto3
```

Instalação:

```bash
pip install -r Fase_7/requirements.txt
```

### Fase 5 (notebook ML)

```bash
pip install -r "Fase 5/Capitulo 1/requirements.txt"
```

### Fase 6 (YOLO — Google Colab recomendado)

```bash
pip install -r "Fase 6/Capitulo 1/requirements.txt"
```

---

## Licença

Attribution 4.0 International — conforme template FIAP.
