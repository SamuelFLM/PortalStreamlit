import streamlit as st
import pandas as pd
from utilidades import *


def painel_redea():
    st.markdown("##### Painel :green[REDEA]")
    with st.expander("Base Controle De Reparo"):
        controle_de_reparo = st.file_uploader(
            "Anexar Base Controle De Reparo",
            type=["xlsx"],
            key="unique_key_2",
        )

    if controle_de_reparo is not None:
        df_reparos = pd.read_excel(
            controle_de_reparo, engine="openpyxl", sheet_name="Resultado"
        )
