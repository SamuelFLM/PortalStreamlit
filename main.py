import streamlit as st
from utilidades import *
from views.base import *
from views.colaborador import *
from views.painel import *
from views.historico import *


@st.cache_data()
def carregar_dados(arquivo):
    df_data = pd.read_excel(arquivo, engine="openpyxl", sheet_name="LISTA")
    return df_data


if __name__ == "__main__":
    st.set_page_config("Portal", layout="wide")
    with st.sidebar:
        with st.expander("Base De Migração"):
            base_de_migracao = st.file_uploader(
                "Anexar Base De Migração", type=["xlsx"], key="unique_key_1"
            )

    if base_de_migracao is not None:

        iniciar_dados(carregar_dados(base_de_migracao))

        with st.expander("Menu", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.button(
                "Painel De Migração",
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

        if st.session_state["pagina_central"] == "pag_home":
            painel()

        elif st.session_state["pagina_central"] == "pag_base_migracao":
            base_migracao()

        elif st.session_state["pagina_central"] == "pag_colaborador":
            colaborador()

        elif st.session_state["pagina_central"] == "pag_historico":
            historico()
