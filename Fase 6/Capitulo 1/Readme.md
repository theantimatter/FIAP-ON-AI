# FarmTech Solutions — Visão computacional (Fase 6)

**FIAP — Graduação em Inteligência Artificial | Fase 6 | PBL**

## Nome do grupo

FarmTech Solutions — Fase 6 (Entregas 1 e 2)

## Integrantes

- Diego Filipe Pereira de Araujo — RM567064

## Professores

- **Tutor(a):** Sabrina Otoni
- **Coordenador(a):** Andre Godoi Chiovato

---

## Descrição

Projeto **FarmTech Solutions** em visão computacional: **Entrega 1** com YOLO (dataset em `assets/dataset_yolo_farmtech`, Make Sense IA, treino 30 e 60 épocas, validação e teste) e **Entrega 2** comparando **YOLO da E1**, **YOLO pré-treinada (COCO)** e **CNN simples do zero**.

---

## Notebooks

| Entrega | Arquivo no repositório                                                                                                               | Google Colab                                                                                              |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **1**   | [src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6.ipynb](src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6.ipynb)                   | [Abrir no Colab](https://colab.research.google.com/drive/10TWiqWN55SFTNgBIh50atKXMN3rVP3Gw?usp=sharing)   |
| **2**   | [src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6_entrega2.ipynb](src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6_entrega2.ipynb) | [Abrir no Colab](https://colab.research.google.com/drive/1lFFpfhOYb88yqfQx30W2wETNjt9kpI7R?usp=sharing) |

**Execução recomendada:** **Google Colab** (GPU: _Runtime → Change runtime type → GPU_). Os links da coluna **Google Colab** abrem cada notebook já hospedado no Google Drive (Entrega 1 e Entrega 2).

---

## Como executar (Google Colab)

1. **GPU (opcional mas recomendado para treino):** _Runtime → Change runtime type → GPU (T4)_.
2. **Dataset:** compacte a pasta **`dataset_yolo_farmtech`** do seu repositório local em **`dataset_yolo_farmtech.zip`** (a raiz do zip deve conter a pasta `dataset_yolo_farmtech/` com `train`, `valid`, `test`). Envie o arquivo para **`/content/farmtech/`** no Colab (menu **Arquivos**).
3. Rode as células **de cima para baixo**. O notebook define **`PROJECT = /content/farmtech`**, descompacta o zip se existir, clona **`yolov5`** e instala dependências com `pip`.
4. **Alternativa:** deixe o projeto no **Google Drive**, edite na primeira célula de código `USE_GOOGLE_DRIVE = True` e **`DRIVE_PROJECT`** apontando para a pasta **Capítulo 1** (que contém `assets/dataset_yolo_farmtech`).

### Entrega 2

- Na **raiz do Capítulo 1** precisam existir **`runs/`** (treinos/detect) e **`data_fase6.yaml`** gerados na E1 (`runs/train/fase6_ep60/weights/best.pt`, etc.). No Colab: mesma sessão após a E1 **ou** enviar **`runs`** e **`data_fase6.yaml`** para **`/content/farmtech/`** (`PROJECT`).

---

## Estrutura de pastas (repositório local)

```
Fase 6/Capitulo 1/
├── Readme.md
├── data_fase6.yaml           # dataset YOLO (raiz do projeto)
├── runs/                     # treino YOLO + detect (raiz; opcional no Git)
├── requirements.txt
├── scripts/
├── assets/
└── src/
    ├── DiegoFilipePereiradeAraujo_rm567064_pbl_fase6.ipynb
    └── DiegoFilipePereiradeAraujo_rm567064_pbl_fase6_entrega2.ipynb
```

No Colab, o clone **`yolov5/`** fica em **`/content/farmtech/`**; **`runs/`** e **`data_fase6.yaml`** ficam na raiz **`PROJECT`** (mesmo nível que `yolov5/`).

---

## Vídeo (YouTube — não listado)

- [Demonstração do projeto (Fase 6)](https://youtu.be/lEjT5GtKMig)

---

## Checklist alinhado ao enunciado (`Fase 6/atividade.md`)

**E1:** 80 imagens e split; Make Sense; notebook com treino/val/teste; duas épocas (30 e 60); conclusões; prints; vídeo + README com link do notebook.

**E2:** três abordagens; comparação nos quatro critérios; Markdown crítico + saídas.

---

## Referências

- [YOLOv5](https://github.com/ultralytics/yolov5)
- [Make Sense IA](https://www.makesense.ai/)
- [Google Colab](https://colab.research.google.com/)
- [Notebook no Git (FIAP)](https://www.youtube.com/watch?v=5ZYRqca7OVc)
