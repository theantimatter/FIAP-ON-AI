# Projeto integrador — Fase 6

Documento da disciplina FIAP — graduação em IA (visão computacional e redes neurais).

---

## 1. Descrição rápida do projeto

Para a **Fase 6**, você vai desenvolver uma **rede neural** aplicada ao projeto FarmTech Solutions.

Além das entregas obrigatórias, há **duas entregas extras (“Ir Além”)**, que **não entram na nota**.

Assim como na fase anterior, esperamos que os grupos se desafiem com essas entregas extras. Como recompensa de quem entregar “Ir Além”, os grupos ganham **gratificações** (não notas), explicadas ao longo das lives e neste documento.

---

## 2. Descrição detalhada do projeto

### Entrega 1 — Visão computacional com YOLO

A **FarmTech Solutions** está expandindo os serviços de IA além do agronegócio. A carteira de clientes cresceu e a empresa passou a atuar em:

- saúde animal;
- segurança patrimonial de fazendas e residências;
- controle de acesso de funcionários;
- análise de documentos de diversos tipos;
- **visão computacional**.

Nesta entrega, você faz parte do time de desenvolvimento da FarmTech e visita um cliente que quer **entender na prática** como funciona um sistema de **visão computacional**.

**Objetivo:** criar um sistema de visão computacional usando **YOLO**, demonstrando potencial e acurácia. Você é livre para escolher o **cenário de imagens** usado em treino, validação e testes.

#### Metas da Entrega 1

1. Organizar um dataset com **no mínimo 40 imagens** de um **objeto A** e **+40 imagens** de um **objeto B** bem diferente do A, totalizando **80 imagens**.
2. Das 40 imagens do objeto A: **32 treino**, **4 validação**, **4 teste**. Repetir o mesmo split para o objeto B.
3. Organizar as imagens no **Google Drive** (pessoal ou do grupo), em pastas de **treino**, **validação** e **teste**.
4. Rotular as imagens de **treinamento** com o site **Make Sense IA**.
5. Salvar as rotulações no Google Drive.
6. Montar um **Colab** conectado ao Drive capaz de **treinar**, **validar** e **testar**, descrevendo em **Markdown** o passo a passo dessas três etapas.
7. Fazer **pelo menos duas simulações** com **quantidade diferente de épocas** e comparar **acurácia**, **erro** e **desempenho** ao alterar esse parâmetro (ex.: **30 e 60 épocas**, bem diferentes entre si).
8. Apresentar **conclusões** sobre validação e testes. Os resultados aparecem em pastas do tipo `yolov5/runs/detect/expX` (o **X** incrementa a cada treino).
9. Incluir **prints** das imagens de **teste** processadas pelo modelo (para “convencer” o cliente fictício da FarmTech).

#### Entregáveis — Enunciado 1

- Publicar a solução em um **novo repositório GitHub** com o nome do grupo (**1 a 5 pessoas ou solo**) e enviar o link pelo **portal da FIAP** (pode usar PDF com o link).
- **Não fazer commits após a data de entrega** (evita ser classificado como entrega fora do prazo).
- No repositório, incluir o **link do notebook Jupyter** — a correção executará seu notebook.
- O notebook deve conter:
  - **células de código executadas**, Python otimizado e **comentários nas linhas**;
  - **células Markdown** organizando o relatório, com achados e conclusões sobre **pontos fortes** e **limitações**.
- **Nome do arquivo:** deve conter nome completo, RM e `pbl_fase6.ipynb`  
  Exemplo: `JoaoSantos_rm76332_pbl_fase6.ipynb`.
- **Vídeo:** até **5 minutos**, demonstrando o entregável, no YouTube como **“não listado”**, com link no **README**.
- **README:** documentação introdutória que **conduza** o leitor ao Colab/Jupyter (passo a passo completo fica no notebook). **Não repetir** o conteúdo integral do notebook no README — integre a documentação do projeto.
- Repositório **público** para a equipe FIAP acessar; **cuidado** com links para não vazarem ou serem plagiados.

> **Dica:** como subir o Colab Notebook para o Git — [YouTube — FIAP](https://www.youtube.com/watch?v=5ZYRqca7OVc).

---

### Entrega 2 — Comparar abordagens

Agora que você customizou a YOLO na Entrega 1, compare com outras abordagens “concorrentes”.

Na visão computacional **não existe** solução 100% melhor ou pior: depende do **cenário** e dos **critérios** que você define com prática. Mesmo que a YOLO tenha ido bem (ou não), vale experimentar alternativas.

#### Metas da Entrega 2

Com a **mesma base** da Entrega 1:

1. Aplicar a **YOLO tradicional** (capítulo 3 de Redes Neurais) e avaliar o desempenho **em relação** à proposta da Entrega 1.
2. Treinar uma **CNN do zero** para **classificar** a qual classe a imagem pertence.

#### Entregáveis — Enunciado 2

Para cada abordagem (**YOLO da Entrega 1**, **YOLO padrão**, **CNN do zero** — conforme capítulos de Redes Neurais), avalie criticamente comparando:

- facilidade de uso / integração;
- precisão do modelo;
- tempo de treinamento / customização (se aplicável);
- tempo de inferência (predição).

**Notebook Jupyter ou Colab** no GitHub com:

- código executado;
- saídas;
- avaliações;
- Markdown crítico comparando as soluções.

---

## 3. Projeto “Ir Além”

Esta seção descreve **dois entregáveis extras** (não valem nota). Os grupos escolhem qual “Ir Além” desenvolver.

Quem postar solução pode receber gratificação: cada integrante pode ganhar um **troféu de excelência** em busca do “Ir Além” ao final do ano. Grupos que entregarem “Ir Além” nas **Fases 5, 6 e 7** somam pontos internos.

- Cada “Ir Além” vale até **10 pontos** internos (**30 pontos** no total entre as três fases); **não impactam** o boletim.
- A nota do “Ir Além” é divulgada no Teams para quem postou.

No final do ano, os pontos são somados e divulgados no Teams. Entregas incompletas também podem ser avaliadas de **0 a 10** no game interno.

### 3.1 Primeira opção — Coleta de imagem com ESP32

Reconhecer imagens da Entrega 1 com **ESP32-CAM** real **ou** **webcam** no PC + Python lendo o `best.pt` da Entrega 1 conta como “Ir Além”.

Desenvolva um projeto com **ESP32-CAM** e Wi‑Fi coletando imagens em tempo real e transmitindo para o **VS Code** (ou ambiente equivalente) que reconheça os objetos escolhidos. Se não houver os objetos por perto, pode filmar uma **TV** com imagens para testar detecção.

**Etapas:**

- seguir o capítulo de **AI Computer Systems & Sensors** sobre modelagem de imagens customizadas;
- implementar o ESP32-CAM na prática (compra **não** é obrigatória — é “Ir Além”).

**Critérios de avaliação (opção 1):**

| Aspecto | O que é avaliado |
|--------|------------------|
| Funcionalidade | Coleta e envio de dados funcionais |
| Wi‑Fi | Comunicação estável e eficiente |
| Escolha do ESP32-CAM | Clareza e alinhamento ao contexto |
| Documentação GitHub | Código comentado, figura da arquitetura, justificativa |
| Apresentação | Vídeo até 5 min + GitHub organizado |

**Entregável:** notebook/Colab na seção “Ir Além”, código comentado, justificativa com figura autoral, imagens comprovando resultados, vídeo “não listado” no YouTube (até 5 min).

---

### 3.2 Segunda opção — Transfer learning e fine tuning

Além de treinar uma CNN do zero, experimente **transfer learning** + **fine tuning** de uma rede grande treinada na **ImageNet** (ex.: VGG, Inception, MobileNet ou outra no TensorFlow). Investigue implementações e configurações.

**Hipótese 1:** uma rede pré-treinada em dataset enorme performa melhor que uma CNN treinada do zero?

**Segunda abordagem — segmentação + classificação:**

1. Aplicar uma rede de **segmentação** do objeto e gerar **máscara**.
2. Usar a máscara para **recortar** a imagem (objeto em destaque, fundo apagado ou branco/preto).
3. Classificar a imagem recortada com a rede escolhida (do zero ou transfer learning).
4. Comparar **acertos** entre abordagens.

**Hipótese 2:** pré-segmentar o objeto facilita a classificação?

**Critérios de avaliação (opção 2):**

| Aspecto | O que é avaliado |
|--------|------------------|
| Implementação | Duas abordagens, código limpo e comentado |
| Transfer learning | Justificar arquitetura, fine tuning, camadas congeladas, pré-processamento |
| Segmentação | Máscaras automáticas; mostrar original, máscara e recorte |
| Documentação GitHub | Código organizado + avaliações textuais |
| Apresentação | Vídeo até 5 min + GitHub organizado |

**Entregável:** igual à opção 1 (notebook “Ir Além”, figuras, vídeo não listado).

---

## Barema das entregas obrigatórias

Critérios das **Entregas 1 e 2** (nota):

| Critério | Descrição | Peso |
|----------|-----------|------|
| Repositório no GitHub | Criado no prazo; notebook/Colab correto; nomeação do arquivo conforme pedido; **sem commits após o prazo** | 1,5 |
| Notebook Jupyter / Colab | Código executado, funcional; Markdown com achados, pontos fortes e limitações | 3,0 |
| Estrutura do README | Introdução clara; **link funcional** para o notebook; **link** do vídeo no YouTube | 2,0 |
| Vídeo demonstrativo | Até 5 min; demonstra o entregável; YouTube **não listado**; link no README | 2,0 |
| Organização geral | Estrutura do repo; nomes corretos; notebook legível | 1,5 |

**Detalhes adicionais**

- **Notebook:** código otimizado, executando corretamente; Markdown com resultados, conclusões e limitações.
- **README:** guiar ao notebook; **não duplicar** todo o conteúdo do Jupyter.
- **Vídeo:** breve, claro, focado na solução; link no README.
- **Pontualidade:** entrega no prazo e sem commits extras ajudam nota máxima.

**Faixas de avaliação**

| Faixa | Significado |
|-------|-------------|
| 9,0 – 10,0 | Excelência: critérios atendidos, código funcional, organização forte, comparações bem fechadas, vídeo claro |
| 7,0 – 8,9 | Entrega completa com pequenas falhas de organização ou execução |
| 5,0 – 6,9 | Entrega com falhas relevantes (ex.: código não funcional ou documentação incompleta) |
| 0,0 – 4,9 | Não atende requisitos mínimos ou está fora do prazo |
