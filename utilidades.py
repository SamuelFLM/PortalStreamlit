import streamlit as st
import pandas as pd
from pathlib import Path
from time import sleep

PASTA_ATUAL = Path(__file__).parent
PASTA_EXCEL = PASTA_ATUAL / "a" / "test"
PASTA_IMAGEM = PASTA_ATUAL / "img"


@st.cache_data
def carregar_dados():
    excel = "Controle de migração Cobre-Fibra.xlsx"
    df_data = pd.read_excel(PASTA_EXCEL / excel, engine="openpyxl", sheet_name="LISTA")
    return df_data


@st.cache_data
def carregar_dados_2023():
    excel = "Controle Migração Cobre Para Fibra fechamento 2023.xlsx"
    df_data = pd.read_excel(PASTA_EXCEL / excel, engine="openpyxl", sheet_name="LISTA")
    return df_data


@st.cache_data
def carregar_dados_meta():
    excel = "SOP - Migração Cobre para Fibra B2B - Ciclo Jan24 v1.xlsx"
    df_data = pd.read_excel(PASTA_EXCEL / excel, engine="openpyxl", sheet_name="METAS")
    return df_data


@st.cache_data
def carregar_dados_reparo():
    excel = "Base_Rep_CB.xlsx"
    df_data = pd.read_excel(
        PASTA_EXCEL / excel, engine="openpyxl", sheet_name="Planilha1"
    )
    return df_data


def iniciar_dados():
    df = carregar_dados()
    # df_2023 = carregar_dados_2023()
    df_metas = carregar_dados_meta()
    df_reparos = carregar_dados_reparo()

    if not "dados_excel" in st.session_state:
        st.session_state["dados_excel"] = df

    if not "dados_metas" in st.session_state:
        st.session_state["dados_metas"] = df_metas

    if not "dados_reparos" in st.session_state:
        st.session_state["dados_reparos"] = df_reparos

    if not "pagina_central" in st.session_state:
        st.session_state["pagina_central"] = "pag_home"

    # if not "dados_excel_2023" in st.session_state:
    #     st.session_state["dados_2023"] = df_2023


def mudar_pagina(pagina):
    st.session_state["pagina_central"] = pagina


def carregar_elemento():
    with st.spinner("Wait for it..."):
        sleep(0.3)


def configuracao_pagina():
    st.set_page_config(
        "Portal - Operações De Terceiros", page_icon="img\\oi_logo.png", layout="wide"
    )


def aplicar_espaco_entre_componentes():
    st.markdown(
        """
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock] {
    gap: 0rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def tabela_metas_historico(df, df_metas, mes, col_tabela, col_filtro):
    df_filtro = df[df["MÊS CONCLUSÃO"] == mes]

    # Cria um DataFrame com todas as filiais e inicializa o resultado com 0
    df_uf = pd.DataFrame(
        {"UF": df_metas["UF"].unique(), "Meta": df_metas["Meta"], "Resultado": 0}
    )

    # Calcula o número de migrações concluídas por filial
    filial = (
        df_filtro[df_filtro["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]
        .groupby("FILIAL")
        .size()
    )

    # Atualiza o resultado para as filiais que concluíram a migração
    """explicacao
    O método .isin() é usado para filtrar dados e verificar se um valor existe em uma determinada série ou DataFrame. No seu caso, filial.index é uma lista de filiais que concluíram a migração.

    Quando você usa df_uf["UF"].isin(filial.index), está criando uma série booleana que é True para cada filial em df_uf["UF"] que também está presente em filial.index (ou seja, as filiais que concluíram a migração), e False caso contrário.

    Então, df_uf.loc[df_uf["UF"].isin(filial.index), "Resultado"] seleciona as linhas do DataFrame df_uf onde o valor de “UF” está presente no índice do DataFrame filial (ou seja, as filiais que concluíram a migração), e especificamente a coluna “Resultado” dessas linhas
    """
    df_uf.loc[df_uf["UF"].isin(filial.index), "Resultado"] = filial.values

    df_uf["Farol"] = df_uf.apply(
        lambda row: "🟢" if row["Resultado"] >= row["Meta"] else "🔴", axis=1
    )
    df_uf["Porcentagem"] = ((df_uf["Resultado"] / df_uf["Meta"]) * 100).round(2).astype(
        str
    ) + "%"
    df_uf["Colaborador"] = df_metas["Colaborador"]

    farol = col_filtro.selectbox("Farol", ["Selecione", "🟢", "🔴"])
    df_farol_filted = df_uf[df_uf["Farol"] == farol]

    if farol != "Selecione":
        df_farol_atual = df_farol_filted
    else:
        df_farol_atual = df_uf
    col_tabela.dataframe(df_farol_atual, width=460, hide_index=True)


def tabela_metas_colaborador(df_mes, df_metas, col_tabela, col_filtro):

    # Cria um DataFrame com todas as filiais e inicializa o resultado com 0
    df_uf = pd.DataFrame(
        {"UF": df_metas["UF"].unique(), "Meta": df_metas["Meta"], "Resultado": 0}
    )

    # Calcula o número de migrações concluídas por filial
    filial = (
        df_mes[df_mes["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]
        .groupby("FILIAL")
        .size()
    )

    # Atualiza o resultado para as filiais que concluíram a migração
    """explicacao
    O método .isin() é usado para filtrar dados e verificar se um valor existe em uma determinada série ou DataFrame. No seu caso, filial.index é uma lista de filiais que concluíram a migração.

    Quando você usa df_uf["UF"].isin(filial.index), está criando uma série booleana que é True para cada filial em df_uf["UF"] que também está presente em filial.index (ou seja, as filiais que concluíram a migração), e False caso contrário.

    Então, df_uf.loc[df_uf["UF"].isin(filial.index), "Resultado"] seleciona as linhas do DataFrame df_uf onde o valor de “UF” está presente no índice do DataFrame filial (ou seja, as filiais que concluíram a migração), e especificamente a coluna “Resultado” dessas linhas
    """
    df_uf.loc[df_uf["UF"].isin(filial.index), "Resultado"] = filial.values

    df_uf["Farol"] = df_uf.apply(
        lambda row: "🟢" if row["Resultado"] >= row["Meta"] else "🔴", axis=1
    )
    df_uf["Porcentagem"] = ((df_uf["Resultado"] / df_uf["Meta"]) * 100).round(2).astype(
        str
    ) + "%"
    df_uf["Colaborador"] = df_metas["Colaborador"]

    farol = col_filtro.selectbox("Farol", ["Selecione", "🟢", "🔴"])
    df_farol_filted = df_uf[df_uf["Farol"] == farol]

    if farol != "Selecione":
        df_farol_atual = df_farol_filted
    else:
        df_farol_atual = df_uf
    col_tabela.dataframe(df_farol_atual, width=460, hide_index=True)
