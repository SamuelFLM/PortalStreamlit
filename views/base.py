import streamlit as st
from utilidades import *


def base_migracao():
    df = st.session_state["dados_excel"]
    tabela_atual = df

    st.markdown("##### Base :green[De Migração]")

    filtro1, filtro2 = st.columns(2)
    with filtro1.expander("Filtro"):
        col1, col2 = st.columns([0.3, 0.3])

        colaborador, df_colaborador = filtro_tabela(
            df, "RESPONSÁVEL NOVA OI", col1, "Colaborador"
        )
        status, df_status = filtro_tabela(
            df_colaborador, "STATUS DETALHADO", col2, "Status Detalhado"
        )
        
        col1, col2 = st.columns([0.3, 0.3])
        psrs = list(df_colaborador["PSR"].unique())
        psrs.append("Selecione")
        psr = col1.selectbox("PSR", psrs, index=(len(psrs) - 1))
        df_psr = df_colaborador[df_colaborador["PSR"] == psr]
        
        solucoes = list(df_colaborador["SOLUÇÃO PADRÃO"].unique())
        solucoes.append("Selecione")
        solucao = col2.selectbox("SOLUÇÃO PADRÃO".title(), solucoes, index=(len(solucoes) - 1))
        df_solucao_padrao = df_colaborador[df_colaborador["SOLUÇÃO PADRÃO"] == solucao]

    if colaborador != "Selecione":
        tabela_atual = df_colaborador
    if status != "Selecione":
        tabela_atual = df_status
    elif psr != "Selecione":
        tabela_atual = df_psr
    elif solucao != "Selecione":
        tabela_atual = df_solucao_padrao

    with filtro2.expander("Pesquisar"):
        st.markdown("Buscar por Circuito (LOTE)")
        st.caption("Lista de Dados (1 por linha) Ex.: GNA 0478965 ou RBO 0418279, RBO 0419313")
        circuito = st.text_area("")
        col1, col2, col3 = st.columns(3)
        btn = col1.button("Buscar", type="primary")
        limpar = col2.button("Limpar Filtro", type="primary")
        if btn:
            if circuito.strip():  # Verifique se o campo não está vazio
                circuitos_inseridos = [c.strip() for c in circuito.split("\n")]
                df_filtro = df[df["CIRCUITO"].isin(circuitos_inseridos)]
                if not df_filtro.empty:
                    tabela_atual = df_filtro
                else:
                    st.warning("Circuito não existe")
            else:
                st.warning("Insira um nome de circuito para buscar.")
        elif limpar:
            tabela_atual = df
    st.divider()

    st.dataframe(tabela_atual)


def filtro_tabela(df, coluna_excel, posicao_tela, titulo_selectbox):
    valores_unicos = list(df[coluna_excel].unique())
    valores_unicos.append("Selecione")
    ultimo_index = len(valores_unicos) - 1
    valor = posicao_tela.selectbox(
        titulo_selectbox, valores_unicos, placeholder="Selecione", index=ultimo_index
    )
    df_filtrado = df[df[coluna_excel] == valor]
    return valor, df_filtrado
