import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

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

def criar_features(dados):
    X = dados[['umidade', 'ph', 'nitrogenio', 'fosforo', 'potassio']].copy()
    
    X['ph_distancia_ideal'] = abs(X['ph'] - 7.0)
    X['umidade_quadrado'] = X['umidade'] ** 2
    X['total_nutrientes'] = X['nitrogenio'] + X['fosforo'] + X['potassio']
    X['umidade_ph'] = X['umidade'] * X['ph']
    
    return X

def treinar_modelo(dados):
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
    
    metricas = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R²': r2
    }
    
    print("=" * 50)
    print("MÉTRICAS DO MODELO")
    print("=" * 50)
    print(f"MAE (Erro Médio Absoluto): {mae:.2f} kg/hectare")
    print(f"MSE (Erro Quadrático Médio): {mse:.2f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse:.2f} kg/hectare")
    print(f"R² (Coeficiente de Determinação): {r2:.4f}")
    print(f"\nFeatures utilizadas: {list(X.columns)}")
    print("=" * 50)
    
    return modelo, X_test, y_test, y_pred, metricas

def main():
    print("Iniciando pipeline de Machine Learning...")
    print("Gerando dados agrícolas simulados...")
    
    dados = gerar_dados_agricolas(n_samples=200)
    
    dados.to_csv('dados_agricolas.csv', index=False)
    print(f"Dados salvos em 'dados_agricolas.csv' ({len(dados)} amostras)")
    
    print("\nTreinando modelo de regressão...")
    modelo, X_test, y_test, y_pred, metricas = treinar_modelo(dados)
    
    os.makedirs('modelos', exist_ok=True)
    modelo_path = 'modelos/modelo_regressao.pkl'
    joblib.dump(modelo, modelo_path)
    print(f"\nModelo salvo em '{modelo_path}'")
    
    metricas_df = pd.DataFrame([metricas])
    metricas_df.to_csv('metricas_modelo.csv', index=False)
    print("Métricas salvas em 'metricas_modelo.csv'")
    
    print("\nPipeline concluído com sucesso!")
    return modelo, dados, metricas

if __name__ == "__main__":
    modelo, dados, metricas = main()
