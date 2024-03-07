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

        df_redea = pd.DataFrame(
            {
                "PROTOCOLO": df_reparos["PROTOCOLO"],
                "PSR": df_reparos["PSR"],
                "REGIONAL": df_reparos["REGIONAL_VTAL"],
                "UF": df_reparos["FILIAL"],
                "CIRCUITO": df_reparos["CIRCUITO"],
                "CLIENTE": df_reparos["NOME_CLIENTE"],
                "POSTO": df_reparos["POSTO"],
                "FAIXA": df_reparos["TEMPO_ABERTURA"],
            }
        )

        tab1, tab2 = st.tabs(["Base", "Base Tratada"])

        with tab1:
            col1, col2, col3 = st.columns(3)
            
            psr, df_psr = filtro(df_redea, 'PSR',col1,"PSR")
            regional, df_regional = filtro(df_redea, 'REGIONAL',col2,"REGIONAL")
            faixa, df_faixa = filtro(df_redea, 'FAIXA',col3,"Faixa")
            df_atual = df_redea
            if psr != "Selecione":
                df_atual = df_psr
            if regional != "Selecione":
                df_atual = df_regional
            if faixa != "Selecione":
                df_atual = df_faixa
            
            
            st.dataframe(df_atual, hide_index=True)

        with tab2:
            
            contagem = df_redea.groupby(['PSR', 'REGIONAL', 'UF']).size()

            df_tratada = contagem.reset_index(name='TOTAL')
            
            col1, col2, col3 = st.columns(3)
            
            psr, df_psr = filtro(df_tratada, 'PSR',col1,"PSR")
            regional, df_regional = filtro(df_tratada, 'REGIONAL',col2,"REGIONAL")
            uf, df_uf = filtro(df_tratada, 'UF',col3,"UF")
            
            df_atual = df_tratada
            if psr != "Selecione":
                df_atual = df_psr
            if regional != "Selecione":
                df_atual = df_regional
            if uf != "Selecione":
                df_atual = df_uf
            
            
            st.dataframe(df_atual,width=600, hide_index=True)


def filtro(df, coluna_df, col_pag, nome_filtro):
    valores = list(df[coluna_df].unique())
    valores.append("Selecione")
    valor = col_pag.selectbox(nome_filtro, valores, index=(len(valores) - 1))
    df_filtrado = df[df[coluna_df] == valor]
    return valor, df_filtrado