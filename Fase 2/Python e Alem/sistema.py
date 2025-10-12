import oracledb
import pandas as pd

oracledb.defaults.fetch_lobs = False

TIPOS_COLHEITA = ("manual", "mecanica")
PERCENTUAIS_PERDA = (5, 15)

colheitas = []

def validar_numero(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("Digite um numero positivo")
                continue
            return valor
        except:
            print("Digite um numero valido")

def validar_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("Digite um texto valido")
            continue
        return texto

def validar_tipo_colheita():
    while True:
        tipo = input("Tipo de colheita (manual ou mecanica): ").lower().strip()
        if tipo in TIPOS_COLHEITA:
            return tipo
        print("Digite manual ou mecanica")

def calcular_perda(tipo, toneladas):
    if tipo == TIPOS_COLHEITA[0]:
        percentual = PERCENTUAIS_PERDA[0]
    else:
        percentual = PERCENTUAIS_PERDA[1]
    perda = (toneladas * percentual) / 100
    return perda, percentual

def calcular_prejuizo(perda, preco):
    prejuizo = perda * preco
    return prejuizo

def cadastrar_colheita():
    print("\n=== CADASTRAR COLHEITA ===")

    propriedade = validar_texto("Nome da propriedade: ")
    data = validar_texto("Data da colheita (dd/mm/aaaa): ")
    tipo = validar_tipo_colheita()
    toneladas = validar_numero("Toneladas colhidas: ")
    preco = validar_numero("Preco por tonelada (R$): ")

    perda, percentual = calcular_perda(tipo, toneladas)
    prejuizo = calcular_prejuizo(perda, preco)

    colheita = {
        "propriedade": propriedade,
        "data": data,
        "tipo": tipo,
        "toneladas": toneladas,
        "preco": preco,
        "perda": perda,
        "percentual": percentual,
        "prejuizo": prejuizo
    }

    colheitas.append(colheita)

    print("\nColheita cadastrada!")
    print(f"Perda estimada: {perda:.2f} toneladas ({percentual}%)")
    print(f"Prejuizo estimado: R$ {prejuizo:.2f}")

def listar_colheitas():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    print("\n=== LISTA DE COLHEITAS ===")
    print(f"Total: {len(colheitas)} colheitas cadastradas")
    print("=" * 60)

    for i in range(len(colheitas)):
        c = colheitas[i]
        print(f"\nColheita #{i+1}")
        print(f"  Propriedade: {c['propriedade']}")
        print(f"  Data: {c['data']}")
        print(f"  Tipo: {c['tipo']}")
        print(f"  Toneladas colhidas: {c['toneladas']:.2f}")
        print(f"  Perda: {c['perda']:.2f} toneladas ({c['percentual']}%)")
        print(f"  Prejuizo: R$ {c['prejuizo']:.2f}")
        print("-" * 60)

def relatorio_total():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    total_toneladas = 0
    total_perda = 0
    total_prejuizo = 0
    maior_perda = 0
    menor_perda = None

    for c in colheitas:
        total_toneladas = total_toneladas + c["toneladas"]
        total_perda = total_perda + c["perda"]
        total_prejuizo = total_prejuizo + c["prejuizo"]

        if c["perda"] > maior_perda:
            maior_perda = c["perda"]
        if menor_perda == None or c["perda"] < menor_perda:
            menor_perda = c["perda"]

    media_perda = total_perda / len(colheitas)
    media_prejuizo = total_prejuizo / len(colheitas)
    percentual_perda_medio = media_perda / (total_toneladas / len(colheitas)) * 100

    print("\n=== RELATORIO TOTAL ===")
    print(f"Total de colheitas: {len(colheitas)}")
    print(f"Total colhido: {total_toneladas:.2f} toneladas")
    print(f"Total de perdas: {total_perda:.2f} toneladas")
    print(f"Total de prejuizo: R$ {total_prejuizo:.2f}")
    print("")
    print("=== MEDIAS ===")
    print(f"Perda media por colheita: {media_perda:.2f} toneladas")
    print(f"Prejuizo medio por colheita: R$ {media_prejuizo:.2f}")
    print(f"Percentual medio de perda: {percentual_perda_medio:.2f}%")
    print("")
    print("=== EXTREMOS ===")
    print(f"Maior perda: {maior_perda:.2f} toneladas")
    print(f"Menor perda: {menor_perda:.2f} toneladas")

def gerar_relatorio_txt():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    arquivo = None
    try:
        from datetime import datetime

        linhas = [
            "=" * 60,
            "RELATORIO DE COLHEITA DE CANA-DE-ACUCAR",
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "=" * 60,
            ""
        ]

        total_toneladas = 0
        total_perda = 0
        total_prejuizo = 0
        manuais = 0
        mecanicas = 0

        for i in range(len(colheitas)):
            c = colheitas[i]
            linhas.extend([
                f"Colheita {i+1}:",
                f"  Propriedade: {c['propriedade']}",
                f"  Data: {c['data']}",
                f"  Tipo: {c['tipo']}",
                f"  Toneladas colhidas: {c['toneladas']:.2f}",
                f"  Perda: {c['perda']:.2f} toneladas ({c['percentual']}%)",
                f"  Prejuizo: R$ {c['prejuizo']:.2f}",
                "-" * 60
            ])

            total_toneladas = total_toneladas + c["toneladas"]
            total_perda = total_perda + c["perda"]
            total_prejuizo = total_prejuizo + c["prejuizo"]

            if c["tipo"] == "manual":
                manuais = manuais + 1
            else:
                mecanicas = mecanicas + 1

        media_perda = total_perda / len(colheitas)
        percentual_medio = media_perda / (total_toneladas / len(colheitas)) * 100

        linhas.extend([
            "",
            "=" * 60,
            "TOTAIS:",
            f"  Total de colheitas: {len(colheitas)}",
            f"  Colheitas manuais: {manuais}",
            f"  Colheitas mecanicas: {mecanicas}",
            f"  Total colhido: {total_toneladas:.2f} toneladas",
            f"  Total de perdas: {total_perda:.2f} toneladas",
            f"  Total de prejuizo: R$ {total_prejuizo:.2f}",
            "=" * 60,
            ""
        ])

        linhas.extend([
            "ANALISE RESUMIDA:",
            f"  Perda media: {media_perda:.2f} toneladas por colheita",
            f"  Percentual medio de perda: {percentual_medio:.2f}%",
            f"  Prejuizo medio: R$ {total_prejuizo / len(colheitas):.2f} por colheita",
            "=" * 60,
            ""
        ])

        conclusao = ["CONCLUSAO:"]
        if percentual_medio > 10:
            conclusao.extend([
                "  As perdas estao acima da media esperada.",
                "  Recomenda-se revisar os processos de colheita."
            ])
        else:
            conclusao.extend([
                "  As perdas estao dentro da media esperada.",
                "  Continue monitorando para manter a eficiencia."
            ])
        conclusao.append("=" * 60)
        linhas.extend(conclusao)

        conteudo = "\n".join(linhas)

        arquivo = open("relatorio.txt", "w")
        arquivo.write(conteudo)

        print("\nRelatorio salvo em relatorio.txt")
    except Exception as e:
        print(f"\nErro ao gerar relatorio: {e}")
    finally:
        if arquivo != None:
            arquivo.close()

def exibir_tabela_memoria():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    tabela = []

    cabecalho = ["Propriedade", "Data", "Tipo", "Toneladas", "Perda", "Prejuizo"]
    tabela.append(cabecalho)

    total_toneladas = 0
    total_perda = 0
    total_prejuizo = 0

    for c in colheitas:
        linha = [
            c["propriedade"],
            c["data"],
            c["tipo"],
            c["toneladas"],
            c["perda"],
            c["prejuizo"]
        ]
        tabela.append(linha)

        total_toneladas = total_toneladas + c["toneladas"]
        total_perda = total_perda + c["perda"]
        total_prejuizo = total_prejuizo + c["prejuizo"]

    print("\n=== TABELA DE MEMORIA ===")
    print(f"{tabela[0][0]:20} {tabela[0][1]:12} {tabela[0][2]:10} {tabela[0][3]:>12} {tabela[0][4]:>12} {tabela[0][5]:>14}")
    print("=" * 90)

    for i in range(1, len(tabela)):
        print(f"{tabela[i][0]:20} {tabela[i][1]:12} {tabela[i][2]:10} {tabela[i][3]:>12.2f} {tabela[i][4]:>12.2f} {tabela[i][5]:>14.2f}")

    print("=" * 90)
    print(f"{'TOTAIS':20} {' ':12} {' ':10} {total_toneladas:>12.2f} {total_perda:>12.2f} {total_prejuizo:>14.2f}")
    print("=" * 90)

def salvar_arquivo():
    arquivo = None
    try:
        df = pd.DataFrame(colheitas)
        df.to_json("colheitas.json", orient="records", indent=4)
        df.to_csv("colheitas.csv", index=False)
        print("\nDados salvos em colheitas.json e colheitas.csv")
    except Exception as e:
        print(f"\nErro ao salvar arquivo: {e}")
    finally:
        if arquivo != None:
            arquivo.close()

def carregar_arquivo():
    try:
        df = pd.read_json("colheitas.json")
        dados = df.to_dict("records")

        colheitas.clear()
        for d in dados:
            colheitas.append(d)

        print(f"\n{len(dados)} colheitas carregadas do arquivo")
    except FileNotFoundError:
        print("\nNenhum arquivo anterior encontrado")
    except Exception as e:
        print(f"\nErro ao carregar arquivo: {e}")

def conectar_banco():
    try:
        usuario = input("Usuario do banco: ")
        senha = input("Senha do banco: ")
        host = "oracle.fiap.com.br:1521/orcl"

        conexao = oracledb.connect(user=usuario, password=senha, dsn=host)
        print("\nConexao com banco realizada!")
        return conexao
    except Exception as e:
        print(f"\nErro ao conectar no banco: {e}")
        return None

def salvar_banco(conexao):
    if conexao == None:
        print("\nConexao nao estabelecida")
        return

    cursor = None
    try:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE colheitas (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                propriedade VARCHAR2(100),
                data VARCHAR2(20),
                tipo VARCHAR2(20),
                toneladas NUMBER,
                perda NUMBER,
                prejuizo NUMBER
            )
        """)
        print("\nTabela criada")
    except Exception as e:
        print("\nTabela ja existe")
    finally:
        if cursor != None:
            cursor.close()

    cursor = None
    try:
        cursor = conexao.cursor()

        for c in colheitas:
            cursor.execute("""
                INSERT INTO colheitas (propriedade, data, tipo, toneladas, perda, prejuizo)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (c["propriedade"], c["data"], c["tipo"],
                  c["toneladas"], c["perda"], c["prejuizo"]))

        conexao.commit()
        print(f"\n{len(colheitas)} colheitas salvas no banco")
    except Exception as e:
        print(f"\nErro ao salvar no banco: {e}")
        conexao.rollback()
    finally:
        if cursor != None:
            cursor.close()

def comparar_tipos_colheita():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    manuais = []
    mecanicas = []

    for c in colheitas:
        if c["tipo"] == "manual":
            manuais.append(c)
        else:
            mecanicas.append(c)

    print("\n=== COMPARACAO ENTRE TIPOS DE COLHEITA ===")

    if len(manuais) > 0:
        total_perda_manual = 0
        total_prejuizo_manual = 0
        for c in manuais:
            total_perda_manual = total_perda_manual + c["perda"]
            total_prejuizo_manual = total_prejuizo_manual + c["prejuizo"]
        media_perda_manual = total_perda_manual / len(manuais)
        media_prejuizo_manual = total_prejuizo_manual / len(manuais)

        print(f"\nColheita Manual ({len(manuais)} colheitas):")
        print(f"  Perda media: {media_perda_manual:.2f} toneladas")
        print(f"  Prejuizo medio: R$ {media_prejuizo_manual:.2f}")
    else:
        print("\nNenhuma colheita manual cadastrada")

    if len(mecanicas) > 0:
        total_perda_mecanica = 0
        total_prejuizo_mecanica = 0
        for c in mecanicas:
            total_perda_mecanica = total_perda_mecanica + c["perda"]
            total_prejuizo_mecanica = total_prejuizo_mecanica + c["prejuizo"]
        media_perda_mecanica = total_perda_mecanica / len(mecanicas)
        media_prejuizo_mecanica = total_prejuizo_mecanica / len(mecanicas)

        print(f"\nColheita Mecanica ({len(mecanicas)} colheitas):")
        print(f"  Perda media: {media_perda_mecanica:.2f} toneladas")
        print(f"  Prejuizo medio: R$ {media_prejuizo_mecanica:.2f}")
    else:
        print("\nNenhuma colheita mecanica cadastrada")

    if len(manuais) > 0 and len(mecanicas) > 0:
        print("\n=== RECOMENDACAO ===")
        if media_perda_manual < media_perda_mecanica:
            diferenca = media_perda_mecanica - media_perda_manual
            print(f"Colheita manual tem {diferenca:.2f} toneladas menos de perda em media")
            print("Recomendacao: Considere aumentar o uso de colheita manual")
        else:
            print("Colheita mecanica esta com desempenho similar ou melhor")

def calcular_economia_potencial():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    mecanicas = []
    for c in colheitas:
        if c["tipo"] == "mecanica":
            mecanicas.append(c)

    if len(mecanicas) == 0:
        print("\nNenhuma colheita mecanica para calcular economia")
        return

    print("\n=== ECONOMIA POTENCIAL ===")
    print("Simulacao: E se todas as colheitas mecanicas fossem manuais?")
    print("")

    economia_toneladas = 0
    economia_dinheiro = 0

    for c in mecanicas:
        perda_mecanica = c["perda"]
        perda_manual_seria = (c["toneladas"] * 5) / 100
        diferenca_toneladas = perda_mecanica - perda_manual_seria
        diferenca_dinheiro = diferenca_toneladas * c["preco"]

        economia_toneladas = economia_toneladas + diferenca_toneladas
        economia_dinheiro = economia_dinheiro + diferenca_dinheiro

    print(f"Total de colheitas mecanicas: {len(mecanicas)}")
    print(f"Economia potencial em toneladas: {economia_toneladas:.2f}")
    print(f"Economia potencial em dinheiro: R$ {economia_dinheiro:.2f}")
    print("")
    print("Nota: Considere o custo adicional de mao de obra manual")

def estatisticas_propriedades():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    propriedades = {}

    for c in colheitas:
        nome = c["propriedade"]
        if nome not in propriedades:
            propriedades[nome] = {
                "toneladas": 0,
                "perda": 0,
                "prejuizo": 0,
                "quantidade": 0
            }
        propriedades[nome]["toneladas"] = propriedades[nome]["toneladas"] + c["toneladas"]
        propriedades[nome]["perda"] = propriedades[nome]["perda"] + c["perda"]
        propriedades[nome]["prejuizo"] = propriedades[nome]["prejuizo"] + c["prejuizo"]
        propriedades[nome]["quantidade"] = propriedades[nome]["quantidade"] + 1

    print("\n=== ESTATISTICAS POR PROPRIEDADE ===")
    print("")

    for nome in propriedades:
        p = propriedades[nome]
        media_perda = p["perda"] / p["quantidade"]
        print(f"Propriedade: {nome}")
        print(f"  Colheitas: {p['quantidade']}")
        print(f"  Total colhido: {p['toneladas']:.2f} toneladas")
        print(f"  Total de perdas: {p['perda']:.2f} toneladas")
        print(f"  Perda media: {media_perda:.2f} toneladas")
        print(f"  Prejuizo total: R$ {p['prejuizo']:.2f}")
        print("")

    menor_perda = None
    menor_perda_nome = ""
    maior_perda = None
    maior_perda_nome = ""

    for nome in propriedades:
        p = propriedades[nome]
        media_perda = p["perda"] / p["quantidade"]

        if menor_perda == None or media_perda < menor_perda:
            menor_perda = media_perda
            menor_perda_nome = nome

        if maior_perda == None or media_perda > maior_perda:
            maior_perda = media_perda
            maior_perda_nome = nome

    print("=== RANKING ===")
    print(f"Melhor desempenho: {menor_perda_nome} ({menor_perda:.2f} ton de perda media)")
    print(f"Precisa melhorar: {maior_perda_nome} ({maior_perda:.2f} ton de perda media)")

def analise_pandas():
    if len(colheitas) == 0:
        print("\nNenhuma colheita cadastrada")
        return

    df = pd.DataFrame(colheitas)

    print("\n=== ANALISE ESTATISTICA COMPLETA ===")
    print("")
    print("Estatisticas Descritivas:")
    print("")
    print(df[['toneladas', 'perda', 'prejuizo']].describe())
    print("")
    print("=== AGRUPAMENTO POR TIPO DE COLHEITA ===")
    print("")
    print(df.groupby('tipo')[['toneladas', 'perda', 'prejuizo']].agg(['mean', 'sum', 'count']))
    print("")
    print("=== AGRUPAMENTO POR PROPRIEDADE ===")
    print("")
    print(df.groupby('propriedade')[['toneladas', 'perda', 'prejuizo']].sum())

def menu():
    print("\n" + "=" * 60)
    print("SISTEMA DE CONTROLE DE COLHEITA DE CANA-DE-ACUCAR")
    print("=" * 60)
    print("\nCADASTRO E CONSULTA:")
    print("  1. Cadastrar colheita")
    print("  2. Listar colheitas")
    print("  3. Relatorio total")
    print("  7. Ver tabela de memoria")
    print("\nANALISES E COMPARACOES:")
    print("  10. Comparar tipos de colheita")
    print("  11. Calcular economia potencial")
    print("  12. Estatisticas por propriedade")
    print("  13. Analise completa com pandas")
    print("\nPERSISTENCIA DE DADOS:")
    print("  4. Salvar em arquivo JSON/CSV")
    print("  5. Carregar arquivo JSON")
    print("  6. Gerar relatorio em TXT")
    print("  8. Conectar banco Oracle")
    print("  9. Salvar no banco")
    print("\n  0. Sair")
    print("=" * 60)

    opcao = input("\nEscolha uma opcao: ")
    return opcao

conexao_banco = None

carregar_arquivo()

while True:
    opcao = menu()

    if opcao == "1":
        cadastrar_colheita()
    elif opcao == "2":
        listar_colheitas()
    elif opcao == "3":
        relatorio_total()
    elif opcao == "4":
        salvar_arquivo()
    elif opcao == "5":
        carregar_arquivo()
    elif opcao == "6":
        gerar_relatorio_txt()
    elif opcao == "7":
        exibir_tabela_memoria()
    elif opcao == "8":
        conexao_banco = conectar_banco()
    elif opcao == "9":
        salvar_banco(conexao_banco)
    elif opcao == "10":
        comparar_tipos_colheita()
    elif opcao == "11":
        calcular_economia_potencial()
    elif opcao == "12":
        estatisticas_propriedades()
    elif opcao == "13":
        analise_pandas()
    elif opcao == "0":
        print("\nSaindo do sistema...")
        break
    else:
        print("\nOpcao invalida")
