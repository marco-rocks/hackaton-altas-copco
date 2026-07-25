import pandas as pd

MAPEAMENTO_STAGE = {
    "ganho": "Ganho",
    "won": "Ganho",
    "w0n": "Ganho",
    "perdido": "Perdido",
    "lost": "Perdido",
    "not won": "Perdido"
}

def converter_datas(historico: pd.DataFrame) -> pd.DataFrame:
    """Converte as colunas de data para o tipo datetime"""

    resultado = historico.copy()

    resultado["Quote_Date"] = pd.to_datetime(
        resultado["Quote_Date"],
        format = "mixed",
        dayfirst = True,
        errors = "raise"
    )
        

    resultado["Close_Date"] = pd.to_datetime(
        resultado["Close_Date"],
        errors = "raise"
    )

    return resultado

def recuperar_dias_fechamento(historico: pd.DataFrame) -> pd.DataFrame:
    """Recupera valores ausentes de Days_ToClose"""

    resultado = historico.copy()

    dias_calculados = (
        resultado["Close_Date"] - resultado["Quote_Date"]
    ).dt.days

    resultado["Days_To_Close"] = (
        resultado["Days_To_Close"]
        .fillna(dias_calculados)
        .astype(int)
    )

    return resultado

def padronizar_estagio(historico: pd.DataFrame) -> pd.DataFrame:
    """Padroniza os valores de Stage em Ganho e Perdido"""

    resultado = historico.copy()

    estagio_normalizado = (
        resultado["Stage"]
        .str.strip()
        .str.lower()
    )

    resultado["Stage"] = estagio_normalizado.replace(
        MAPEAMENTO_STAGE
    )

    _validar_estagios(resultado)

    return resultado

def _validar_estagios(historico: pd.DataFrame) -> None:
    """Valida se Stage contém apenas categorias reconhecidas"""

    estagios_validos = {"Ganho", "Perdido"}

    estagios_encontrados = set(
        historico["Stage"]
        .dropna()
        .unique()
    )

    estagios_invalidos = (
        historico["Stage"]
        .dropna()
        .unique()
    )

    estagios_invalidos = (
        estagios_encontrados - estagios_validos
    )

    if estagios_invalidos:
        raise ValueError(
            "Foram encontrados valores inválidos em Stage: "
            f"{estagios_invalidos}"
        )

def adicionar_valor_winsorizado(historico: pd.DataFrame) -> pd.DataFrame:
    """
    Preserva o valor original e adiciona uma versão Winsorizada de Amount_BRL
    """

    resultado = historico.copy()

    resultado["Amount_BRL_Original"] = (
        resultado["Amount_BRL"]
    )

    limite_inferior, limite_superior = (
        _calcular_limites_iqr(
            resultado["Amount_BRL"]
        )
    )

    resultado["Amount_BRL_Tratado"] = (
        resultado["Amount_BRL"]
        .clip(
            lower = limite_inferior,
            upper= limite_superior
        )
    )

    return resultado

def _calcular_limites_iqr(serie: pd.Series) -> tuple[float, float]:
    """Calcula os limites inferior e superior pelos métodos de IQR"""

    primeiro_quartil = serie.quantile(0.25)
    terceiro_quartil = serie.quantile(0.75)

    intervalo_interquartil = (
        terceiro_quartil - primeiro_quartil
    )

    limite_inferior = (
        primeiro_quartil - 1.5 * intervalo_interquartil
    )

    limite_superior = (
        terceiro_quartil + 1.5 * intervalo_interquartil
    )

    return limite_inferior, limite_superior

def adicionar_segmento(historico: pd.DataFrame) -> pd.DataFrame:
    """Adiciona o segmento comercial de cada cliente"""

    resultado = historico.copy()

    resultado["Segmento"] = (
        resultado["Client_Name"]
        .apply(_extrair_segmento)
    )

    return resultado

def _extrair_segmento(nome_cliente: str) -> str:
        """Extrai o segmento presente do nome do cliente"""

        partes_nome = nome_cliente.split()

        if len(partes_nome) < 3:
            raise ValueError(
                "Nome de cliente fora do padrão esperado"
                f"{nome_cliente}"
            )

        return " ".join(partes_nome[1:-1])

def preparar_historico(historico: pd.DataFrame) -> pd.DataFrame:
    "Executa o pipeline completo de preparação do histórico"

    resultado = converter_datas(historico)
    resultado = recuperar_dias_fechamento(resultado)
    resultado = padronizar_estagio(resultado)
    resultado = adicionar_valor_winsorizado(resultado)
    resultado = adicionar_segmento(resultado)

    return resultado