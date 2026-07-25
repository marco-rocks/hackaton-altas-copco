from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plotar_desempenho_segmentos(
        segmentos: pd.DataFrame,
        win_rate_geral: float,
        tempo_medio_geral: float,
        caminho_saida: Path
) -> None:
    """Gera o gráfico de desempenho comercial dos segmentos"""

    plt.figure(figsize=(10,6))

    plt.scatter(
        segmentos["Tempo_Medio_Dias"],
        segmentos["Win_Rate"],
        s = 140
    )

    for segmento, indicadores in segmentos.iterrows():
        plt.annotate(
            segmento,
            (
                indicadores["Tempo_Medio_Dias"],
                indicadores["Win_Rate"]
            ),
            xytext= (5, 5),
            textcoords = "offset points"
        )

    plt.axvline(
        tempo_medio_geral,
        linestyle = "--",
        label = "Tempo médio geral",
    )

    plt.axhline(
        win_rate_geral,
        linestyle = "--",
        label = "Win Rate Geral"
    )

    plt.title("Desempenho Comercial por Segmento")
    plt.xlabel("Tempo Médio de Fechamento (dias)")
    plt.ylabel("Win Rate (%)")
    plt.legend()
    plt.tight_layout()

    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        caminho_saida,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plotar_contribuicao_modelos(
        analise_modelos: pd.DataFrame,
        caminho_saida: Path
) -> None:
    """Gera o gráfico de contribuição aproximada por modelo"""

    dados_grafico = analise_modelos.reset_index()

    plt.figure(figsize=(9,5))

    sns.barplot(
        data=dados_grafico,
        x = "F1_Model",
        y = "Contribuicao_Aproximada"
    )

    plt.axhline(
        0,
        linestyle = "--",
        linewidth = 1
    )

    
    plt.title("Contribuição Aproximada por Modelo")
    plt.xlabel("Modelo")
    plt.ylabel("Contribuição aproximada (R$)")

    plt.gca().yaxis.set_major_formatter(
            lambda valor, _: f"R$ {valor:,.0f}"
    )

    plt.tight_layout()

    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        caminho_saida,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()