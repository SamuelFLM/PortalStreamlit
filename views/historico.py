import streamlit as st
from utilidades import *
import numpy as np


def historico():
    df = st.session_state["dados_excel"]
    df_metas = st.session_state["dados_metas"]
    # df_2023 = st.session_state["dados_2023"]

    st.header("Histórico De Migração")
    col1, col2, col3 = st.columns([0.2, 0.2, 0.9])
    ano = col1.selectbox("Ano", ["2024", "2023"])

    st.header("", divider="green")

    aplicar_espaco_entre_componentes()

    if ano == "2024":
        _tabela_2024(df, df_metas)
    else:
        with st.spinner("Carregando..."):
            _tabela_2023()


def _tabela_2024(df, df_metas):

    # Filtragem dos dados onde o status detalhado é "MIGRAÇÃO CONCLUÍDA"
    df_filtro_migracao = df[df["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]

    # Contagem dos valores e criação do dataframe
    resultado = df_filtro_migracao["MÊS CONCLUSÃO"].value_counts()
    df_historico = pd.DataFrame(
        {"Mês": resultado.index, "Meta": "1000", "Resultado": resultado.values}
    )

    # Adição da coluna "Farol" com emojis
    # df_historico["Farol"] = df_historico["Resultado"].apply(lambda x: '🟢' if (x/len(df_filtro_migracao) * 100) >= 10 else ('🟡' if 3 <= (x/len(df_filtro_migracao) * 100) <= 10 else '🔴'))
    df_historico["Farol"] = df_historico["Resultado"].apply(
        lambda x: "🟢" if x >= 1000 else ("🟡" if x >= 500 else "🔴")
    )

    # Adição da coluna de porcentagem
    df_historico["Porcentagem"] = ((df_historico["Resultado"] / 1000) * 100).round(
        2
    ).astype(str) + "%"
    df_historico["Total"] = (
        df_filtro_migracao.groupby("STATUS DETALHADO").count()["STATUS"].iloc[0]
    )

    # filtro
    coluna_filtro_mes, coluna_filtro_farol, col3, col4 = st.columns([0.3, 0.3, 0.3, 1])

    df_mes, mes = _filtro(coluna_filtro_mes, df_historico, "Mês", "Mês")

    col1, col2, col3 = st.columns([0.8,0.9,0.3])

    col1.dataframe(df_historico, width=400, hide_index=True)
    if mes != "Selecione":
        tabela_metas_historico(df, df_metas, mes, col2, col3)
       


def _tabela_2023():
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }
    
    excel = "Controle Migração Cobre Para Fibra fechamento 2023.xlsx"
    df = pd.read_excel(PASTA_EXCEL / excel, engine="openpyxl", sheet_name="LISTA")
    df["MÊS"] = pd.to_datetime(df["MÊS"])
    df["MÊS"] = df["MÊS"].dt.month.map(meses)

    df_filtro_migracao = df[df["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]

    # Contando os valores e criando o dataframe
    resultado = df_filtro_migracao["MÊS"].value_counts()
    df_historico = pd.DataFrame({"Mês": resultado.index, "Resultado": resultado.values})

    # Adicionando a coluna "Farol" com emojis
    # df_historico["Farol"] = df_historico["Resultado"].apply(lambda x: '🟢' if (x/len(df_filtro_migracao) * 100) >= 10 else ('🟡' if 3 <= (x/len(df_filtro_migracao) * 100) <= 10 else '🔴'))
    df_historico["Farol"] = df_historico["Resultado"].apply(
        lambda x: (
            "🟢"
            if x >= 1
            else ("🟡" if 3 <= (x / len(df_filtro_migracao) * 100) <= 10 else "🔴")
        )
    )

    # Adicionando a coluna de porcentagem
    # df_historico["Porcentagem"] = ((df_historico["Resultado"] / len(df_filtro_migracao)) * 100).round(2).astype(str) + '%'
    df_historico["Porcentagem"] = "100" + "%"

    # Ordenando a tabela de Janeiro a Dezembro
    ordem_meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    df_historico["Mês"] = pd.Categorical(
        df_historico["Mês"], categories=ordem_meses, ordered=True
    )
    df_historico.sort_values(by="Mês", inplace=True)

    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 1])
    # df_mes, mes = _filtro(col1, df_historico, "Mês", "Mês")

    # if mes != "Selecione":
    #     df_atual = df_mes
    # else:
    #     df_atual = df_historico

    col1, col2, col3, col4 = st.columns([0.9, 0.3, 0.3, 1])

    col1.dataframe(df_historico, width=450, height=460, hide_index=True)

    col2.metric(
        "Total Migração Concluída",
        int(df_filtro_migracao.groupby("STATUS DETALHADO").count()["MÊS"]),
        "100%",
    )
    col2.divider()


def _filtro(coluna, df, coluna_tabela, nome_filtro):
    lista_unica = list(df[coluna_tabela].unique())
    lista_unica.append("Selecione")
    escolha = coluna.selectbox(nome_filtro, lista_unica, index=(len(lista_unica) - 1))
    df_filtro = df[df[coluna_tabela] == escolha]
    return df_filtro, escolha
