import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="FarmTech Solutions - Dashboard Agrícola", page_icon="🌾", layout="wide"
)

st.title("🌾 FarmTech Solutions - Assistente Agrícola Inteligente")
st.markdown("---")


def carregar_modelo():
    modelo_path = "modelos/modelo_regressao.pkl"
    if os.path.exists(modelo_path):
        return joblib.load(modelo_path)
    else:
        st.error("Modelo não encontrado! Execute primeiro o script ml_pipeline.py")
        st.stop()


def carregar_dados():
    if os.path.exists("dados_agricolas.csv"):
        return pd.read_csv("dados_agricolas.csv")
    else:
        st.warning("Dados não encontrados. Usando dados de exemplo.")
        return None


def carregar_metricas():
    if os.path.exists("metricas_modelo.csv"):
        return pd.read_csv("metricas_modelo.csv")
    return None


def criar_features(dados):
    X = dados[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()

    X["ph_distancia_ideal"] = abs(X["ph"] - 7.0)
    X["umidade_quadrado"] = X["umidade"] ** 2
    X["total_nutrientes"] = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["umidade_ph"] = X["umidade"] * X["ph"]

    return X


modelo = carregar_modelo()
dados = carregar_dados()
metricas = carregar_metricas()

st.sidebar.title("📊 Navegação")
pagina = st.sidebar.radio(
    "Selecione uma seção:",
    [
        "🏠 Visão Geral",
        "📈 Métricas de Desempenho",
        "🔍 Análise de Correlação",
        "🔮 Previsões",
    ],
)

if pagina == "🏠 Visão Geral":
    st.header("Visão Geral do Sistema")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Amostras", len(dados) if dados is not None else "N/A")

    with col2:
        if dados is not None:
            rendimento_medio = dados["rendimento"].mean()
            st.metric("Rendimento Médio", f"{rendimento_medio:.0f} kg/hectare")
        else:
            st.metric("Rendimento Médio", "N/A")

    with col3:
        if dados is not None:
            umidade_media = dados["umidade"].mean()
            st.metric("Umidade Média", f"{umidade_media:.1f}%")
        else:
            st.metric("Umidade Média", "N/A")

    st.markdown("---")

    if dados is not None:
        st.subheader("📋 Resumo dos Dados")
        st.dataframe(dados.head(10), use_container_width=True)

        st.subheader("📊 Estatísticas Descritivas")
        st.dataframe(dados.describe(), use_container_width=True)
    else:
        st.info("Execute o script ml_pipeline.py para gerar os dados.")

elif pagina == "📈 Métricas de Desempenho":
    st.header("Métricas de Desempenho do Modelo")

    if metricas is not None:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("MAE", f"{metricas['MAE'].values[0]:.2f} kg/hectare")
            st.caption("Erro Médio Absoluto")

        with col2:
            st.metric("MSE", f"{metricas['MSE'].values[0]:.2f}")
            st.caption("Erro Quadrático Médio")

        with col3:
            st.metric("RMSE", f"{metricas['RMSE'].values[0]:.2f} kg/hectare")
            st.caption("Raiz do Erro Quadrático Médio")

        with col4:
            r2_value = metricas["R²"].values[0]
            st.metric("R²", f"{r2_value:.4f}")
            st.caption("Coeficiente de Determinação")

        st.markdown("---")

        st.subheader("📚 Interpretação das Métricas")

        st.markdown(
            """
        - **MAE (Mean Absolute Error)**: Média dos erros absolutos. Quanto menor, melhor.
        - **MSE (Mean Squared Error)**: Média dos erros ao quadrado. Penaliza erros grandes.
        - **RMSE (Root Mean Squared Error)**: Raiz quadrada do MSE. Mesma unidade da variável alvo.
        - **R² (Coeficiente de Determinação)**: Proporção da variância explicada. Varia de 0 a 1, sendo 1 o melhor.
        """
        )

        st.subheader("Qualidade do Modelo (R²)")

        r2_progress = max(0.0, min(1.0, float(r2_value)))
        st.progress(r2_progress)

        if r2_value < 0:
            st.warning(
                f"⚠️ R² negativo ({r2_value:.4f}): O modelo está com desempenho muito ruim, pior que uma linha horizontal na média. Considere revisar os dados ou o modelo."
            )
            st.caption(
                f"O modelo tem R² de {r2_value:.4f}, indicando que precisa ser melhorado."
            )
        elif r2_value < 0.5:
            st.info(
                f"ℹ️ R² baixo ({r2_value:.4f}): O modelo explica apenas {r2_value*100:.2f}% da variância. Considere melhorar o modelo."
            )
            st.caption(f"O modelo explica {r2_value*100:.2f}% da variância nos dados.")
        else:
            st.caption(f"O modelo explica {r2_value*100:.2f}% da variância nos dados.")

    else:
        st.warning(
            "Métricas não encontradas. Execute o script ml_pipeline.py primeiro."
        )

elif pagina == "🔍 Análise de Correlação":
    st.header("Análise de Correlação entre Variáveis")

    if dados is not None:
        variaveis = ["umidade", "ph", "nitrogenio", "fosforo", "potassio", "rendimento"]
        dados_corr = dados[variaveis]
        matriz_corr = dados_corr.corr()

        st.subheader("Mapa de Calor de Correlação")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            matriz_corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax,
        )
        plt.title("Matriz de Correlação entre Variáveis Agrícolas", fontsize=14, pad=20)
        st.pyplot(fig)

        st.markdown("---")

        st.subheader("Relação entre Variáveis e Rendimento")

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(dados["umidade"], dados["rendimento"], alpha=0.6)
            ax.set_xlabel("Umidade do Solo (%)")
            ax.set_ylabel("Rendimento (kg/hectare)")
            ax.set_title("Umidade vs Rendimento")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(dados["ph"], dados["rendimento"], alpha=0.6, color="orange")
            ax.set_xlabel("pH do Solo")
            ax.set_ylabel("Rendimento (kg/hectare)")
            ax.set_title("pH vs Rendimento")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        st.subheader("Impacto dos Nutrientes no Rendimento")
        nutrientes = ["nitrogenio", "fosforo", "potassio"]
        rendimento_com_nutriente = []
        rendimento_sem_nutriente = []

        for nutriente in nutrientes:
            com = dados[dados[nutriente] == 1]["rendimento"].mean()
            sem = dados[dados[nutriente] == 0]["rendimento"].mean()
            rendimento_com_nutriente.append(com)
            rendimento_sem_nutriente.append(sem)

        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(nutrientes))
        width = 0.35

        ax.bar(
            x - width / 2,
            rendimento_com_nutriente,
            width,
            label="Com Nutriente",
            color="green",
            alpha=0.7,
        )
        ax.bar(
            x + width / 2,
            rendimento_sem_nutriente,
            width,
            label="Sem Nutriente",
            color="red",
            alpha=0.7,
        )

        ax.set_xlabel("Nutrientes")
        ax.set_ylabel("Rendimento Médio (kg/hectare)")
        ax.set_title("Impacto dos Nutrientes NPK no Rendimento")
        ax.set_xticks(x)
        ax.set_xticklabels(["Nitrogênio (N)", "Fósforo (P)", "Potássio (K)"])
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        st.pyplot(fig)

    else:
        st.warning("Dados não encontrados. Execute o script ml_pipeline.py primeiro.")

elif pagina == "🔮 Previsões":
    st.header("Previsão de Rendimento em Tempo Real")

    st.markdown(
        """
    Preencha os valores abaixo para obter uma previsão do rendimento esperado
    baseada nas condições do solo e nutrientes disponíveis.
    """
    )

    col1, col2 = st.columns(2)

    with col1:
        umidade = st.slider(
            "Umidade do Solo (%)", min_value=0, max_value=100, value=60, step=1
        )

        ph = st.slider("pH do Solo", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

    with col2:
        st.subheader("Nutrientes Disponíveis")
        nitrogenio = st.checkbox("Nitrogênio (N) presente", value=True)
        fosforo = st.checkbox("Fósforo (P) presente", value=True)
        potassio = st.checkbox("Potássio (K) presente", value=True)

    n_val = 1 if nitrogenio else 0
    p_val = 1 if fosforo else 0
    k_val = 1 if potassio else 0

    dados_previsao_base = pd.DataFrame(
        {
            "umidade": [umidade],
            "ph": [ph],
            "nitrogenio": [n_val],
            "fosforo": [p_val],
            "potassio": [k_val],
        }
    )

    dados_previsao = criar_features(dados_previsao_base)

    if st.button("🔮 Calcular Previsão", type="primary"):
        previsao = modelo.predict(dados_previsao)[0]

        st.markdown("---")
        st.success(f"### Rendimento Previsto: {previsao:.0f} kg/hectare")

        st.subheader("📋 Valores de Entrada")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Umidade", f"{umidade}%")
        with col2:
            st.metric("pH", f"{ph:.1f}")
        with col3:
            st.metric("N", "✅" if nitrogenio else "❌")
        with col4:
            st.metric("P", "✅" if fosforo else "❌")
        with col5:
            st.metric("K", "✅" if potassio else "❌")

        st.markdown("---")
        st.subheader("💡 Recomendações")

        recomendacoes = []

        if umidade < 50:
            recomendacoes.append("⚠️ Umidade baixa. Considere irrigação.")
        elif umidade > 70:
            recomendacoes.append("⚠️ Umidade alta. Pode haver excesso de água.")
        else:
            recomendacoes.append("✅ Umidade em nível adequado.")

        if ph < 6.0 or ph > 8.0:
            recomendacoes.append(
                "⚠️ pH fora da faixa ideal (6.5-7.5). Considere correção."
            )
        else:
            recomendacoes.append("✅ pH em nível adequado.")

        if not nitrogenio:
            recomendacoes.append(
                "💡 Considere adicionar nitrogênio para melhorar o rendimento."
            )
        if not fosforo:
            recomendacoes.append(
                "💡 Considere adicionar fósforo para melhorar o rendimento."
            )
        if not potassio:
            recomendacoes.append(
                "💡 Considere adicionar potássio para melhorar o rendimento."
            )

        for rec in recomendacoes:
            st.markdown(f"- {rec}")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "FarmTech Solutions - Assistente Agrícola Inteligente | PARTE 1"
    "</div>",
    unsafe_allow_html=True,
)
