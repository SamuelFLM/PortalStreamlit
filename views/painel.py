import streamlit as st
from utilidades import *
import matplotlib.pyplot as plt
from PIL import Image


def painel():
    df = st.session_state["dados_excel"]

    st.markdown("##### Painel :green[De Migração]")

    tab_base(df)

def tab_base(df):
    with st.expander("Filtro"):
        col1, col2, col3 = st.columns([0.25, 0.25, 0.4])
        
        clientes = list(df["FRENTE DE TRABALHO"].unique())
        clientes.append("Selecione")
        cliente = col1.selectbox(
            "FRENTE DE TRABALHO: ".title(), clientes, index=(len(clientes) - 1)
        )
        df_cliente = df[(df["FRENTE DE TRABALHO"] == cliente)]
        
        projetos = list(df_cliente["PROJETO"].unique())
        projetos.append("Selecione")
        projeto = col2.selectbox(
            "PROJETO: ".title(), projetos, index=(len(projetos) - 1)
        )
        df_projeto = df_cliente[df_cliente["PROJETO"] == projeto]

    if cliente == "Selecione":
        df_atual = df
        cliente_atual = "Total"
    else:
        df_atual = df_cliente
        cliente_atual = cliente
    
    if projeto != "Selecione":
        df_atual = df_projeto
    

    coluna1, coluna2 = st.columns(2)
    plt1 = grafico_pizza(df_atual["SOLUÇÃO PADRÃO"], "img/solucao_padrao.png")
    with coluna1.container(border=True):
        st.image(plt1, caption="SOLUÇÃO PADRÃO")
    plt.clf()

    plt2 = grafico_pizza(df_atual["STATUS DETALHADO"], "img/status_detalhado.png")
    with coluna2.container(border=True):
        st.image(plt2, caption="STATUS DETALHADO")

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
            [
                "Aguard. Abert. OS - UN",
                "Aguard. Abert. OS - OPERAÇÃO",
                "MIGRAÇÃO CONCLUÍDA",
            ],
            [
                int(contagem_un.iloc[0]),
                contagem_operacao_atual,
                int(contagem_migracao_concluida.iloc[0]),
            ],
        )
    except:
        pass
    
def _contagem_os(df_atual):
    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]
    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()

    contagem_area_responsavel_operacao = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "OPERAÇÃO"
    ].value_counts()
    return contagem_area_responsavel_un, contagem_area_responsavel_operacao


def container_aguard_os_detalhado(
    coluna, titulos, valores, cores=["orange", "blue", "green"]
):
    with coluna.container():
        col1, col2, col3 = st.columns(3)
        # Loop através das colunass, títulos e valores
        for col, titulo, valor, cor in zip([col1, col2, col3], titulos, valores, cores):
            with col.container(border=True):
                st.markdown(f"{titulo.title()}")
                st.write(f"### :{cor}[{str(valor)}]")


def grafico_pizza(coluna, nome_arquivo):
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

    plt.savefig(nome_arquivo)

    img = Image.open(nome_arquivo)

    return img
