import streamlit as st
from utilidades import *
from view.pag_home import *
from view.pag_base_migracao import *
from view.pag_colaborador import *
from view.pag_painel import *
from view.pag_historico import *
from time import sleep


def main(df):

    iniciar_dados(df)
    col1, col2 = st.columns([2, 0.1])

    with col1.expander("Menu", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.button(
            "Início",
            use_container_width=True,
            on_click=mudar_pagina,
            args=("pag_home",),
            type="primary",
        )
        col2.button(
            "Base De Migração",
            use_container_width=True,
            on_click=mudar_pagina,
            args=("pag_base_migracao",),
            type="primary",
        )
        col3.button(
            "Colaborador",
            use_container_width=True,
            on_click=mudar_pagina,
            args=("pag_colaborador",),
            type="primary",
        )
        col4.button(
            "Histórico",
            use_container_width=True,
            on_click=mudar_pagina,
            args=("pag_historico",),
            type="primary",
        )
        col5.button(
            "Painel De Migração",
            use_container_width=True,
            on_click=mudar_pagina,
            args=("pag_painel",),
            type="primary",
        )


    if st.session_state["pagina_central"] == "pag_home":
        home()

    elif st.session_state["pagina_central"] == "pag_base_migracao":
        base_migracao()

    elif st.session_state["pagina_central"] == "pag_colaborador":
        st.session_state["expandir"] = False
        colaborador()

    elif st.session_state["pagina_central"] == "pag_historico":
        historico()

    elif st.session_state["pagina_central"] == "pag_painel":
        painel()

@st.cache_data()
def carregar_dados(arquivo):
    df_data = pd.read_excel(arquivo, engine="openpyxl", sheet_name="LISTA")
    return df_data
    

if __name__ == "__main__":
    configuracao_pagina()
    col1, col2 = st.columns([0.2, 0.1])
    with col1.expander("Arquivo"):
        uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx'])
    
    if uploaded_file is not None:
        df = carregar_dados(uploaded_file)
        main(df)
    else:
        st.write("Por favor, carregue um arquivo para continuar.")
