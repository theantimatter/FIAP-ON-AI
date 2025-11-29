import pandas as pd
import numpy as np
import os

def criar_features(dados):
    X = dados[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    
    X["ph_distancia_ideal"] = abs(X["ph"] - 7.0)
    X["umidade_quadrado"] = X["umidade"] ** 2
    X["total_nutrientes"] = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["umidade_ph"] = X["umidade"] * X["ph"]
    
    return X

def criar_features_umidade_ph(dados, dados_completos=None):
    X = dados[["nitrogenio", "fosforo", "potassio", "rendimento"]].copy()
    
    X["total_nutrientes"] = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    
    if dados_completos is not None and len(dados_completos) > 0:
        rend_mean = dados_completos["rendimento"].mean()
        rend_std = dados_completos["rendimento"].std()
        if rend_std > 0:
            X["rendimento_normalizado"] = (X["rendimento"] - rend_mean) / rend_std
        else:
            X["rendimento_normalizado"] = 0
    else:
        X["rendimento_normalizado"] = 0
    
    return X

def criar_features_irrigacao(dados):
    X = dados[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    
    X["umidade_quadrado"] = X["umidade"] ** 2
    X["ph_distancia_ideal"] = abs(X["ph"] - 7.0)
    X["total_nutrientes"] = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["umidade_ph"] = X["umidade"] * X["ph"]
    
    return X

def criar_features_fertilizacao(dados):
    X = dados[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    
    X["ph_distancia_ideal"] = abs(X["ph"] - 7.0)
    X["faltam_nutrientes"] = (X["nitrogenio"] == 0).astype(int) + (X["fosforo"] == 0).astype(int) + (X["potassio"] == 0).astype(int)
    X["umidade_baixa"] = (X["umidade"] < 50).astype(int)
    X["ph_fora_faixa"] = ((X["ph"] < 6.0) | (X["ph"] > 8.0)).astype(int)
    
    return X

def carregar_dados():
    caminhos_possiveis = [
        "dados/dados_agricolas.csv",
        "dados_agricolas.csv"
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)
    
    return None

