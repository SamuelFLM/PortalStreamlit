import streamlit as st
from utilidades import *


def base_migracao():
    df = st.session_state["dados_excel"]
    
    
    st.markdown("## Base :green[De Migração]") 
    col1 ,col2 = st.columns([0.3,0.3])
    
    colaborador, df_colaborador  = _filtro_tabela(df,"RESPONSÁVEL NOVA OI", col1, "Colaborador")
    status, df_status = _filtro_tabela(df_colaborador,"STATUS DETALHADO", col2, "Status Detalhado")   
    
    st.divider() 

    tabela_atual = df
    if colaborador != "Selecione":
        tabela_atual = df_colaborador
        if status != "Selecione":
            tabela_atual = df_status
    else:
        tabela_atual = df
    st.dataframe(tabela_atual)


def _filtro_tabela(df,coluna_excel,posicao_tela, titulo_selectbox):
    valores_unicos = list(df[coluna_excel].unique())
    valores_unicos.append("Selecione")
    ultimo_index = len(valores_unicos) - 1
    valor = posicao_tela.selectbox(titulo_selectbox, valores_unicos, placeholder="Selecione",index=ultimo_index)
    df_filtrado = df[df[coluna_excel] == valor]
    return valor, df_filtrado


# with st.form("my_form"):
#     st.write("Inside the form")
#     slider_val = st.slider("Form slider")
#     checkbox_val = st.checkbox("Form checkbox")
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("slider", slider_val, "checkbox", checkbox_val)