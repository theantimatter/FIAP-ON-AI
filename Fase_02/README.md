# CardioIA — Fase 2: Diagnóstico Assistido por IA

**Aluno:** Diego Filipe Pereira de Araujo — RM567064
**Curso:** Bacharelado em Inteligência Artificial — FIAP ON (2º ano)
**Entrega:** Fase 2 — NLP, extração de sintomas e classificação de risco

**Vídeo de demonstração (YouTube, não listado):** https://youtu.be/T61K493zCE0

A gravação também está em `video/cardioia_fase2_demo.mov` (1920×1080, 3min26). O arquivo tem 55 MB e não é versionado no Git, assim como as imagens de ECG da Fase 1.

---

## Sobre esta entrega

A Fase 1 montou o laboratório: três bases de dados reais, licenciadas e documentadas. Esta fase é a primeira em que o CardioIA **faz algo** com texto.

São dois módulos independentes que resolvem problemas diferentes do mesmo fluxo de atendimento:

| Parte | Pergunta que responde | Técnica |
|---|---|---|
| **1 — Extração de sintomas** | *O que este paciente está descrevendo?* | mapa de conhecimento + casamento de expressões |
| **2 — Classificador de risco** | *Quem precisa ser atendido primeiro?* | TF-IDF + regressão logística |

A separação é proposital. A Parte 1 usa uma regra explícita, auditável, em que cada sugestão pode ser rastreada até a linha do CSV que a gerou. A Parte 2 usa aprendizado estatístico, acerta mais em frases que ninguém previu e, em troca, não consegue explicar direito por que decidiu. As duas abordagens convivem em sistemas hospitalares reais justamente porque esse trade-off não tem solução única.

---

## Estrutura

```
Fase_02/
├── README.md                          este documento
├── atividade.md                       enunciado da fase
├── mapa_mental.png                    mapa mental do PBL
├── dados/
│   ├── relatos_pacientes.txt          Parte 1 — 10 relatos de sintomas
│   ├── mapa_conhecimento.csv          Parte 1 — 40 linhas de sintoma → doença
│   └── frases_risco.csv               Parte 2 — 72 frases rotuladas por risco
├── scripts/
│   └── extrair_sintomas.py            Parte 1 — leitura, extração e sugestão
├── notebooks/
│   └── parte2_classificador_risco.ipynb   Parte 2 — TF-IDF, treino e avaliação
├── saidas/
│   └── diagnosticos_sugeridos.csv     Parte 1 — resultado da execução
└── video/
    └── cardioia_fase2_demo.mov        demonstração em vídeo (fora do Git)
```

## Como reproduzir

```bash
pip install pandas scikit-learn matplotlib jupyter

python Fase_02/scripts/extrair_sintomas.py
jupyter notebook Fase_02/notebooks/parte2_classificador_risco.ipynb
```

O script não depende de rede nem de arquivos externos. O notebook lê `dados/frases_risco.csv` e, na seção de viés, `../../Fase_01/dados/cardioia_pacientes.csv`.

---

## Parte 1 — Relatos, mapa de conhecimento e extração

### Os relatos

[`dados/relatos_pacientes.txt`](dados/relatos_pacientes.txt) traz 10 frases, uma por linha, escritas como um paciente descreve o próprio quadro. Cada uma carrega as três informações que o enunciado pede: **o que sente**, **quando começou** e **como isso afeta a rotina**.

> *"Faz uns quinze dias que acordo com as pernas inchadas e preciso dormir sentado porque sinto falta de ar quando me deito."*

Os dez casos cobrem quadros diferentes de propósito — angina, infarto, insuficiência cardíaca, arritmia, hipertensão, pericardite, doença arterial periférica, trombose venosa e estenose aórtica. Uma base em que todos os relatos falassem de dor no peito não testaria nada.

### O mapa de conhecimento

[`dados/mapa_conhecimento.csv`](dados/mapa_conhecimento.csv) tem **40 linhas** no formato pedido:

| sintoma_1 | sintoma_2 | doenca_associada |
|---|---|---|
| aperto no tórax | peso no peito | Angina estável |
| irradia para o braço esquerdo | dor no braço esquerdo | Infarto agudo do miocárdio |
| cansaço constante | fadiga | Insuficiência cardíaca |
| coração acelerado | taquicardia | Arritmia cardíaca |

Cada linha reúne duas formas de dizer a mesma coisa e a doença à qual elas apontam. São 80 expressões distribuídas em **12 condições**. Três delas — acidente vascular cerebral, miocardite e transtorno de ansiedade — não aparecem em nenhum dos dez relatos: estão ali como diagnósticos diferenciais, porque um mapa que só contém as respostas certas não é um mapa, é um gabarito.

### A extração

[`scripts/extrair_sintomas.py`](scripts/extrair_sintomas.py) faz quatro coisas:

1. **Normaliza** relato e expressões — minúsculas e remoção de acentos, para que "tórax" case com "torax" e o CSV não precise prever cada grafia.
2. **Procura da expressão mais longa para a mais curta** e marca o trecho já consumido. Isso resolve a sobreposição: em *"dor no peito que piora ao respirar"*, a expressão longa (Pericardite) vence e impede que o pedaço *"dor no peito"* (Infarto) seja contado de novo no mesmo trecho. Sem essa regra, toda frase que mencionasse o peito puxaria infarto.
3. **Conta os votos** de cada doença entre as expressões encontradas e sugere a mais apoiada, declarando empate quando houver.
4. **Grava** o resultado em [`saidas/diagnosticos_sugeridos.csv`](saidas/diagnosticos_sugeridos.csv), com os sintomas que sustentam cada sugestão.

### Resultado

Os 10 relatos receberam sugestão, nenhum empate:

| Paciente | Sintomas identificados | Diagnóstico sugerido | Apoio |
|---|---|---|:-:|
| P01 | aperto no tórax; subo as escadas; minutos de repouso | Angina estável | 3 |
| P02 | dor no peito; irradia para o braço esquerdo; suor frio | Infarto agudo do miocárdio | 3 |
| P03 | cansaço constante; mesmo depois de descansar; não consigo terminar a caminhada | Insuficiência cardíaca | 3 |
| P04 | pernas inchadas; dormir sentado; falta de ar quando me deito | Insuficiência cardíaca | 3 |
| P05 | coração acelerado; palpitações | Arritmia cardíaca | 2 |
| P06 | dor de cabeça forte; nuca pesada; visão turva | Hipertensão arterial | 3 |
| P07 | dor no peito que piora ao respirar; inclino para frente | Pericardite | 2 |
| P08 | dor na perna ao caminhar; esperar a dor passar | Doença arterial periférica | 2 |
| P09 | perna inchada e dolorida; quente e vermelha | Trombose venosa profunda | 2 |
| P10 | tontura ao subir escada; sopro no coração; quase desmaiei | Estenose aórtica | 3 |

### Limites honestos desta abordagem

O módulo só reconhece o que está escrito no CSV. Um paciente que diga "o peito tá fechando" não é compreendido, porque essa expressão não foi cadastrada — e o resultado é um silêncio, não um erro visível. Ele também é cego a negação e a tempo verbal: *"já tive dor no peito no ano passado"* conta como se a dor fosse de agora. Resolver isso exige o que vem nas próximas fases: lematização, listas de negação e modelos que olhem a estrutura da frase, não só a presença do termo.

---

## Parte 2 — Classificador de risco

Todo o desenvolvimento está em [`notebooks/parte2_classificador_risco.ipynb`](notebooks/parte2_classificador_risco.ipynb), com as saídas salvas.

### A base

[`dados/frases_risco.csv`](dados/frases_risco.csv) — **72 frases** nas colunas `frase` e `situacao`, com 36 de cada classe. O equilíbrio é deliberado: com classes desbalanceadas, um modelo que respondesse sempre a majoritária já acertaria a maioria e a acurácia esconderia o problema.

### O pipeline

**TF-IDF** com `ngram_range=(1, 2)` e `min_df=2`. Os bigramas importam porque "falta de ar" só tem sentido clínico como expressão inteira; o `min_df=2` evita que uma palavra escrita uma única vez ganhe IDF máximo e se transforme numa impressão digital daquela frase. O resultado é uma matriz 72 × 140.

**Regressão logística** contra **árvore de decisão**, divisão 75/25 estratificada. A regressão ganhou com folga (88,9% contra 72,2%) e foi a escolhida também por devolver probabilidade em vez de rótulo seco — o que permite calibrar o limiar da fila — e por ter coeficientes legíveis.

### Resultados

| Métrica | Valor |
|---|---|
| Acurácia no teste (18 frases) | **88,9%** |
| Acurácia em validação cruzada (5 partes) | **90,5%** (desvio 9,0) |
| Recall da classe *alto risco* | **0,778** |
| Precision da classe *alto risco* | 1,000 |

A acurácia não é a métrica que importa aqui. Classificar baixo risco como alto gera um atendimento desnecessário; classificar **alto risco como baixo** manda para o fim da fila alguém que pode estar infartando. O recall de 0,778 significa que **2 dos 9 casos graves do teste foram rebaixados** — e são esses dois que decidem se o sistema serve ou não.

### Distorções encontradas

O notebook testa o modelo com frases novas e difíceis. Três falhas aparecem:

**Uma palavra pesa mais que o quadro clínico.** As frases *"dor no peito que irradia para o braço esquerdo"* e *"dor **leve** no peito que irradia para o braço esquerdo"* descrevem o mesmo quadro. A probabilidade de alto risco cai de **0,739 para 0,617** por causa do adjetivo. `leve` é o termo de maior peso para baixo risco em toda a base — porque nós o escrevemos em quase todas as frases brandas, e a correlação virou atalho.

**O atalho erra.** *"sinto um leve cansaço mas também falta de ar quando me deito"* sai como **baixo risco (0,420)**. Falta de ar ao deitar é ortopneia, sinal de alarme de insuficiência cardíaca — mas os três termos de maior peso para baixo risco (`leve`, `mas`, `um`) estão todos na frase.

**Negação é invisível.** *"não sinto dor no peito nem falta de ar"* é classificada como **alto risco com 0,793**. Para o TF-IDF, "não" é apenas mais um termo. Em prontuário médico, onde "nega dor torácica" é construção padrão, isso inviabilizaria o uso direto.

Há ainda um padrão revelador nos coeficientes: do lado do baixo risco, depois de `leve`, vêm `depois`, `mas`, `um`, `uma`, `tive`, `um pouco` — nenhum deles descreve sintoma. São marcas de **estilo de escrita**: as frases brandas que escrevemos tendem ao passado e ao atenuador, as graves ao presente. O modelo aprendeu a reconhecer o nosso jeito de escrever junto com a gravidade, e parte da acurácia de 90% vem daí.

---

## Governança de dados e viés

A Fase 1 declarou os vieses das bases coletadas. Aqui eles cobram a conta.

### O viés da Fase 1 atravessa para a Fase 2

A base Cleveland usada na Fase 1 tem **68% de homens** (206 de 303 pacientes, idade média 54,4 anos) — o notebook recalcula esse número a partir do CSV original. A doença coronariana se manifesta de forma diferente em mulheres, com mais sintomas atípicos: náusea, fadiga, dor nas costas e na mandíbula, em vez do aperto retroesternal clássico.

Isso contaminou as duas partes desta fase. O mapa de conhecimento foi montado em torno de dor no peito e falta de ar; as frases de alto risco giram nos mesmos termos. Um sistema calibrado assim tende a classificar como baixo risco justamente o relato típico de uma paciente infartando — e o erro seria invisível na acurácia, porque o conjunto de teste tem o mesmo viés do treino.

### Dados sintéticos têm limite claro

As 72 frases e os 10 relatos foram escritos por uma pessoa só. Isso garante que não há dado pessoal de ninguém envolvido — não há questão de LGPD nesta entrega, diferente das imagens de ECG da Fase 1 — mas produz um vocabulário uniforme, sem erros de digitação, sem gíria regional e sem a vagueza de quem está com dor. A acurácia medida aqui é um **limite superior otimista**.

### Onde esta solução pode e não pode ser usada

Ambos os módulos servem para **ordenar uma fila**, nunca para dispensar um paciente. A Parte 1 sugere hipóteses para o profissional confirmar; a Parte 2 prioriza. Nenhuma das duas decide. Um sistema que usasse esses 90% de acurácia para mandar alguém para casa estaria errando com uma em cada dez pessoas, e o notebook mostra exatamente quais frases ele erra.

---

## Referências

1. JANOSI, A.; STEINBRUNN, W.; PFISTERER, M.; DETRANO, R. **Heart Disease**. UCI Machine Learning Repository, 1988. DOI: [10.24432/C52P4X](https://doi.org/10.24432/C52P4X)

2. OLIVEIRA, G. M. M. et al. **Estatística Cardiovascular – Brasil 2023**. *Arquivos Brasileiros de Cardiologia*, v. 121, n. 2, e20240079, 2024. DOI: [10.36660/abc.20240079](https://doi.org/10.36660/abc.20240079)

3. PEDREGOSA, F. et al. **Scikit-learn: Machine Learning in Python**. *Journal of Machine Learning Research*, v. 12, p. 2825-2830, 2011.

4. Entrega da Fase 1 do CardioIA, com a documentação completa das bases e dos vieses: [`Fase_01/README.md`](../Fase_01/README.md)
