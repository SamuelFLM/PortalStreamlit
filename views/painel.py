import streamlit as st
from utilidades import *
import matplotlib.pyplot as plt


def painel(df):

    # df = st.session_state["dados_excel"]

    st.markdown("## Painel :green[De Migração]")

    clientes = list(df["FRENTE DE TRABALHO"].unique())
    clientes.append("Selecione")
    col1, col2, col3 = st.columns([0.25, 0.6, 0.4])
    cliente = col1.selectbox(
        "FRENTE DE TRABALHO: ".title(), clientes, index=(len(clientes) - 1)
    )


    if cliente == "Selecione":
        df_atual = df
        cliente_atual = "Total"
    else:
        df_atual = df[(df["FRENTE DE TRABALHO"] == cliente)]
        cliente_atual = cliente

    coluna1, coluna2 = st.columns(2)
    plt1 = grafico_pizza(df_atual["SOLUÇÃO PADRÃO"])
    with coluna1.container(border=True):
        _card_grafico(st, f"SOLUÇÃO PADRÃO - {cliente_atual}".title(), plt1)
    plt.clf()

    plt2 = grafico_pizza(df_atual["STATUS DETALHADO"])
    with coluna2.container(border=True):
        _card_grafico(st, f"STATUS DETALHADO - {cliente_atual}".title(), plt2)

    contagem_un, contagem_operacao = _contagem_os(df_atual)
    df_migracao = df_atual[(df_atual["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA")]
    contagem_migracao_concluida = df_migracao["ÁREA RESPONSÁVEL"].value_counts()
    
    try:
        if contagem_operacao.empty:
            contagem_operacao_atual = 0
        else:
            contagem_operacao_atual = int(contagem_operacao.iloc[0])
        container_aguard_os_detalhado(
            st,
            ["Aguard. Abert. OS - UN", "Aguard. Abert. OS - OPERAÇÃO", "MIGRAÇÃO CONCLUÍDA"],
            [
                int(contagem_un.iloc[0]),
                contagem_operacao_atual,
                int(contagem_migracao_concluida.iloc[0])
                
            ],
        )
    except:
        pass


def _card_grafico(col1, titulo, plt):
    col1.markdown(f"{titulo}")
    col1.pyplot(plt)


def _contagem_os(df_atual):
    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]
    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()

    contagem_area_responsavel_operacao = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "OPERAÇÃO"
    ].value_counts()
    return contagem_area_responsavel_un, contagem_area_responsavel_operacao


def container_aguard_os_detalhado(coluna, titulos, valores, cores=["orange","blue","green"]):
    with coluna.container():
        col1, col2, col3 = st.columns(3)
        # Loop através das colunass, títulos e valores
        for col, titulo, valor, cor in zip([col1, col2, col3], titulos, valores, cores):
            with col.container(border=True):
                st.markdown(f"{titulo.title()}")
                st.write(f"### :{cor}[{str(valor)}]")


def grafico_pizza(coluna):
    valores = coluna.value_counts()
    labels = [
        f"{label}: {value}" for label, value in zip(valores.index, valores.values)
    ]
    # Cria um gráfico de pizza
    plt.figure(figsize=(12, 4))
    plt.pie(valores, autopct="%1.1f%%", labeldistance=1.5)
    soma_total = sum(valores.values)
    plt.axis("equal")
    plt.legend(title=f"Total:{soma_total}", labels=labels)
    return plt
