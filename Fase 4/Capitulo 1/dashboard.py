import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import criar_features, criar_features_umidade_ph, criar_features_irrigacao, criar_features_fertilizacao

st.set_page_config(
    page_title="FarmTech Solutions - Dashboard", page_icon=None, layout="wide"
)

st.title("FarmTech Solutions - Assistente Agrícola Inteligente")
st.markdown("---")


def carregar_modelo(caminho):
    if os.path.exists(caminho):
        return joblib.load(caminho)
    return None


def carregar_dados():
    caminhos = ["dados/dados_agricolas.csv", "dados_agricolas.csv"]
    for caminho in caminhos:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)
    return None


def carregar_dados_acoes():
    caminhos = ["dados/dados_com_acoes.csv", "dados_com_acoes.csv"]
    for caminho in caminhos:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)
    return None


def gerar_recomendacoes(volume_irrigacao, necessidade_fertilizacao, umidade, ph, nitrogenio, fosforo, potassio):
    recomendacoes = []
    
    if volume_irrigacao > 150:
        recomendacoes.append({
            'tipo': 'Irrigação Urgente',
            'acao': f'Aplicar {volume_irrigacao:.0f} litros/hectare de água',
            'prioridade': 'Alta',
            'motivo': 'Umidade do solo muito baixa'
        })
    elif volume_irrigacao > 50:
        recomendacoes.append({
            'tipo': 'Irrigação Moderada',
            'acao': f'Aplicar {volume_irrigacao:.0f} litros/hectare de água',
            'prioridade': 'Média',
            'motivo': 'Umidade do solo abaixo do ideal'
        })
    else:
        recomendacoes.append({
            'tipo': 'Irrigação Não Necessária',
            'acao': 'Manter monitoramento',
            'prioridade': 'Baixa',
            'motivo': 'Umidade do solo adequada'
        })
    
    if necessidade_fertilizacao >= 7:
        recomendacoes.append({
            'tipo': 'Fertilização Urgente',
            'acao': 'Aplicar fertilizante completo NPK',
            'prioridade': 'Alta',
            'motivo': f'Necessidade: {necessidade_fertilizacao:.1f}/10'
        })
    elif necessidade_fertilizacao >= 4:
        recomendacoes.append({
            'tipo': 'Fertilização Moderada',
            'acao': 'Aplicar fertilizante conforme deficiências',
            'prioridade': 'Média',
            'motivo': f'Necessidade: {necessidade_fertilizacao:.1f}/10'
        })
    else:
        recomendacoes.append({
            'tipo': 'Fertilização Não Necessária',
            'acao': 'Manter monitoramento',
            'prioridade': 'Baixa',
            'motivo': 'Nutrientes em níveis adequados'
        })
    
    if not nitrogenio:
        recomendacoes.append({
            'tipo': 'Correção de Solo',
            'acao': 'Adicionar nitrogênio',
            'prioridade': 'Média',
            'motivo': 'Deficiência de nitrogênio detectada'
        })
    
    if not fosforo:
        recomendacoes.append({
            'tipo': 'Correção de Solo',
            'acao': 'Adicionar fósforo',
            'prioridade': 'Média',
            'motivo': 'Deficiência de fósforo detectada'
        })
    
    if not potassio:
        recomendacoes.append({
            'tipo': 'Correção de Solo',
            'acao': 'Adicionar potássio',
            'prioridade': 'Média',
            'motivo': 'Deficiência de potássio detectada'
        })
    
    if ph < 6.0 or ph > 8.0:
        recomendacoes.append({
            'tipo': 'Correção de pH',
            'acao': f'Ajustar pH para próximo de 7.0 (atual: {ph:.1f})',
            'prioridade': 'Alta',
            'motivo': 'pH fora da faixa ideal'
        })
    
    return recomendacoes


modelo_rendimento = carregar_modelo("modelos/modelo_rendimento.pkl")
modelo_umidade = carregar_modelo("modelos/modelo_umidade.pkl")
modelo_ph = carregar_modelo("modelos/modelo_ph.pkl")
modelo_irrigacao = carregar_modelo("modelos/modelo_irrigacao.pkl")
modelo_fertilizacao = carregar_modelo("modelos/modelo_fertilizacao.pkl")

dados = carregar_dados()
dados_acoes = carregar_dados_acoes()

st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione uma seção:",
    [
        "Visão Geral",
        "Métricas de Desempenho",
        "Análise de Correlação",
        "Previsões Rendimento",
        "Previsões Umidade e pH",
        "Ações Agrícolas",
        "Análise de Ações",
    ],
)

if pagina == "Visão Geral":
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
        st.subheader("Resumo dos Dados")
        st.dataframe(dados.head(10), use_container_width=True)

        st.subheader("Estatísticas Descritivas")
        st.dataframe(dados.describe(), use_container_width=True)
    else:
        st.info("Execute o script ml_pipeline.py para gerar os dados.")

elif pagina == "Métricas de Desempenho":
    st.header("Métricas de Desempenho dos Modelos")

    metricas_previsao = None
    if os.path.exists("metricas/metricas_previsao.csv"):
        metricas_previsao = pd.read_csv("metricas/metricas_previsao.csv")

    metricas_acoes = None
    if os.path.exists("metricas/metricas_acoes.csv"):
        metricas_acoes = pd.read_csv("metricas/metricas_acoes.csv")

    if metricas_previsao is not None:
        st.subheader("Modelos de Previsão")
        st.dataframe(metricas_previsao, use_container_width=True)

    if metricas_acoes is not None:
        st.subheader("Modelos de Ações")
        st.dataframe(metricas_acoes, use_container_width=True)

    if metricas_previsao is None and metricas_acoes is None:
        st.warning("Métricas não encontradas. Execute ml_pipeline.py primeiro.")

elif pagina == "Análise de Correlação":
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

    else:
        st.warning("Dados não encontrados. Execute o script ml_pipeline.py primeiro.")

elif pagina == "Previsões Rendimento":
    st.header("Previsão de Rendimento em Tempo Real")

    st.markdown(
        "Preencha os valores abaixo para obter uma previsão do rendimento esperado baseada nas condições do solo e nutrientes disponíveis."
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

    if st.button("Calcular Previsão", type="primary"):
        if modelo_rendimento is None:
            st.error("Modelo não encontrado! Execute primeiro o script ml_pipeline.py")
        else:
            previsao = modelo_rendimento.predict(dados_previsao)[0]

            st.markdown("---")
            st.success(f"### Rendimento Previsto: {previsao:.0f} kg/hectare")

            st.subheader("Valores de Entrada")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Umidade", f"{umidade}%")
            with col2:
                st.metric("pH", f"{ph:.1f}")
            with col3:
                st.metric("N", "Sim" if nitrogenio else "Não")
            with col4:
                st.metric("P", "Sim" if fosforo else "Não")
            with col5:
                st.metric("K", "Sim" if potassio else "Não")

            st.markdown("---")
            st.subheader("Recomendações")

            recomendacoes = []

            if umidade < 50:
                recomendacoes.append("ATENÇÃO: Umidade baixa. Considere irrigação.")
            elif umidade > 70:
                recomendacoes.append("ATENÇÃO: Umidade alta. Pode haver excesso de água.")
            else:
                recomendacoes.append("OK: Umidade em nível adequado.")

            if ph < 6.0 or ph > 8.0:
                recomendacoes.append(
                    "ATENÇÃO: pH fora da faixa ideal (6.5-7.5). Considere correção."
                )
            else:
                recomendacoes.append("OK: pH em nível adequado.")

            if not nitrogenio:
                recomendacoes.append(
                    "SUGESTÃO: Considere adicionar nitrogênio para melhorar o rendimento."
                )
            if not fosforo:
                recomendacoes.append(
                    "SUGESTÃO: Considere adicionar fósforo para melhorar o rendimento."
                )
            if not potassio:
                recomendacoes.append(
                    "SUGESTÃO: Considere adicionar potássio para melhorar o rendimento."
                )

            for rec in recomendacoes:
                st.markdown(f"- {rec}")

elif pagina == "Previsões Umidade e pH":
    st.header("Previsão de Umidade e pH do Solo")

    st.markdown(
        "Preencha os dados de nutrientes e rendimento para prever umidade e pH do solo."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nutrientes Disponíveis")
        nitrogenio = st.checkbox("Nitrogênio (N) presente", value=True)
        fosforo = st.checkbox("Fósforo (P) presente", value=True)
        potassio = st.checkbox("Potássio (K) presente", value=True)

    with col2:
        rendimento = st.number_input(
            "Rendimento Esperado (kg/hectare)",
            min_value=500.0,
            max_value=5000.0,
            value=2000.0,
            step=100.0,
        )

    n_val = 1 if nitrogenio else 0
    p_val = 1 if fosforo else 0
    k_val = 1 if potassio else 0

    if modelo_umidade is None or modelo_ph is None:
        st.warning(
            "Modelos de umidade e pH não encontrados. Execute ml_pipeline.py primeiro."
        )
    else:
        dados_entrada = pd.DataFrame(
            {
                "nitrogenio": [n_val],
                "fosforo": [p_val],
                "potassio": [k_val],
                "rendimento": [rendimento],
            }
        )

        if dados is not None and len(dados) > 0:
            features = criar_features_umidade_ph(dados_entrada, dados)

            if st.button("Prever Umidade e pH", type="primary"):
                previsao_umidade = modelo_umidade.predict(features)[0]
                previsao_umidade = max(0, min(100, previsao_umidade))

                previsao_ph = modelo_ph.predict(features)[0]
                previsao_ph = max(0, min(14, previsao_ph))

                st.markdown("---")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Umidade Prevista")
                    st.metric("Umidade do Solo", f"{previsao_umidade:.1f}%")
                    if previsao_umidade < 50:
                        st.warning("ATENÇÃO: Umidade baixa prevista")
                    elif previsao_umidade > 70:
                        st.warning("ATENÇÃO: Umidade alta prevista")
                    else:
                        st.success("OK: Umidade em faixa adequada")

                with col2:
                    st.subheader("pH Previsto")
                    st.metric("pH do Solo", f"{previsao_ph:.2f}")
                    if previsao_ph < 6.0 or previsao_ph > 8.0:
                        st.warning("ATENÇÃO: pH fora da faixa ideal")
                    else:
                        st.success("OK: pH em faixa adequada")

                st.markdown("---")
                st.subheader("Dados de Entrada Utilizados")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("N", "Sim" if nitrogenio else "Não")
                with col2:
                    st.metric("P", "Sim" if fosforo else "Não")
                with col3:
                    st.metric("K", "Sim" if potassio else "Não")
                with col4:
                    st.metric("Rendimento", f"{rendimento:.0f} kg/ha")
        else:
            st.info("Carregue os dados primeiro executando ml_pipeline.py")

elif pagina == "Ações Agrícolas":
    st.header("Previsões e Recomendações de Ações")

    st.markdown("Preencha os dados do solo para receber recomendações de irrigação e fertilização.")

    col1, col2 = st.columns(2)

    with col1:
        umidade = st.slider("Umidade do Solo (%)", min_value=0, max_value=100, value=60, step=1)
        ph = st.slider("pH do Solo", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

    with col2:
        st.subheader("Nutrientes Disponíveis")
        nitrogenio = st.checkbox("Nitrogênio (N) presente", value=True)
        fosforo = st.checkbox("Fósforo (P) presente", value=True)
        potassio = st.checkbox("Potássio (K) presente", value=True)

    n_val = 1 if nitrogenio else 0
    p_val = 1 if fosforo else 0
    k_val = 1 if potassio else 0

    dados_entrada = pd.DataFrame({
        "umidade": [umidade],
        "ph": [ph],
        "nitrogenio": [n_val],
        "fosforo": [p_val],
        "potassio": [k_val],
    })

    if st.button("Gerar Recomendações", type="primary"):
        if modelo_irrigacao is None or modelo_fertilizacao is None:
            st.error("Modelos não encontrados! Execute primeiro ml_pipeline.py")
        else:
            features_irrigacao = criar_features_irrigacao(dados_entrada)
            features_fertilizacao = criar_features_fertilizacao(dados_entrada)

            volume_irrigacao = modelo_irrigacao.predict(features_irrigacao)[0]
            volume_irrigacao = max(0, volume_irrigacao)

            necessidade_fertilizacao = modelo_fertilizacao.predict(features_fertilizacao)[0]
            necessidade_fertilizacao = np.clip(necessidade_fertilizacao, 0, 10)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Volume de Irrigação")
                st.metric("Litros/hectare", f"{volume_irrigacao:.0f}")
                if volume_irrigacao > 150:
                    st.error("URGENTE: Irrigação urgente necessária")
                elif volume_irrigacao > 50:
                    st.warning("ATENÇÃO: Irrigação moderada recomendada")
                else:
                    st.success("OK: Irrigação não necessária no momento")

            with col2:
                st.subheader("Necessidade de Fertilização")
                st.metric("Pontuação (0-10)", f"{necessidade_fertilizacao:.1f}")
                if necessidade_fertilizacao >= 7:
                    st.error("URGENTE: Fertilização urgente necessária")
                elif necessidade_fertilizacao >= 4:
                    st.warning("ATENÇÃO: Fertilização moderada recomendada")
                else:
                    st.success("OK: Fertilização não necessária no momento")

            st.markdown("---")
            st.subheader("Recomendações Detalhadas")

            recomendacoes = gerar_recomendacoes(
                volume_irrigacao, necessidade_fertilizacao,
                umidade, ph, nitrogenio, fosforo, potassio
            )

            for rec in recomendacoes:
                if rec['prioridade'] == 'Alta':
                    st.error(f"ALTA PRIORIDADE: **{rec['tipo']}** - {rec['acao']}")
                    st.caption(f"Motivo: {rec['motivo']}")
                elif rec['prioridade'] == 'Média':
                    st.warning(f"MÉDIA PRIORIDADE: **{rec['tipo']}** - {rec['acao']}")
                    st.caption(f"Motivo: {rec['motivo']}")
                else:
                    st.info(f"BAIXA PRIORIDADE: **{rec['tipo']}** - {rec['acao']}")
                    st.caption(f"Motivo: {rec['motivo']}")

elif pagina == "Análise de Ações":
    st.header("Análise de Ações Recomendadas")

    if dados_acoes is not None:
        st.subheader("Distribuição de Volume de Irrigação")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(dados_acoes['volume_irrigacao'], bins=30, color='skyblue', edgecolor='black')
        ax.set_xlabel('Volume de Irrigação (litros/hectare)')
        ax.set_ylabel('Frequência')
        ax.set_title('Distribuição de Volumes de Irrigação Recomendados')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        st.markdown("---")

        st.subheader("Distribuição de Necessidade de Fertilização")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(dados_acoes['necessidade_fertilizacao'], bins=20, color='lightgreen', edgecolor='black')
        ax.set_xlabel('Necessidade de Fertilização (0-10)')
        ax.set_ylabel('Frequência')
        ax.set_title('Distribuição de Necessidades de Fertilização')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    else:
        st.warning("Dados não encontrados. Execute o script ml_pipeline.py primeiro.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "FarmTech Solutions - Assistente Agrícola Inteligente"
    "</div>",
    unsafe_allow_html=True,
)
