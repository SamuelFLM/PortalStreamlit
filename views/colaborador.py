import streamlit as st
from utilidades import *

colunas = [
    "Em execução",
    "Migração Concluída",
    "Cotar Terceiros",
    "Aguardando Abertura OS",
    "Migração Suspensa",
    "Em análise",
    "Impedimento Clarify",
    "Aprovar Contratação OEMP",
    "Histórico/ Em retirada",
]


def colaborador(df):
    df_metas = st.session_state["dados_metas"]

    col_colaborador, col_data, col3 = st.columns([0.3, 0.3, 1])
    colaborador, df_colaborador = _filtro_colaborador(df, col_colaborador)
    data_conclusao = col_data.selectbox(
        "Migração concluída Mês", ["Selecione", "01/2024", "02/2024"]
    )

    if colaborador == "Selecione":
        df_atual = df
    else:
        df_atual = df_colaborador
    total_filtro_status = len(df_atual["STATUS DETALHADO"])

    uf_metas = st.empty()
    total_metas = _filtro_metas_total(df_metas, colaborador)
    status_em_execução = _filtro_status(df_atual, colunas[0].upper())
    status_migracao_concluida = _filtro_status(df_atual, colunas[1].upper())
    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]

    if data_conclusao == "Selecione":
        valor_migracao_mes = 0
    else:
        valor = status_migracao_concluida[
            status_migracao_concluida["MÊS CONCLUSÃO"] == data_conclusao
        ]
        valor_migracao_mes = valor["MÊS CONCLUSÃO"].value_counts().iloc[0]

    if uf_metas.empty:
        if colaborador == "Selecione":
            valor_meta = 1000
        else:
            valor_meta = total_metas
    else:
        valor_meta = int(uf_metas.iloc[0])

    container_principal(
        [
            "Total",
            "Em execução",
            "Meta Acumulada",
            "Migração concluída Acumulada",
            "Meta Mês",
            "Migração concluída Mês",
        ],
        [
            total_filtro_status,
            len(status_em_execução),
            2000,
            len(status_migracao_concluida),
            valor_meta,
            valor_migracao_mes,
        ],
        ["orange", "red", "blue", "green", "blue", "green"],
    )
    detalhes, controle_de_reparo, tabela_filtrada = st.tabs(
        ["Detalhes", "Controle De Reparo", "Tabela"]
    )
    with detalhes:
        contagem_un, contagem_operacao = _contagem_os(df_status)
        col1, col2 = st.columns([0.8, 0.4])
        _container_status_detalhado(
            df_atual,
            col1,
            colunas,
        )
        try:
            if contagem_operacao.empty:
                valor = 0
            else:
                valor = str(contagem_operacao.iloc[0])
            container_aguard_os_detalhado(
                col2,
                ["UN", "OPERAÇÃO"],
                [
                    str(contagem_un.iloc[0]),
                    valor,
                ],
            )
        except:
            pass

    with controle_de_reparo:
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
            col1, col2, col3, col4 = st.columns(4)

            if colaborador == "Selecione":
                contem = df_reparos[df_reparos["Leonam_2024"] == "Sim"][
                    "Leonam_2024"
                ].value_counts()
                nao_contem = df_reparos[df_reparos["Leonam_2024"] == "Não"][
                    "Leonam_2024"
                ].value_counts()
                _controle_de_reparo(col1,col2,col3,col4,nao_contem,contem,"26 fev")
            else:
                df_atual_reparos = df_reparos[df_reparos["Colaborador"] == colaborador]

                contem = df_atual_reparos[df_atual_reparos["Leonam_2024"] == "Sim"][
                    "Leonam_2024"
                ].value_counts()
                nao_contem = df_atual_reparos[df_atual_reparos["Leonam_2024"] == "Não"][
                    "Leonam_2024"
                ].value_counts()
                _controle_de_reparo(col1,col2,col3,col4,nao_contem,contem,"26 fev")
                
                

    with tabela_filtrada:

        base_mes_meta = _base_mes_meta(df_atual, valor_meta)

        if colaborador != "Selecione":
            col1, col_filtro, col3, col4 = st.columns([0.2, 0.2, 0.4, 0.4])
            mes = col1.selectbox("Mês", ["Selecione", "01/2024", "02/2024"])

            df_mes = df_colaborador[df_colaborador["MÊS CONCLUSÃO"] == mes]
            col1, col2, col3 = st.columns([0.8, 0.8, 0.3])
            
            col1.dataframe(base_mes_meta, hide_index=True,)
            df_metas_filtro_colaborador = df_metas[
                df_metas["Colaborador"] == colaborador.title()
            ]
            if mes != "Selecione":
                farol = col_filtro.selectbox("Farol", ["Selecione", "🟢", "🔴"])
                tabela_metas_colaborador(
                    df_mes, df_metas_filtro_colaborador, col2, farol
                )
        else:
            st.info("Selecione um colaborador")


def _controle_de_reparo(col1, col2,col3,col4, nao_contem, contem, data):
    with col1.container(border=True):
                    st.markdown("Não Contem na base de migração")
                    st.markdown(f"## :red[{nao_contem.iloc[0]}]")

    with col2.container(border=True):
                    st.markdown("Contem na base de migração")
                    st.markdown(f"## :green[{contem.iloc[0]}]")

    with col3.container(border=True):
                    st.markdown("Total")
                    st.markdown(
                        f"## :blue[{int(contem.iloc[0]) + int(nao_contem.iloc[0])}]"
                    )
    col4.write(f"Base: {data}")


def _contagem_os(df_status):
    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()

    contagem_area_responsavel_operacao = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "OPERAÇÃO"
    ].value_counts()
    return contagem_area_responsavel_un, contagem_area_responsavel_operacao


def container_principal(titulos, valores, cores):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Loop através das colunass, títulos e valores
    for col, titulo, valor, cor in zip(
        [col1, col2, col3, col4, col5, col6], titulos, valores, cores
    ):
        with col.container(border=True):
            st.markdown(f"{titulo.title()}")
            st.write(f"### :{cor}[{str(valor)}]")


def _container_status_detalhado(df, col, titulos):

    with col.container():
        # Cria três linhas de colunass
        for i in range(3):
            cols = st.columns(3)

            # Loop através das colunass, títulos e valores
            for j in range(3):
                index = i * 3 + j
                with cols[j].container(border=True):
                    st.markdown(f"{titulos[index].title()}")

                    df_filtro_status = df[
                        df["STATUS DETALHADO"] == colunas[index].upper()
                    ]
                    st.write(f"#### :black[{len(df_filtro_status)}]")


def container_aguard_os_detalhado(coluna, titulos, valores):
    with coluna.container():
        col1, col2 = st.columns(2)
        # Loop através das colunass, títulos e valores
        for col, titulo, valor in zip([col1, col2], titulos, valores):
            with col.container(border=True):
                st.markdown("Aguardando Abertura OS")
                st.markdown(f"{titulo}")
                st.write(f"### :black[{str(valor)}]")


def _filtro_colaborador(df, colunas):
    colaboradores = list(df["RESPONSÁVEL NOVA OI"].unique())
    colaboradores.append("Selecione")
    colaborador = colunas.selectbox(
        "Colaborador", colaboradores, index=(len(colaboradores) - 1)
    )
    df_colaborador = df[df["RESPONSÁVEL NOVA OI"] == colaborador]

    return colaborador, df_colaborador


def _filtro_status(df, colunas):
    df_filtro_status = df[df["STATUS DETALHADO"] == colunas]
    return df_filtro_status


def _filtro_metas_total(df_metas, colaborador):
    df_filtro = df_metas[df_metas["Colaborador"] == colaborador.title()]["Meta"].sum()
    return df_filtro


def _base_mes_meta(df_atual, valor_meta):
    status = df_atual[df_atual["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]
    base = pd.DataFrame(
        {
            "Mês": status["MÊS CONCLUSÃO"].unique(),
            "Migração Concluída": status["MÊS CONCLUSÃO"].value_counts(),
            "Meta Mensal": valor_meta,
        }
    )

    base["Farol"] = base["Migração Concluída"].apply(
        lambda x: "🟢" if x >= valor_meta else "🔴"
    )
    base["Porcentagem"] = ((base["Migração Concluída"] / valor_meta) * 100).round(
        2
    ).astype(str) + " % "
    base = base.sort_values("Mês")
    return base

