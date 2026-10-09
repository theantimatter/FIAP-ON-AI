"""
CardioIA - Fase 2 | Parte 1: extracao de sintomas e sugestao de diagnostico.

Le os relatos de dados/relatos_pacientes.txt, procura as expressoes do mapa de
conhecimento de dados/mapa_conhecimento.csv e sugere o diagnostico mais provavel
para cada relato. O resultado consolidado vai para saidas/diagnosticos_sugeridos.csv.
"""

import csv
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RELATOS = BASE / "dados" / "relatos_pacientes.txt"
MAPA = BASE / "dados" / "mapa_conhecimento.csv"
SAIDA = BASE / "saidas" / "diagnosticos_sugeridos.csv"


def normalizar(texto):
    decomposto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def carregar_mapa(caminho):
    expressoes = []
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            doenca = linha["doenca_associada"].strip()
            for coluna in ("sintoma_1", "sintoma_2"):
                sintoma = linha[coluna].strip()
                if sintoma:
                    expressoes.append((normalizar(sintoma), sintoma, doenca))
    expressoes.sort(key=lambda item: len(item[0]), reverse=True)
    return expressoes


def carregar_relatos(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo if linha.strip()]


def identificar_sintomas(relato, expressoes):
    texto = normalizar(relato)
    encontrados = []
    for chave, sintoma, doenca in expressoes:
        posicao = texto.find(chave)
        if posicao < 0:
            continue
        texto = texto[:posicao] + "\0" * len(chave) + texto[posicao + len(chave):]
        encontrados.append((sintoma, doenca))
    return encontrados


def sugerir_diagnostico(encontrados):
    if not encontrados:
        return "nao identificado", 0
    contagem = Counter(doenca for _, doenca in encontrados)
    maior = max(contagem.values())
    empatados = sorted(doenca for doenca, total in contagem.items() if total == maior)
    return " ou ".join(empatados), maior


def analisar(relatos, expressoes):
    resultados = []
    for numero, relato in enumerate(relatos, start=1):
        encontrados = identificar_sintomas(relato, expressoes)
        diagnostico, evidencias = sugerir_diagnostico(encontrados)
        resultados.append(
            {
                "paciente": "P{:02d}".format(numero),
                "relato": relato,
                "sintomas_identificados": "; ".join(s for s, _ in encontrados),
                "diagnostico_sugerido": diagnostico,
                "expressoes_de_apoio": evidencias,
            }
        )
    return resultados


def gravar(resultados, caminho):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    expressoes = carregar_mapa(MAPA)
    relatos = carregar_relatos(RELATOS)

    print("Mapa de conhecimento: {} expressoes".format(len(expressoes)))
    print("Relatos lidos: {}\n".format(len(relatos)))

    resultados = analisar(relatos, expressoes)
    for item in resultados:
        print("[{}] {}".format(item["paciente"], item["relato"]))
        print("  Sintomas  : {}".format(item["sintomas_identificados"] or "nenhum"))
        print(
            "  Diagnostico: {} ({} expressoes de apoio)\n".format(
                item["diagnostico_sugerido"], item["expressoes_de_apoio"]
            )
        )

    sem_diagnostico = sum(1 for i in resultados if i["expressoes_de_apoio"] == 0)
    print("Relatos com diagnostico sugerido: {}/{}".format(len(resultados) - sem_diagnostico, len(resultados)))

    gravar(resultados, SAIDA)
    print("Arquivo gravado: {}".format(SAIDA))


if __name__ == "__main__":
    main()
