import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="FarmTech Solutions - Dashboard Integrado",
    layout="wide",
)

# ─── Feature engineering (Fase 4 / utils.py) ────────────────────────────────

def feat_rendimento(d):
    X = d[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    X["ph_dist"]  = abs(X["ph"] - 7.0)
    X["umid2"]    = X["umidade"] ** 2
    X["npk"]      = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["umid_ph"]  = X["umidade"] * X["ph"]
    return X

def feat_umid_ph(d, rend_mean, rend_std):
    X = d[["nitrogenio", "fosforo", "potassio", "rendimento"]].copy()
    X["npk"]       = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["rend_norm"] = (X["rendimento"] - rend_mean) / rend_std if rend_std > 0 else 0.0
    return X

def feat_irrigacao(d):
    X = d[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    X["umid2"]   = X["umidade"] ** 2
    X["ph_dist"] = abs(X["ph"] - 7.0)
    X["npk"]     = X["nitrogenio"] + X["fosforo"] + X["potassio"]
    X["umid_ph"] = X["umidade"] * X["ph"]
    return X

def feat_fertilizacao(d):
    X = d[["umidade", "ph", "nitrogenio", "fosforo", "potassio"]].copy()
    X["ph_dist"]  = abs(X["ph"] - 7.0)
    X["faltam"]   = ((X["nitrogenio"]==0).astype(int)
                    + (X["fosforo"]==0).astype(int)
                    + (X["potassio"]==0).astype(int))
    X["umid_baixa"] = (X["umidade"] < 50).astype(int)
    X["ph_ruim"]    = ((X["ph"] < 6.0) | (X["ph"] > 8.0)).astype(int)
    return X

# ─── Treinar modelos uma vez por sessão (Fase 4 / ml_pipeline.py) ────────────

@st.cache_resource
def treinar_modelos():
    np.random.seed(42)
    n = 200

    umidade    = np.random.uniform(30, 90, n)
    ph         = np.random.uniform(5.5, 8.5, n)
    nitrogenio = np.random.choice([0, 1], n, p=[0.3, 0.7])
    fosforo    = np.random.choice([0, 1], n, p=[0.3, 0.7])
    potassio   = np.random.choice([0, 1], n, p=[0.3, 0.7])

    rendimento = np.clip(
        1500
        + 10 * umidade - 0.1 * (umidade - 60) ** 2
        + 200 * ph - 15 * (ph - 7.0) ** 2
        + nitrogenio * 300 + fosforo * 250 + potassio * 200
        + np.random.normal(0, 150, n),
        800, 4000,
    )
    volume_irrigacao = np.clip(100 + (60 - umidade) * 2, 0, 300)
    nec_fert = np.clip(
        (nitrogenio == 0) * 3
        + (fosforo == 0) * 2
        + (potassio == 0) * 2
        + (np.abs(ph - 7.0) > 1.0) * 2
        + (umidade < 40) * 1,
        0, 10,
    )

    dados = pd.DataFrame({
        "umidade": umidade, "ph": ph,
        "nitrogenio": nitrogenio, "fosforo": fosforo, "potassio": potassio,
        "rendimento": rendimento,
        "volume_irrigacao": volume_irrigacao,
        "necessidade_fertilizacao": nec_fert,
    })

    rend_mean = dados["rendimento"].mean()
    rend_std  = dados["rendimento"].std()

    def fit(X, y):
        m = LinearRegression()
        m.fit(X, y)
        return m

    m_rend  = fit(feat_rendimento(dados), dados["rendimento"])
    m_umid  = fit(feat_umid_ph(dados, rend_mean, rend_std), dados["umidade"])
    m_ph    = fit(feat_umid_ph(dados, rend_mean, rend_std), dados["ph"])
    m_irrig = fit(feat_irrigacao(dados), dados["volume_irrigacao"])
    m_fert  = fit(feat_fertilizacao(dados), dados["necessidade_fertilizacao"])

    return dados, m_rend, m_umid, m_ph, m_irrig, m_fert, rend_mean, rend_std

# ─── Helpers ─────────────────────────────────────────────────────────────────

def enviar_alerta_aws(topico_arn, mensagem, assunto, regiao="us-east-1"):
    try:
        import boto3
        sns = boto3.client("sns", region_name=regiao)
        sns.publish(TopicArn=topico_arn, Message=mensagem, Subject=assunto)
        return True, "Alerta enviado via AWS SNS!"
    except ImportError:
        return False, "boto3 nao instalado. Execute: pip install boto3"
    except Exception as e:
        return False, f"Erro AWS: {e}"

# ─── Session state ────────────────────────────────────────────────────────────

if "colheitas" not in st.session_state:
    st.session_state.colheitas = []
if "leituras_sensor" not in st.session_state:
    st.session_state.leituras_sensor = []

# ─── Sidebar ─────────────────────────────────────────────────────────────────

st.sidebar.title("FarmTech Solutions")
st.sidebar.markdown("Sistema Integrado de Gestão Agrícola")
pagina = st.sidebar.radio(
    "Navegação:",
    [
        "Visão Geral",
        "Fase 1 - Área e Insumos",
        "Fase 2 - Gestão de Colheita",
        "Fase 3 - Sensores IoT",
        "Fase 4 - Previsões ML",
        "Fase 6 - Visão Computacional",
        "Alertas AWS",
    ],
)

# ═══════════════════════════════════════════════════════════════════════════════
# VISÃO GERAL
# ═══════════════════════════════════════════════════════════════════════════════
if pagina == "Visão Geral":
    st.title("FarmTech Solutions — Dashboard Integrado (Fase 7)")
    st.markdown("Integração de todas as fases do projeto de gestão agrícola inteligente.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Colheitas Cadastradas", len(st.session_state.colheitas))
    with col2:
        st.metric("Leituras de Sensor", len(st.session_state.leituras_sensor))
    with col3:
        alertas_ativos = sum(
            1 for l in st.session_state.leituras_sensor if l.get("alerta", False)
        )
        st.metric("Leituras com Alerta", alertas_ativos)

    st.markdown("---")
    st.subheader("Fases do Projeto")

    fases = [
        ("Fase 1", "Cálculo de área de plantio e manejo de insumos para Café e Soja"),
        ("Fase 2", "Gestão de colheita de cana-de-açúcar com análise de perdas"),
        ("Fase 3", "Sensores IoT ESP32: umidade (DHT22), pH (LDR), automação da bomba"),
        ("Fase 4", "Machine Learning com Scikit-Learn para previsão de rendimento e ações"),
        ("Fase 5", "Cloud Computing AWS — infraestrutura segura e escalável"),
        ("Fase 6", "Visão computacional (YOLO) para análise de saúde das plantações"),
        ("Fase 7", "Integração de todas as fases em um único dashboard + alertas AWS SNS"),
    ]
    for fase, desc in fases:
        st.markdown(f"**{fase}:** {desc}")

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1 — ÁREA E INSUMOS
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Fase 1 - Área e Insumos":
    st.title("Fase 1 — Cálculo de Área e Insumos")
    st.markdown("Baseado em `Fase 1/play-na-sua-carreira-em-ia/atividade.py`")

    cultura = st.selectbox("Cultura:", ["Café", "Soja"])

    col1, col2 = st.columns(2)
    with col1:
        comprimento = st.number_input("Comprimento (ha):", min_value=0.1, value=10.0, step=0.1)
        largura     = st.number_input("Largura (ha):", min_value=0.1, value=5.0, step=0.1)
    with col2:
        espacamento = st.number_input("Espaçamento entre plantas (m):", min_value=0.1, value=1.5, step=0.1)
        data_op     = st.date_input("Data da operação:")

    if st.button("Calcular", type="primary"):
        if cultura == "Café":
            area    = comprimento * largura                  # retângulo
            insumos = (150 + 100 + 150) * area               # N+P+K em kg/ha
            st.success(f"Área do Café: **{area:.2f} ha** (retângulo)")
            st.info(f"Macronutrientes totais (N+P+K): **{insumos:.0f} kg**")
            st.caption("Nitrogênio 150 kg/ha · Fósforo 100 kg/ha · Potássio 150 kg/ha")
        else:
            area    = (comprimento * largura) / 2            # triângulo
            insumos = 8_000 * area                           # m³ de água
            st.success(f"Área da Soja: **{area:.2f} ha** (triângulo)")
            st.info(f"Água para irrigação: **{insumos:.0f} m³**")
            st.caption("Referência: 8.000 m³ de água por hectare")

        resumo = pd.DataFrame({
            "Campo": ["Cultura", "Data", "Comprimento", "Largura", "Espaçamento", "Área", "Insumo"],
            "Valor": [
                cultura, str(data_op),
                f"{comprimento} ha", f"{largura} ha", f"{espacamento} m",
                f"{area:.2f} ha",
                f"{insumos:.0f} {'kg' if cultura == 'Café' else 'm³'}",
            ],
        })
        st.dataframe(resumo, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2 — GESTÃO DE COLHEITA
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Fase 2 - Gestão de Colheita":
    st.title("Fase 2 — Gestão de Colheita de Cana-de-Açúcar")
    st.markdown("Baseado em `Fase 2/Python e Alem/sistema.py`")

    tab_cad, tab_list, tab_rel = st.tabs(["Cadastrar", "Listar", "Relatório"])

    with tab_cad:
        st.subheader("Nova Colheita")
        col1, col2 = st.columns(2)
        with col1:
            prop      = st.text_input("Propriedade:")
            data_col  = st.date_input("Data da colheita:")
            tipo      = st.selectbox("Tipo:", ["manual", "mecanica"])
        with col2:
            toneladas = st.number_input("Toneladas colhidas:", min_value=0.1, value=100.0, step=1.0)
            preco     = st.number_input("Preço por tonelada (R$):", min_value=0.1, value=200.0, step=10.0)

        if st.button("Cadastrar", type="primary"):
            if not prop.strip():
                st.error("Digite o nome da propriedade.")
            else:
                percentual = 5 if tipo == "manual" else 15
                perda      = toneladas * percentual / 100
                prejuizo   = perda * preco
                st.session_state.colheitas.append({
                    "propriedade": prop,
                    "data": str(data_col),
                    "tipo": tipo,
                    "toneladas": toneladas,
                    "preco": preco,
                    "perda": perda,
                    "percentual": percentual,
                    "prejuizo": prejuizo,
                })
                st.success(
                    f"Cadastrada! Perda: {perda:.2f} t ({percentual}%) | "
                    f"Prejuízo: R$ {prejuizo:.2f}"
                )

    with tab_list:
        if not st.session_state.colheitas:
            st.info("Nenhuma colheita cadastrada.")
        else:
            df = pd.DataFrame(st.session_state.colheitas)
            cols = ["propriedade", "data", "tipo", "toneladas", "perda", "prejuizo"]
            df_show = df[cols].copy()
            df_show.columns = ["Propriedade", "Data", "Tipo", "Toneladas", "Perda (t)", "Prejuízo (R$)"]
            st.dataframe(df_show, use_container_width=True)
            st.download_button("Baixar CSV", df.to_csv(index=False), "colheitas.csv", "text/csv")

    with tab_rel:
        if not st.session_state.colheitas:
            st.info("Cadastre colheitas para ver o relatório.")
        else:
            df = pd.DataFrame(st.session_state.colheitas)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Colheitas", len(df))
            with col2:
                st.metric("Total Colhido", f"{df['toneladas'].sum():.1f} t")
            with col3:
                st.metric("Prejuízo Total", f"R$ {df['prejuizo'].sum():,.2f}")

            if len(df) >= 2:
                fig, ax = plt.subplots(figsize=(7, 4))
                por_tipo = df.groupby("tipo")["perda"].mean()
                ax.bar(por_tipo.index, por_tipo.values, color=["skyblue", "salmon"])
                ax.set_title("Perda Média por Tipo de Colheita")
                ax.set_ylabel("Toneladas")
                st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 3 — SENSORES IoT
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Fase 3 - Sensores IoT":
    st.title("Fase 3 — Sensores IoT (ESP32)")
    st.markdown(
        "Simula leituras do ESP32: umidade via DHT22, pH via LDR, "
        "e lógica de ativação da bomba de irrigação."
    )

    UMID_MIN, UMID_MAX = 40, 70
    PH_MIN,   PH_MAX   = 6.0, 8.0

    col1, col2 = st.columns(2)
    with col1:
        umidade_s = st.slider("Umidade DHT22 (%):", 0, 100, 55)
        ph_s      = st.slider("pH via LDR:", 0.0, 14.0, 6.5, 0.1)
    with col2:
        nitro_s = st.checkbox("Nitrogênio detectado", value=True)
        fosfo_s = st.checkbox("Fósforo detectado",    value=True)
        potas_s = st.checkbox("Potássio detectado",   value=False)

    if st.button("Registrar Leitura", type="primary"):
        bomba   = umidade_s < UMID_MIN
        alertas = []
        if bomba:
            alertas.append("UMIDADE BAIXA — Bomba de irrigação ATIVADA")
        if umidade_s > UMID_MAX:
            alertas.append("UMIDADE ALTA — Verificar drenagem")
        if ph_s < PH_MIN or ph_s > PH_MAX:
            alertas.append(f"pH {ph_s:.1f} FORA DA FAIXA — Corrigir solo")
        if not nitro_s:
            alertas.append("NITROGÊNIO AUSENTE — Aplicar adubação")
        if not fosfo_s:
            alertas.append("FÓSFORO AUSENTE — Aplicar adubação")
        if not potas_s:
            alertas.append("POTÁSSIO AUSENTE — Aplicar adubação")

        st.session_state.leituras_sensor.append({
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "umidade": umidade_s, "ph": ph_s,
            "nitrogenio": nitro_s, "fosforo": fosfo_s, "potassio": potas_s,
            "bomba_ativa": bomba,
            "alerta": len(alertas) > 0,
            "alertas": alertas,
        })

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Umidade", f"{umidade_s}%")
        with col2:
            st.metric("pH", f"{ph_s:.1f}")
        with col3:
            if bomba:
                st.error("BOMBA: ATIVA")
            else:
                st.success("BOMBA: INATIVA")

        if alertas:
            for a in alertas:
                st.warning(a)
        else:
            st.success("Todos os sensores dentro dos limites normais.")

    if st.session_state.leituras_sensor:
        st.markdown("---")
        st.subheader("Histórico de Leituras")
        df_s = pd.DataFrame(st.session_state.leituras_sensor)
        st.dataframe(
            df_s[["timestamp", "umidade", "ph", "bomba_ativa", "alerta"]].tail(10),
            use_container_width=True,
        )

        if len(df_s) >= 2:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            idx = range(len(df_s))

            axes[0].plot(idx, df_s["umidade"], marker="o", color="blue")
            axes[0].axhline(UMID_MIN, color="red",    linestyle="--", label="Mín")
            axes[0].axhline(UMID_MAX, color="orange", linestyle="--", label="Máx")
            axes[0].set_title("Histórico de Umidade")
            axes[0].set_ylabel("%")
            axes[0].legend()

            axes[1].plot(idx, df_s["ph"], marker="o", color="green")
            axes[1].axhline(PH_MIN, color="red",    linestyle="--", label="Mín")
            axes[1].axhline(PH_MAX, color="orange", linestyle="--", label="Máx")
            axes[1].set_title("Histórico de pH")
            axes[1].legend()

            st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 4 — PREVISÕES ML
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Fase 4 - Previsões ML":
    st.title("Fase 4 — Previsões com Machine Learning")
    st.markdown("Baseado em `Fase 4/Capitulo 1/dashboard.py` e `ml_pipeline.py`")

    with st.spinner("Treinando modelos..."):
        dados, m_rend, m_umid, m_ph, m_irrig, m_fert, rend_mean, rend_std = treinar_modelos()

    st.success("Modelos prontos (LinearRegression, Scikit-Learn).")

    secao = st.radio(
        "Seção:",
        ["Previsão de Rendimento", "Ações Agrícolas", "Análise dos Dados"],
        horizontal=True,
    )

    if secao == "Previsão de Rendimento":
        col1, col2 = st.columns(2)
        with col1:
            umid = st.slider("Umidade (%):", 0, 100, 60)
            ph   = st.slider("pH:",          0.0, 14.0, 7.0, 0.1)
        with col2:
            n = st.checkbox("Nitrogênio (N)", value=True)
            p = st.checkbox("Fósforo (P)",    value=True)
            k = st.checkbox("Potássio (K)",   value=True)

        if st.button("Calcular Previsão", type="primary"):
            entrada = pd.DataFrame({
                "umidade": [umid], "ph": [ph],
                "nitrogenio": [int(n)], "fosforo": [int(p)], "potassio": [int(k)],
            })
            prev = m_rend.predict(feat_rendimento(entrada))[0]
            st.success(f"**Rendimento Previsto: {prev:.0f} kg/hectare**")

            if umid < 50:
                st.warning("Umidade baixa. Considere irrigação.")
            if ph < 6.0 or ph > 8.0:
                st.warning(f"pH {ph:.1f} fora da faixa ideal (6.0–8.0).")

    elif secao == "Ações Agrícolas":
        col1, col2 = st.columns(2)
        with col1:
            umid = st.slider("Umidade (%):", 0, 100, 60, key="ac_u")
            ph   = st.slider("pH:",          0.0, 14.0, 7.0, 0.1, key="ac_p")
        with col2:
            n = st.checkbox("Nitrogênio (N)", value=True, key="ac_n")
            p = st.checkbox("Fósforo (P)",    value=True, key="ac_f")
            k = st.checkbox("Potássio (K)",   value=True, key="ac_k")

        if st.button("Gerar Recomendações", type="primary"):
            entrada = pd.DataFrame({
                "umidade": [umid], "ph": [ph],
                "nitrogenio": [int(n)], "fosforo": [int(p)], "potassio": [int(k)],
            })
            vol  = max(0, m_irrig.predict(feat_irrigacao(entrada))[0])
            fert = float(np.clip(m_fert.predict(feat_fertilizacao(entrada))[0], 0, 10))

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Irrigação (L/ha)", f"{vol:.0f}")
                if   vol > 150: st.error("URGENTE: Irrigar imediatamente!")
                elif vol > 50:  st.warning("Irrigação moderada recomendada")
                else:           st.success("Irrigação não necessária")
            with col2:
                st.metric("Fertilização (0–10)", f"{fert:.1f}")
                if   fert >= 7: st.error("URGENTE: Fertilizar imediatamente!")
                elif fert >= 4: st.warning("Fertilização moderada recomendada")
                else:           st.success("Fertilização não necessária")

    else:
        st.subheader("Amostra dos Dados de Treinamento")
        st.dataframe(dados.head(10), use_container_width=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        cols_corr = ["umidade", "ph", "nitrogenio", "fosforo", "potassio", "rendimento"]
        sns.heatmap(dados[cols_corr].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Matriz de Correlação")
        st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 6 — VISÃO COMPUTACIONAL
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Fase 6 - Visão Computacional":
    st.title("Fase 6 — Visão Computacional")
    st.markdown(
        "Análise de saúde das plantações por processamento de cores. "
        "Baseado no modelo YOLO treinado no notebook `Fase 6/Capitulo 1/src/`."
    )

    imagem = st.file_uploader("Envie uma foto da plantação:", type=["jpg", "jpeg", "png"])

    if imagem:
        from PIL import Image

        img     = Image.open(imagem).convert("RGB")
        img_arr = np.array(img)
        st.image(img, caption="Imagem carregada", use_container_width=True)

        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        total   = r.size

        pct_verde   = np.sum((g > r) & (g > b) & (g > 80))  / total * 100
        pct_amarelo = np.sum((r > 150) & (g > 150) & (b < 100)) / total * 100
        pct_marrom  = np.sum((r > 100) & (g < 80)  & (b < 70))  / total * 100

        if pct_verde > 40:
            status = "Saudável"
            score  = min(100.0, pct_verde * 1.5)
        elif pct_verde > 20:
            status = "Atenção"
            score  = pct_verde
        else:
            status = "Crítico"
            score  = pct_verde * 0.5

        st.markdown("---")
        st.subheader("Resultado da Análise")

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Verde (%)",   f"{pct_verde:.1f}%")
        with col2: st.metric("Amarelo (%)", f"{pct_amarelo:.1f}%")
        with col3: st.metric("Marrom (%)",  f"{pct_marrom:.1f}%")
        with col4: st.metric("Score Saúde", f"{score:.0f}/100")

        if status == "Saudável":
            st.success(f"**{status}** — Plantação aparenta boa saúde.")
        elif status == "Atenção":
            st.warning(f"**{status}** — Sinais de estresse detectados. Monitorar.")
        else:
            st.error(f"**{status}** — Sinais preocupantes. Ação necessária!")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(
            ["Verde\n(Saudável)", "Amarelo\n(Estresse)", "Marrom\n(Doença/Seco)"],
            [pct_verde, pct_amarelo, pct_marrom],
            color=["green", "yellow", "brown"],
            edgecolor="black",
        )
        ax.set_title("Distribuição de Cores da Plantação")
        ax.set_ylabel("% dos pixels")
        st.pyplot(fig)
    else:
        st.info("Envie uma imagem para iniciar a análise.")
        st.markdown("""
**Método:** análise de distribuição de cores (verde, amarelo, marrom) para estimar saúde.

Para análise com o modelo YOLO treinado na Fase 6, consulte o notebook
`Fase 6/Capitulo 1/src/DiegoFilipePereiradeAraujo_rm567064_pbl_fase6.ipynb`.
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# ALERTAS AWS
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "Alertas AWS":
    st.title("Alertas AWS — Serviço de Mensageria SNS")
    st.markdown(
        "Envie alertas de e-mail ou SMS via AWS SNS. "
        "Usa a infraestrutura de nuvem configurada na Fase 5."
    )

    with st.expander("Como configurar o SNS na AWS"):
        st.markdown("""
1. Acesse o AWS Console → **SNS** → **Topics** → **Create topic** (Standard)
2. Copie o **Topic ARN** (ex: `arn:aws:sns:us-east-1:123456789012:farmtech-alertas`)
3. Clique em **Create subscription** → Protocol: **Email** ou **SMS** → adicione destino
4. Confirme a assinatura pelo e-mail recebido
5. Configure credenciais locais: `aws configure`
        """)

    st.subheader("Configuração")
    topico_arn = st.text_input(
        "Topic ARN:",
        placeholder="arn:aws:sns:us-east-1:123456789012:farmtech-alertas",
    )
    regiao = st.selectbox("Região AWS:", ["us-east-1", "sa-east-1", "us-west-2"])

    st.subheader("Compor Alerta")

    TEMPLATES = {
        "Umidade Crítica":
            "ALERTA FARMTECH: Umidade do solo abaixo do limite crítico (< 40%). "
            "Ativar sistema de irrigação imediatamente. Aplicar ~200 L/ha.",
        "pH Fora da Faixa":
            "ALERTA FARMTECH: pH do solo fora da faixa ideal (6.0–8.0). "
            "Risco de perda de rendimento. Aplicar calcário (pH baixo) ou enxofre (pH alto).",
        "Deficiência de Nutrientes":
            "ALERTA FARMTECH: Deficiência de N/P/K detectada pelos sensores. "
            "Aplicar fertilizante NPK conforme análise de solo.",
        "Praga Detectada":
            "ALERTA FARMTECH: Visão computacional detectou possível praga ou doença. "
            "Realizar inspeção presencial e aplicar defensivo se necessário.",
        "Personalizado": "",
    }

    tipo = st.selectbox("Tipo de Alerta:", list(TEMPLATES.keys()))
    msg  = st.text_area("Mensagem:", value=TEMPLATES[tipo], height=130)
    subj = st.text_input(
        "Assunto:",
        value=f"[FarmTech] {tipo} — {datetime.now().strftime('%d/%m/%Y %H:%M')}",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar via AWS SNS", type="primary"):
            if not topico_arn:
                st.error("Insira o Topic ARN.")
            elif not msg:
                st.error("Escreva a mensagem.")
            else:
                ok, resp = enviar_alerta_aws(topico_arn, msg, subj, regiao)
                if ok:
                    st.success(resp)
                else:
                    st.error(resp)

    with col2:
        if st.button("Simular (sem AWS)"):
            if not msg:
                st.warning("Escreva a mensagem.")
            else:
                st.success("Alerta simulado!")
                st.markdown(f"**Assunto:** {subj}")
                st.markdown(f"**Mensagem:** {msg}")
                st.caption(f"Simulado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Alertas automáticos a partir dos sensores IoT
    alertas_pendentes = [
        l for l in st.session_state.leituras_sensor if l.get("alerta", False)
    ]
    if alertas_pendentes:
        st.markdown("---")
        st.subheader("Alertas Automáticos dos Sensores IoT")
        ultima = alertas_pendentes[-1]
        st.warning(f"Última leitura com alerta: **{ultima['timestamp']}**")
        for a in ultima.get("alertas", []):
            st.markdown(f"- {a}")

        if st.button("Enviar Alertas dos Sensores via AWS"):
            if not topico_arn:
                st.error("Configure o Topic ARN acima.")
            else:
                msg_iot = (
                    f"ALERTA FARMTECH — Sensores IoT ({ultima['timestamp']}):\n"
                    + "\n".join(ultima.get("alertas", []))
                )
                ok, resp = enviar_alerta_aws(
                    topico_arn, msg_iot, "[FarmTech] Alerta Sensores IoT", regiao
                )
                if ok:
                    st.success(resp)
                else:
                    st.error(resp)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;'>"
    "FarmTech Solutions · Fase 7 · FIAP Bacharel em Inteligência Artificial"
    "</div>",
    unsafe_allow_html=True,
)
