import sqlite3
import pandas as pd
import os
from datetime import datetime


def criar_banco_dados():
    os.makedirs("dados", exist_ok=True)
    conn = sqlite3.connect("dados/dados_sensores.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            umidade REAL,
            ph REAL,
            nitrogenio INTEGER,
            fosforo INTEGER,
            potassio INTEGER,
            rendimento REAL
        )
    """
    )

    conn.commit()
    conn.close()


def inserir_dados(dados):
    conn = sqlite3.connect("dados/dados_sensores.db")

    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dados.to_sql("sensores", conn, if_exists="append", index=False)

    conn.close()


def carregar_dados_banco():
    if not os.path.exists("dados/dados_sensores.db"):
        return None

    conn = sqlite3.connect("dados/dados_sensores.db")
    dados = pd.read_sql_query("SELECT * FROM sensores", conn)
    conn.close()

    return dados


def popular_banco_com_dados_existentes():
    if os.path.exists("dados/dados_agricolas.csv"):
        dados = pd.read_csv("dados/dados_agricolas.csv")

        criar_banco_dados()

        for idx, row in dados.iterrows():
            dados_linha = pd.DataFrame(
                [
                    {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "umidade": row["umidade"],
                        "ph": row["ph"],
                        "nitrogenio": row["nitrogenio"],
                        "fosforo": row["fosforo"],
                        "potassio": row["potassio"],
                        "rendimento": row["rendimento"],
                    }
                ]
            )

            inserir_dados(dados_linha)

        print(f"   Dados inseridos no banco: {len(dados)} registros")
    else:
        print("   AVISO: Arquivo dados_agricolas.csv não encontrado")
