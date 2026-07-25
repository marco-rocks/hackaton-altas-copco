import pandas as pd

from .config import MINIMO_PROPOSTAS_CLIENTE
from .metricas import calcular_win_rate

def calcular_indicadores_gerais(historico: pd.DataFrame) -> dict[str, float]:
    """Calcula os principais indicadores comerciais da operação"""

    return{
        "total_propostas": historico["Quote_ID"].nunique(),
        "total_clientes": historico["Client_Name"].nunique(),
        "win_rate": calcular_win_rate(historico["Stage"]),
        "tempo_medio_fechamento": (
            historico["Days_To_Close"].mean()
        ),
    }

def analisar_segmentos(historico: pd.DataFrame,) -> pd.DataFrame:
    """Calcula os indicadores comerciais por segmento."""

    return (
        historico
        .groupby("Segmento")
        .agg(
            Quantidade_Propostas=("Quote_ID", "count"),
            Tempo_Medio_Dias=("Days_To_Close", "mean"),
            Win_Rate=("Stage", calcular_win_rate),
        )
        .round(2)
        .sort_values(
            by=["Win_Rate", "Tempo_Medio_Dias"],
            ascending=[False, True],
        )
    )

def analisar_clientes(historico: pd.DataFrame) -> pd.DataFrame:
    """Calcula os indicadores dos clientes com volume relevante"""

    indicadores_clientes = (
        historico.groupby("Client_Name")
        .agg(
            Quantidade_Propostas = ("Quote_ID", "count"),
            Tempo_Medio_Dias = ("Days_To_Close", "mean"),
            Win_Rate = ("Stage", calcular_win_rate)
        )
        .round(2)
        .reset_index()
    )

    segmentos_clientes = (
        historico[
            ["Client_Name", "Segmento"]
        ]
        .drop_duplicates()
    )

    analise_clientes = indicadores_clientes.merge(
        segmentos_clientes,
        on = "Client_Name",
        how = "left",
        validate = "one_to_one"
    )

    return analise_clientes[
        analise_clientes["Quantidade_Propostas"] >= MINIMO_PROPOSTAS_CLIENTE
    ]

def identificar_oportunidades(historico: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica clientes com Win Rate superior e tempo de
    fechament inhferior aos indicadores gerais
    """

    indicadores_gerais = calcular_indicadores_gerais(historico)

    clientes = analisar_clientes(historico)

    oportunidades = clientes[
        (
            clientes["Win_Rate"] > indicadores_gerais["win_rate"]
        )
        & (
            clientes["Tempo_Medio_Dias"] < indicadores_gerais["tempo_medio_fechamento"]
        )
    ]

    return oportunidades.sort_values(
        by =  ["Win_Rate", "Tempo_Medio_Dias"],
        ascending = [False, True],
    )