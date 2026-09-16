
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.carregar_dados import (
    carregar_dados_gold,
    carregar_dados_historico,
)


st.set_page_config(
    page_title="Projeto Bets",
    page_icon="⚽",
    layout="wide",
)


NOMES_CAMPEONATOS = {
    "soccer_brazil_campeonato": "Brasileirão",
    "soccer_conmebol_copa_libertadores": "Libertadores",
    "soccer_conmebol_copa_sudamericana": "Sul-Americana",
}


df_gold = carregar_dados_gold()
df_historico = carregar_dados_historico()


if df_gold.empty:
    st.warning("Nenhum dado encontrado na camada Gold.")
    st.stop()


# =========================================================
# VERIFICA COLUNAS NECESSÁRIAS
# =========================================================

if "bookmaker_name" not in df_gold.columns:
    st.error(
        "A coluna 'bookmaker_name' não foi encontrada. "
        "Execute novamente o processamento da camada Gold."
    )
    st.stop()


df_gold["commence_time"] = pd.to_datetime(
    df_gold["commence_time"],
    errors="coerce",
    utc=True,
)

df_gold["commence_time"] = (
    df_gold["commence_time"]
    .dt.tz_convert("America/Sao_Paulo")
)


st.title("⚽ Projeto Bets")
st.caption("Dashboard de melhores odds do futebol")


# =========================================================
# FILTROS
# =========================================================

st.sidebar.header("🎯 Filtros")


campeonatos_disponiveis = sorted(
    df_gold["sport_key"].dropna().unique()
)


campeonato_selecionado = st.sidebar.selectbox(
    "Campeonato",
    options=["Todos"] + campeonatos_disponiveis,
    format_func=lambda valor: (
        "Todos"
        if valor == "Todos"
        else NOMES_CAMPEONATOS.get(valor, valor)
    ),
)


df_filtrado = df_gold.copy()


if campeonato_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["sport_key"]
        == campeonato_selecionado
    ]


times_disponiveis = sorted(
    set(df_filtrado["home_team"].dropna())
    | set(df_filtrado["away_team"].dropna())
)


time_selecionado = st.sidebar.selectbox(
    "Time",
    options=["Todos"] + times_disponiveis,
)


if time_selecionado != "Todos":
    df_filtrado = df_filtrado[
        (df_filtrado["home_team"] == time_selecionado)
        | (df_filtrado["away_team"] == time_selecionado)
    ]


bookmakers_disponiveis = sorted(
    df_filtrado["bookmaker_name"]
    .dropna()
    .unique()
)


bookmaker_selecionado = st.sidebar.selectbox(
    "Casa de aposta",
    options=["Todas"] + bookmakers_disponiveis,
)


if bookmaker_selecionado != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["bookmaker_name"]
        == bookmaker_selecionado
    ]


if df_filtrado.empty:
    st.warning(
        "Nenhum dado encontrado para os filtros selecionados."
    )
    st.stop()


# =========================================================
# PROBABILIDADE IMPLÍCITA
# =========================================================

df_filtrado = df_filtrado.copy()

df_filtrado["probabilidade"] = (
    1 / df_filtrado["best_odd"]
) * 100


# =========================================================
# MÉTRICAS
# =========================================================

todos_times = pd.concat(
    [
        df_filtrado["home_team"],
        df_filtrado["away_team"],
    ]
)


coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)


with coluna1:
    st.metric(
        "Jogos",
        df_filtrado["game_id"].nunique(),
    )


with coluna2:
    st.metric(
        "Times",
        todos_times.nunique(),
    )


with coluna3:
    st.metric(
        "Casas de aposta",
        df_filtrado["bookmaker_name"].nunique(),
    )


with coluna4:
    st.metric(
        "Resultados monitorados",
        len(df_filtrado),
    )


with coluna5:
    st.metric(
        "Maior odd",
        f"{df_filtrado['best_odd'].max():.2f}",
    )


with st.expander("🔍 Teste da Gold histórica"):
    st.write(
        f"Registros históricos: {len(df_historico)}"
    )

    if not df_historico.empty:
        st.dataframe(
            df_historico.head(20),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# TABELA
# =========================================================

st.subheader("💰 Melhores odds")


tabela = df_filtrado[
    [
        "commence_time",
        "home_team",
        "away_team",
        "outcome",
        "bookmaker_name",
        "best_odd",
        "probabilidade",
        "sport_key",
    ]
].copy()


tabela["sport_key"] = (
    tabela["sport_key"]
    .map(NOMES_CAMPEONATOS)
    .fillna(tabela["sport_key"])
)


tabela = tabela.rename(
    columns={
        "commence_time": "Data",
        "home_team": "Mandante",
        "away_team": "Visitante",
        "outcome": "Resultado",
        "bookmaker_name": "Casa de aposta",
        "best_odd": "Melhor odd",
        "probabilidade": "Probabilidade",
        "sport_key": "Campeonato",
    }
)


tabela = tabela.sort_values(
    by="Melhor odd",
    ascending=False,
)


tabela["Data"] = tabela["Data"].dt.strftime(
    "%d/%m/%Y %H:%M"
)


st.dataframe(
    tabela,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Melhor odd": st.column_config.NumberColumn(
            format="%.2f"
        ),
        "Probabilidade": st.column_config.NumberColumn(
            format="%.2f%%"
        ),
    },
)


# =========================================================
# TOP 10 MAIORES ODDS
# =========================================================

st.subheader("📊 Top 10 maiores odds")


top_10 = (
    df_filtrado[
        [
            "home_team",
            "away_team",
            "outcome",
            "bookmaker_name",
            "best_odd",
        ]
    ]
    .sort_values(
        by="best_odd",
        ascending=False,
    )
    .head(10)
    .copy()
)


top_10["Jogo"] = (
    top_10["home_team"]
    + " x "
    + top_10["away_team"]
)


top_10["Descrição"] = (
    top_10["Jogo"]
    + " — "
    + top_10["outcome"]
)


grafico = px.bar(
    top_10,
    x="best_odd",
    y="Descrição",
    orientation="h",
    text="best_odd",
    color="bookmaker_name",
    labels={
        "best_odd": "Melhor odd",
        "Descrição": "Jogo e resultado",
        "bookmaker_name": "Casa de aposta",
    },
    hover_data={
        "home_team": False,
        "away_team": False,
        "outcome": True,
        "bookmaker_name": True,
        "best_odd": ":.2f",
    },
    title="Maiores odds disponíveis",
)


grafico.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)


grafico.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    },
    height=500,
    legend_title_text="Casa de aposta",
)


st.plotly_chart(
    grafico,
    use_container_width=True,
)


# =========================================================
# MÉDIA POR CAMPEONATO
# =========================================================

st.subheader("🏆 Média das odds por campeonato")


media_campeonato = (
    df_filtrado
    .groupby(
        "sport_key",
        as_index=False,
    )
    .agg(
        media_odd=("best_odd", "mean"),
        quantidade_jogos=("game_id", "nunique"),
    )
)


media_campeonato["Campeonato"] = (
    media_campeonato["sport_key"]
    .map(NOMES_CAMPEONATOS)
    .fillna(media_campeonato["sport_key"])
)


grafico_campeonato = px.bar(
    media_campeonato,
    x="Campeonato",
    y="media_odd",
    text_auto=".2f",
    labels={
        "media_odd": "Média das odds",
        "Campeonato": "Campeonato",
    },
    hover_data={
        "quantidade_jogos": True,
        "sport_key": False,
    },
)


grafico_campeonato.update_layout(
    xaxis_title=None,
    yaxis_title="Média das odds",
)


st.plotly_chart(
    grafico_campeonato,
    use_container_width=True,
)


# =========================================================
# PARTIDAS EM DESTAQUE
# =========================================================

st.subheader("⚽ Partidas em destaque")


ids_proximos_jogos = (
    df_filtrado
    .dropna(subset=["commence_time"])
    .sort_values("commence_time")
    ["game_id"]
    .drop_duplicates()
    .head(10)
)


partidas = (
    df_filtrado[
        df_filtrado["game_id"].isin(ids_proximos_jogos)
    ]
    .sort_values(
        by="commence_time",
        ascending=True,
    )
)


partidas_agrupadas = partidas.groupby(
    [
        "game_id",
        "commence_time",
        "home_team",
        "away_team",
        "sport_key",
    ],
    as_index=False,
)


for _, grupo in partidas_agrupadas:

    jogo = grupo.iloc[0]

    campeonato = NOMES_CAMPEONATOS.get(
        jogo["sport_key"],
        jogo["sport_key"],
    )

    data_jogo = jogo["commence_time"].strftime(
        "%d/%m/%Y às %H:%M"
    )

    with st.container(border=True):

        st.markdown(
            f"### {jogo['home_team']} x {jogo['away_team']}"
        )

        st.caption(
            f"{campeonato} • {data_jogo}"
        )

        colunas_odds = st.columns(len(grupo))

        for coluna, (_, linha) in zip(
            colunas_odds,
            grupo.iterrows(),
        ):

            with coluna:

                st.metric(
                    label=linha["outcome"],
                    value=f"{linha['best_odd']:.2f}",
                )

                st.caption(
                    f"🏦 {linha['bookmaker_name']}"
                )


# =========================================================
# RANKING DAS CASAS DE APOSTA
# =========================================================

st.subheader("🏦 Ranking das casas de aposta")


ranking_bookmakers = (
    df_filtrado
    .groupby(
        "bookmaker_name",
        as_index=False,
    )
    .agg(
        quantidade_melhores_odds=(
            "best_odd",
            "count",
        ),
        media_odd=(
            "best_odd",
            "mean",
        ),
        maior_odd=(
            "best_odd",
            "max",
        ),
    )
    .sort_values(
        by="quantidade_melhores_odds",
        ascending=False,
    )
)


grafico_bookmakers = px.bar(
    ranking_bookmakers,
    x="quantidade_melhores_odds",
    y="bookmaker_name",
    orientation="h",
    text="quantidade_melhores_odds",
    labels={
        "quantidade_melhores_odds": "Quantidade de melhores odds",
        "bookmaker_name": "Casa de aposta",
        "media_odd": "Média das odds",
        "maior_odd": "Maior odd",
    },
    hover_data={
        "media_odd": ":.2f",
        "maior_odd": ":.2f",
    },
    title="Casas que mais ofereceram as melhores odds",
)


grafico_bookmakers.update_layout(
    yaxis={
        "categoryorder": "total ascending",
    },
    xaxis_title="Quantidade de melhores odds",
    yaxis_title=None,
    height=500,
)


grafico_bookmakers.update_traces(
    textposition="outside",
)


st.plotly_chart(
    grafico_bookmakers,
    use_container_width=True,
)



# =========================================================
# EVOLUÇÃO DAS ODDS
# =========================================================

st.subheader("📈 Evolução das odds")


if not df_historico.empty:

    # -----------------------------------------------------
    # CRIA NOME DO JOGO
    # -----------------------------------------------------

    df_historico["jogo"] = (
        df_historico["home_team"]
        + " x "
        + df_historico["away_team"]
    )

    jogos = (
        df_historico["jogo"]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )


    jogo_escolhido = st.selectbox(
        "Selecione um jogo",
        jogos,
    )


    # -----------------------------------------------------
    # FILTRA O JOGO
    # -----------------------------------------------------

    historico_jogo = df_historico[
        df_historico["jogo"] == jogo_escolhido
    ].copy()


    # -----------------------------------------------------
    # RESULTADOS DISPONÍVEIS
    # -----------------------------------------------------

    resultados_disponiveis = sorted(
        historico_jogo["outcome"]
        .dropna()
        .unique()
    )


    resultado_escolhido = st.selectbox(
        "Selecione o resultado",
        resultados_disponiveis,
    )


    historico_jogo = historico_jogo[
        historico_jogo["outcome"]
        == resultado_escolhido
    ].copy()


    # -----------------------------------------------------
    # CASAS DISPONÍVEIS
    # -----------------------------------------------------

    casas_disponiveis = sorted(
        historico_jogo["bookmaker_name"]
        .dropna()
        .unique()
    )


    casa_escolhida = st.selectbox(
        "Selecione a casa de aposta",
        ["Todas"] + casas_disponiveis,
    )


    # -----------------------------------------------------
    # FILTRO DA CASA
    # -----------------------------------------------------

    historico_grafico = historico_jogo.copy()


    if casa_escolhida != "Todas":

        historico_grafico = historico_grafico[
            historico_grafico["bookmaker_name"]
            == casa_escolhida
        ].copy()


    # -----------------------------------------------------
    # CONVERTE DATA
    # -----------------------------------------------------

    historico_grafico["coleta_em"] = pd.to_datetime(
        historico_grafico["coleta_em"],
        errors="coerce",
        utc=True,
    )


    historico_grafico["coleta_em"] = (
        historico_grafico["coleta_em"]
        .dt.tz_convert("America/Sao_Paulo")
    )


    historico_grafico = historico_grafico.sort_values(
        "coleta_em"
    )


    # -----------------------------------------------------
    # GRÁFICO
    # -----------------------------------------------------

    if not historico_grafico.empty:

        grafico_historico = px.line(
            historico_grafico,
            x="coleta_em",
            y="odd",
            color="bookmaker_name",
            markers=True,
            labels={
                "coleta_em": "Data da coleta",
                "odd": "Odd",
                "bookmaker_name": "Casa de aposta",
            },
            title=(
                f"{jogo_escolhido} — "
                f"{resultado_escolhido}"
            ),
        )


        grafico_historico.update_layout(
            xaxis_title="Data da coleta",
            yaxis_title="Odd",
            hovermode="x unified",
        )


        st.plotly_chart(
            grafico_historico,
            use_container_width=True,
        )


    # -----------------------------------------------------
    # VARIAÇÃO POR CASA
    # -----------------------------------------------------

    st.subheader("📊 Variação das odds por casa")


    historico_variacao = historico_jogo.copy()


    historico_variacao["coleta_em"] = pd.to_datetime(
        historico_variacao["coleta_em"],
        errors="coerce",
        utc=True,
    )


    historico_variacao = (
        historico_variacao
        .sort_values("coleta_em")
    )


    resumo_variacao = []


    for casa, grupo in historico_variacao.groupby(
        "bookmaker_name"
    ):

        grupo = grupo.sort_values(
            "coleta_em"
        )


        odd_inicial = grupo.iloc[0]["odd"]
        odd_atual = grupo.iloc[-1]["odd"]


        if odd_inicial:

            variacao = (
                (odd_atual - odd_inicial)
                / odd_inicial
            ) * 100

        else:

            variacao = 0


        resumo_variacao.append(
            {
                "Casa de aposta": casa,
                "Odd inicial": odd_inicial,
                "Odd atual": odd_atual,
                "Variação (%)": variacao,
                "Coletas": len(grupo),
            }
        )


    tabela_variacao = pd.DataFrame(
        resumo_variacao
    )


    if not tabela_variacao.empty:

        tabela_variacao = (
            tabela_variacao
            .sort_values(
                "Variação (%)",
                ascending=False,
            )
        )


        st.dataframe(
            tabela_variacao,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Odd inicial": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "Odd atual": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "Variação (%)": st.column_config.NumberColumn(
                    format="%.2f%%"
                ),
                "Coletas": st.column_config.NumberColumn(
                    format="%d"
                ),
            },
        )

else:

    st.info(
        "Não há dados históricos disponíveis."
    )
