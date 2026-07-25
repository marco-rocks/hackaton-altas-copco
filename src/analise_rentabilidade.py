import numpy as np
import pandas as pd

from .metricas import calcular_win_rate

def calcular_cobertura_frota(historico: pd.DataFrame, frota: pd.DataFrame) -> dict[str, float]:
    """Calcula a cobertura da frota sobre o histórico comercial"""

    seriais_historico = set(
        historico["Serial_ID"]
    )

    seriais_frota = set(
        frota["Serial_ID"]
    )

    seriais_em_comum = (
        seriais_historico.intersection(seriais_frota)
    )

    cotacoes_com_frota = historico[
        historico["Serial_ID"].isin(seriais_frota)
    ]

    return{
        "ativos_historico": len(seriais_historico),
        "ativos_frotas": len(seriais_frota),
        "ativos_em_comum": len(seriais_em_comum),
        "cobertura_ativos": (
            len(seriais_em_comum) / len(seriais_historico) * 100
        ),
        "cotacoes_com_frota": len(cotacoes_com_frota),
        "cobertura_cotacoes": (
            len(cotacoes_com_frota)/len(historico) * 100
        )    
    }

def integrar_frota(historico: pd.DataFrame, frota: pd.DataFrame) -> pd.DataFrame:
    """Integra o histórico comercial aos dados da frota"""

    _validar_chave_frota(frota)

    return historico.merge(
        frota,
        on = "Serial_ID",
        how = "inner",
        validate =  "many_to_one"
    )

def _validar_chave_frota(frota: pd.DataFrame) -> None:
    """Valida se cada Serial_ID identifica um único ativod"""

    if frota["Serial_ID"].duplicated().any():
        raise ValueError(
            "Foram encontrados Serial_ID duplicados "
            "na base de frota"
        )


def obter_dados_clientes(base_integrada: pd.DataFrame, cliente: str) -> pd.DataFrame:
    """Retorna os registros associados ao cliente informado"""

    dados_cliente = base_integrada[
        base_integrada["Client_Name"] == cliente
    ].copy()

    if dados_cliente.empty:
        raise ValueError(
            f"Nenhum registro encontrado para: {cliente}"
        )

    return dados_cliente

def analisar_modelos_cliente(
    dados_cliente: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compara o desempenho comercial e a manutenção
    dos modelos associados ao cliente.
    """

    desempenho_comercial = (
        _calcular_desempenho_comercial_modelos(
            dados_cliente
        )
    )

    custos_manutencao = (
        _calcular_manutencao_modelos(
            dados_cliente
        )
    )

    analise_modelos = desempenho_comercial.join(
        custos_manutencao
    )

    # Proxy financeira:
    # valor das propostas ganhas menos manutenção acumulada.
    analise_modelos["Contribuicao_Aproximada"] = (
        analise_modelos["Valor_Propostas_Ganhas"]
        - analise_modelos["Manutencao_Total"]
    )

    # Mede quanto a manutenção representa em relação
    # ao valor das propostas ganhas.
    analise_modelos["Razao_Manutencao_Receita"] = (
        analise_modelos["Manutencao_Total"]
        / analise_modelos["Valor_Propostas_Ganhas"]
        .replace(0, np.nan)
    )

    return analise_modelos.round(2)

def _calcular_desempenho_comercial_modelos(dados_cliente: pd.DataFrame) -> pd.DataFrame:
    """Calcula o desempenho comercial por modelo"""

    dados = dados_cliente.copy()

    dados["Valor_Proposta_Ganha"]  = np.where(
        dados["Stage"] == "Ganho",
        dados["Amount_BRL_Original"],
        0,
    )

    return(
        dados
        .groupby(
            ["Solution_Type", "F1_Model"]
        )
        .agg(
            Quantidade_Propostas = ("Quote_ID", "nunique"),
            Quantidade_Ativos = ("Serial_ID", "nunique"),
            Win_Rate = ("Stage", calcular_win_rate),
            Valor_Propostas_Ganhas = (
                "Valor_Proposta_Ganha",
                "sum"
            ),
        )

    )

def _calcular_manutencao_modelos(dados_cliente: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a manutenção acumulada por modelo sem
    duplicar o custo de um mesmo ativo
    """

    ativos_unicos = (
        dados_cliente
        .drop_duplicates(
            subset = [
                "Solution_Type",
                "F1_Model",
                "Serial_ID"
            ]
        )
    )

    return (
        ativos_unicos
        .groupby(
            ["Solution_Type", "F1_Model"]
        )
        .agg(
            Manutencao_Total = (
                "Total_Maintenance_Cost_BRL",
                "sum"
            )
        )
    )