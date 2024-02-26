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


def colaborador():
    df = st.session_state["dados_excel"]
    df_metas = st.session_state["dados_metas"]
    df_reparos = st.session_state["dados_reparos"]

    selectbox_colaborador, selectbox_data, col3 = st.columns([0.3,0.3,0.5])
    colaborador, df_colaborador = _filtro_colaborador(df, selectbox_colaborador)

    if colaborador == "Selecione":
        df_atual = df
    else:
        df_atual = df_colaborador
    total_filtro_status = len(df_atual["STATUS DETALHADO"])

    st.subheader("", divider="green")

    uf_metas = st.empty()
    total_metas = _filtro_metas_total(df_metas, colaborador)
    status_em_execução = _filtro_status(df_atual, colunas[0].upper())
    status_migracao_concluida = _filtro_status(df_atual, colunas[1].upper())
    df_status = df_atual[(df_atual["STATUS DETALHADO"] == "AGUARDANDO ABERTURA OS")]

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
            "Total Migração concluída",
            "Meta Até Mês Recorrente",
            "Meta Mês Corrente",
        ],
        [
            total_filtro_status,
            len(status_em_execução),
            len(status_migracao_concluida),
            2000,
            valor_meta,
        ],
        ["orange", "red", "green", "blue", "blue"],
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

        col1, col2, col3, col4 = st.columns(4)
        colaborador_reparo = df_reparos[df_reparos["Colaborador_Oi"] == colaborador]
        contem = colaborador_reparo[colaborador_reparo["Leonam_2024"] == "Sim"][
            "Leonam_2024"
        ].value_counts()
        nao_contem = colaborador_reparo[colaborador_reparo["Leonam_2024"] == "Não"][
            "Leonam_2024"
        ].value_counts()
        if colaborador != "Selecione":
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
            col4.write("Base: 15 fev")
        else:
            st.info("Selecione um colaborador")

    with tabela_filtrada:

        base_mes_meta = _base_mes_meta(df_atual, valor_meta, colaborador)

        if colaborador != "Selecione":
            col1, col2, col3, col4 = st.columns(4)
            df_migracao = df[df["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]
            meses = list(df_migracao["MÊS CONCLUSÃO"].unique())
            meses.append("Selecione")
            mes = col1.selectbox("Mês", meses, index=(len(meses) - 1))

            df_mes = df_colaborador[df_colaborador["MÊS CONCLUSÃO"] == mes]
            col1, col2, col3 = st.columns([1, 0.9, 0.3])
            col1.dataframe(base_mes_meta, hide_index=True)
            df_metas_filtro_colaborador = df_metas[
                df_metas["Colaborador"] == colaborador.title()
            ]
            if mes != "Selecione":
                tabela_metas_colaborador(
                    df_mes, df_metas_filtro_colaborador, col2, col3
                )
        else:
            st.info("Selecione um colaborador")


def _contagem_os(df_status):
    contagem_area_responsavel_un = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "UN"
    ].value_counts()

    contagem_area_responsavel_operacao = df_status["ÁREA RESPONSÁVEL"][
        df_status["ÁREA RESPONSÁVEL"] == "OPERAÇÃO"
    ].value_counts()
    return contagem_area_responsavel_un, contagem_area_responsavel_operacao


def container_principal(titulos, valores, cores):
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    # Loop através das colunass, títulos e valores
    for col, titulo, valor, cor in zip(
        [col1, col2, col3, col4, col5], titulos, valores, cores
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
                st.markdown(f"{titulo.title()}")
                st.write(f"### :black[{str(valor)}]")


def _filtro_uf(df, colunas):
    filiais = list(df["FILIAL"].unique())
    filiais.append("Selecione")
    filial = colunas.selectbox("UF", filiais, index=(len(filiais) - 1), disabled=True)
    df_filial = df[df["FILIAL"] == filial]
    return filial, df_filial


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


def _filtro_metas(df_metas, filial):
    df_filtro = df_metas[df_metas["UF"] == filial]["Meta"]
    return df_filtro


def _base_mes_meta(df_atual, valor_meta, colaborador):
    status = df_atual[df_atual["STATUS DETALHADO"] == "MIGRAÇÃO CONCLUÍDA"]
    base = pd.DataFrame(
        {
            "Responsável": colaborador,
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
    return base
