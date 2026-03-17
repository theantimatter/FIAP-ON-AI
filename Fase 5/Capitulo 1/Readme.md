# FarmTech Solutions — Previsão de Rendimento de Safra (Entrega 1)

**FIAP — Graduação em Inteligência Artificial | Fase 5 | PBL**

## Nome do grupo

FarmTech Solutions — Entrega 1

## Integrantes

- Diego Filipe Pereira de Araujo — RM567064

## Professores

- **Tutor(a):** Sabrina Otoni
- **Coordenador(a):** André Godoi Chiovato

---

## Descrição

Projeto da **Entrega 1** (Machine Learning): análise de dados agrícolas da base **crop_yield.csv** (condições de solo e clima) para prever o rendimento de safra. O trabalho inclui análise exploratória (EDA), clusterização (K-Means) para tendências e identificação de outliers, e cinco modelos de regressão (Linear, Ridge, Árvore de Decisão, K-Vizinhos e Floresta Aleatória) com avaliação por métricas (MAE, RMSE, R²).

Todo o passo a passo, resultados e conclusões estão no **notebook Jupyter** indicado abaixo.

---

## Link para o notebook

O desenvolvimento completo da solução está no notebook:

- **Arquivo:** [src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase4.ipynb](src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase4.ipynb)

---

## Vídeo de demonstração

*(Inserir aqui o link do vídeo de até 5 minutos no YouTube — modo “não listado” — demonstrando o funcionamento do entregável.)*

---

## Estrutura de pastas

Conforme [template FIAP](https://github.com/agodoi/templateFiapVfinal):

| Pasta / arquivo | Descrição |
|-----------------|-----------|
| `.github` | Configurações do GitHub |
| `assets` | Imagens e elementos não estruturados |
| `config` | Arquivos de configuração e parâmetros |
| `document` | Documentos do projeto (`other/` para complementares) |
| `scripts` | Scripts auxiliares |
| `src` | Código fonte e notebook Jupyter da Entrega 1 |
| `assets/crop_yield.csv` | Dataset (arquivo CSV na pasta assets) |
| `README.md` | Este arquivo |

---

## Como executar

### Pré-requisitos

- **Python** 3.8 ou superior  
- **Jupyter** (ou JupyterLab / VS Code com extensão Jupyter)

### Instalação das dependências

Na pasta do projeto (onde está o `requirements.txt`):

```bash
pip install -r requirements.txt
```

Ou instale manualmente: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `jupyter`.

### Execução do notebook

1. Clone o repositório (ou baixe os arquivos).
2. O dataset `crop_yield.csv` está em `assets/`; o notebook já referencia `../assets/crop_yield.csv`.
3. Abra o notebook em `src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase4.ipynb` no Jupyter e execute as células em ordem (Run All).

---

## Histórico de lançamentos

- **0.1.0** — Entrega 1: EDA, clusterização e modelos de regressão para previsão de rendimento.

---

## Licença

Attribution 4.0 International (template FIAP).
