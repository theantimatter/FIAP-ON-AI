import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from utils import criar_features, criar_features_umidade_ph, criar_features_irrigacao, criar_features_fertilizacao
from banco_dados import criar_banco_dados, popular_banco_com_dados_existentes

def gerar_dados_agricolas(n_samples=200):
    np.random.seed(42)
    
    umidade = np.random.uniform(30, 90, n_samples)
    ph = np.random.uniform(5.5, 8.5, n_samples)
    nitrogenio = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    fosforo = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    potassio = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    
    rendimento_base = 1500
    
    umidade_otima = 60
    fator_umidade_linear = 10 * umidade
    fator_umidade_quadratico = -0.1 * (umidade - umidade_otima) ** 2
    contribuicao_umidade = fator_umidade_linear + fator_umidade_quadratico
    
    ph_otimo = 7.0
    contribuicao_ph = 200 * ph - 15 * (ph - ph_otimo) ** 2
    
    contribuicao_npk = (
        nitrogenio * 300 +
        fosforo * 250 +
        potassio * 200
    )
    
    rendimento = (
        rendimento_base +
        contribuicao_umidade +
        contribuicao_ph +
        contribuicao_npk +
        np.random.normal(0, 150, n_samples)
    )
    
    rendimento = np.clip(rendimento, 800, 4000)
    
    dados = pd.DataFrame({
        'umidade': umidade,
        'ph': ph,
        'nitrogenio': nitrogenio,
        'fosforo': fosforo,
        'potassio': potassio,
        'rendimento': rendimento
    })
    
    return dados

def calcular_volume_irrigacao(dados):
    umidade_ideal = 60
    umidade_atual = dados["umidade"]
    
    volume_base = 100
    diferenca_umidade = umidade_ideal - umidade_atual
    volume_irrigacao = volume_base + (diferenca_umidade * 2)
    volume_irrigacao = np.clip(volume_irrigacao, 0, 300)
    
    dados["volume_irrigacao"] = volume_irrigacao
    return dados

def calcular_necessidade_fertilizacao(dados):
    necessidade = []
    
    for idx, row in dados.iterrows():
        score = 0
        
        if row["nitrogenio"] == 0:
            score += 3
        if row["fosforo"] == 0:
            score += 2
        if row["potassio"] == 0:
            score += 2
        
        ph_dist = abs(row["ph"] - 7.0)
        if ph_dist > 1.0:
            score += 2
        
        if row["umidade"] < 40:
            score += 1
        
        necessidade.append(min(score, 10))
    
    dados["necessidade_fertilizacao"] = necessidade
    return dados

def treinar_modelo_rendimento(dados):
    X = criar_features(dados)
    y = dados['rendimento']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {"MAE": mae, "MSE": mse, "RMSE": rmse, "R²": r2}
    
    print("=" * 50)
    print("MÉTRICAS - MODELO DE RENDIMENTO")
    print("=" * 50)
    print(f"MAE: {mae:.2f} kg/hectare")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f} kg/hectare")
    print(f"R²: {r2:.4f}")
    print("=" * 50)
    
    return modelo, metricas

def treinar_modelo_umidade(dados):
    X = criar_features_umidade_ph(dados)
    y = dados['umidade']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_pred = np.clip(y_pred, 0, 100)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {"MAE": mae, "MSE": mse, "RMSE": rmse, "R²": r2}
    
    print("=" * 50)
    print("MÉTRICAS - MODELO DE UMIDADE")
    print("=" * 50)
    print(f"MAE: {mae:.2f}%")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}%")
    print(f"R²: {r2:.4f}")
    print("=" * 50)
    
    return modelo, metricas

def treinar_modelo_ph(dados):
    X = criar_features_umidade_ph(dados)
    y = dados['ph']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_pred = np.clip(y_pred, 0, 14)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {"MAE": mae, "MSE": mse, "RMSE": rmse, "R²": r2}
    
    print("=" * 50)
    print("MÉTRICAS - MODELO DE pH")
    print("=" * 50)
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.4f}")
    print("=" * 50)
    
    return modelo, metricas

def treinar_modelo_irrigacao(dados):
    X = criar_features_irrigacao(dados)
    y = dados["volume_irrigacao"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {"MAE": mae, "MSE": mse, "RMSE": rmse, "R²": r2}
    
    print("=" * 50)
    print("MÉTRICAS - MODELO DE IRRIGAÇÃO")
    print("=" * 50)
    print(f"MAE: {mae:.2f} litros/hectare")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f} litros/hectare")
    print(f"R²: {r2:.4f}")
    print("=" * 50)
    
    return modelo, metricas

def treinar_modelo_fertilizacao(dados):
    X = criar_features_fertilizacao(dados)
    y = dados["necessidade_fertilizacao"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_pred = np.clip(y_pred, 0, 10)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {"MAE": mae, "MSE": mse, "RMSE": rmse, "R²": r2}
    
    print("=" * 50)
    print("MÉTRICAS - MODELO DE FERTILIZAÇÃO")
    print("=" * 50)
    print(f"MAE: {mae:.2f} pontos")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f} pontos")
    print(f"R²: {r2:.4f}")
    print("=" * 50)
    
    return modelo, metricas

def main():
    print("=" * 60)
    print("FARMTECH SOLUTIONS - PIPELINE COMPLETO DE MACHINE LEARNING")
    print("=" * 60)
    
    print("\n1. Gerando dados agrícolas simulados...")
    dados = gerar_dados_agricolas(n_samples=200)
    
    os.makedirs('dados', exist_ok=True)
    dados.to_csv('dados/dados_agricolas.csv', index=False)
    print(f"   Dados salvos em 'dados/dados_agricolas.csv' ({len(dados)} amostras)")
    
    print("\n2. Criando banco de dados...")
    criar_banco_dados()
    popular_banco_com_dados_existentes()
    print("   Banco de dados criado")
    
    print("\n3. Treinando modelos de previsão...")
    print("   3.1. Modelo de Rendimento...")
    modelo_rendimento, metricas_rendimento = treinar_modelo_rendimento(dados)
    
    print("   3.2. Modelo de Umidade...")
    modelo_umidade, metricas_umidade = treinar_modelo_umidade(dados)
    
    print("   3.3. Modelo de pH...")
    modelo_ph, metricas_ph = treinar_modelo_ph(dados)
    
    os.makedirs('modelos', exist_ok=True)
    joblib.dump(modelo_rendimento, 'modelos/modelo_rendimento.pkl')
    joblib.dump(modelo_umidade, 'modelos/modelo_umidade.pkl')
    joblib.dump(modelo_ph, 'modelos/modelo_ph.pkl')
    print("   Modelos de previsão salvos")
    
    print("\n4. Calculando ações agrícolas...")
    print("   4.1. Volume de irrigação...")
    dados = calcular_volume_irrigacao(dados)
    
    print("   4.2. Necessidade de fertilização...")
    dados = calcular_necessidade_fertilizacao(dados)
    
    dados.to_csv('dados/dados_com_acoes.csv', index=False)
    print("   Dados com ações salvos")
    
    print("\n5. Treinando modelos de ações...")
    print("   5.1. Modelo de Irrigação...")
    modelo_irrigacao, metricas_irrigacao = treinar_modelo_irrigacao(dados)
    
    print("   5.2. Modelo de Fertilização...")
    modelo_fertilizacao, metricas_fertilizacao = treinar_modelo_fertilizacao(dados)
    
    joblib.dump(modelo_irrigacao, 'modelos/modelo_irrigacao.pkl')
    joblib.dump(modelo_fertilizacao, 'modelos/modelo_fertilizacao.pkl')
    print("   Modelos de ações salvos")
    
    os.makedirs('metricas', exist_ok=True)
    
    metricas_previsao = pd.DataFrame({
        'Modelo': ['Rendimento', 'Umidade', 'pH'],
        'MAE': [metricas_rendimento['MAE'], metricas_umidade['MAE'], metricas_ph['MAE']],
        'MSE': [metricas_rendimento['MSE'], metricas_umidade['MSE'], metricas_ph['MSE']],
        'RMSE': [metricas_rendimento['RMSE'], metricas_umidade['RMSE'], metricas_ph['RMSE']],
        'R²': [metricas_rendimento['R²'], metricas_umidade['R²'], metricas_ph['R²']]
    })
    metricas_previsao.to_csv('metricas/metricas_previsao.csv', index=False)
    
    metricas_acoes = pd.DataFrame({
        'Modelo': ['Irrigação', 'Fertilização'],
        'MAE': [metricas_irrigacao['MAE'], metricas_fertilizacao['MAE']],
        'MSE': [metricas_irrigacao['MSE'], metricas_fertilizacao['MSE']],
        'RMSE': [metricas_irrigacao['RMSE'], metricas_fertilizacao['RMSE']],
        'R²': [metricas_irrigacao['R²'], metricas_fertilizacao['R²']]
    })
    metricas_acoes.to_csv('metricas/metricas_acoes.csv', index=False)
    print("   Métricas salvas")
    
    print("\n" + "=" * 60)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\nModelos treinados:")
    print("  - Rendimento")
    print("  - Umidade")
    print("  - pH")
    print("  - Irrigação")
    print("  - Fertilização")
    print("\nExecute 'streamlit run dashboard.py' para visualizar os resultados.")

if __name__ == "__main__":
    main()

