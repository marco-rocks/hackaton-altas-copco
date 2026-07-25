import pandas as pd

def calcular_win_rate(estagios: pd.Series) -> float:
    """Calcula o percentual de propostas ganhas"""

    return estagios.eq("Ganho").mean() * 100
