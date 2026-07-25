from pathlib import Path

import pandas as pd

def exportar_tabela(
        tabela: pd.DataFrame,
        caminho: Path,
        *,
        incluir_indice: bool = False
) -> None:
    """Exporta uma tabela para CSV"""

    caminho.parent.mkdir(
        parents = True,
        exist_ok = True,
    )

    tabela.to_csv(
        caminho,
        index = incluir_indice
    )