import streamlit as st
from utilidades import *
import matplotlib.pyplot as plt


def painel():
    df = st.session_state["dados_excel"]

    st.title("Painel - :green[Controle De Migração]")

    clientes = list(df["FRENTE DE TRABALHO"].unique())
    clientes.append("TODOS")
    col1, col2, col3 = st.columns([0.4, 0.6, 0.4])
    cliente = col1.selectbox(
        "FRENTE DE TRABALHO: ".title(), clientes, index=(len(clientes) - 1)
    )
    col3.info("Se um dos cards não aparecer, é porque o valor total é 0.", icon="ℹ️")

    if cliente == "TODOS":
        df_atual = df
    else:
        df_atual = df[(df["FRENTE DE TRABALHO"] == cliente)]
    total = len(df_atual)

    col1, col2 = st.columns(2)

    plt1 = grafico_pizza(df_atual["SOLUÇÃO PADRÃO"])
    _card_grafico(col1, "SOLUÇÃO PADRÃO".title(), plt1)
    plt.clf()

    plt2 = grafico_pizza(df_atual["STATUS DETALHADO"])
    _card_grafico(col2, "STATUS DETALHADO".title(), plt2)
    plt.clf()

    col1, col2, col3 = st.columns(3)

    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]
    df_migracao = df_atual[(df_atual["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA")]

    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()

    contagem_area_responsavel_operacao = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "OPERAÇÃO"
    ].value_counts()

    contagem_migracao_concluida = df_migracao["ÁREA RESPONSÁVEL"].value_counts()

    try:
        _card(
            col1,
            "AGUARDANDO ABERTURA OS - UN".title(),
            int(contagem_area_responsavel_un),
        )

        _card(
            col2,
            "AGUARDANDO ABERTURA OS - OPERAÇÃO".title(),
            int(contagem_area_responsavel_operacao),
        )
        _card(
            col3,
            "MIGRAÇÃO CONCLUÍDA".title(),
            int(contagem_migracao_concluida),
        )
    except:
        pass


def _card(col1, titulo, total):

    col1.markdown(
        f"{titulo}",
    )
    col1.markdown(
        f"<h4 style='text-align: center;'>Total: {total}</h4>", unsafe_allow_html=True
    )
    col1.divider()


def _card_grafico(col1, titulo, plt):
    col1.divider()
    col1.markdown(f"{titulo}")
    col1.pyplot(plt)
    col1.divider()


def _filtro_contagem_area_responsavel(df_atual):
    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]
    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()


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
