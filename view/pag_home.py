import streamlit as st
from utilidades import *



def home():
    
    st.header("Portal De Operações - Dados B2B - Nova OI", divider='green')
    
    col1, col2, col3 = st.columns([0.4, 0.4, 0.4])
    _card(col1, "GEPREV" , "Descrição" , botao_desativado=False)
    _card(col2, "Pagina em desenvolvimento" , "Descrição" , botao_desativado=True) 
    _card(col3, "Página em desenvolvimento"  , "Descrição" , botao_desativado=True)
    

def _card(coluna , titulo , descricao , botao_desativado):
    coluna.divider()
    coluna.markdown(titulo)
    coluna.caption(descricao)
    coluna.button("Veja mais" ,type="primary", use_container_width=True, key=f'{coluna}' , disabled=botao_desativado)
    coluna.divider()    