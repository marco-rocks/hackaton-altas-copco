import pandas as pd

from .config import(
    ABA_FROTA,
    ABA_HISTORICO,
    CAMINHO_DADOS,
)

def carregar_historico() -> pd.DataFrame:
    """Carrega o histórico de cotações"""

    return pd.read_excel(
        CAMINHO_DADOS,
        sheet_name=ABA_HISTORICO
    )

def carregar_frota() -> pd.DataFrame:
    """Carrega os dados da frota de ativos"""

    return pd.read_excel(
        CAMINHO_DADOS,
        sheet_name=ABA_FROTA
    )

def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega todas as bases utilizadas na análise"""

    historico = carregar_historico()
    frota = carregar_frota()

    return historico, frota