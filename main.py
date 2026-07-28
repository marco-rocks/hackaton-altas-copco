from src.analise_comercial import (
    analisar_segmentos,
    calcular_indicadores_gerais,
    identificar_oportunidades
)

from src.analise_rentabilidade import(
    analisar_modelos_cliente,
    calcular_cobertura_frota,
    integrar_frota,
    obter_dados_clientes
)

from src.carregamento import carregar_dados

from src.config import(
    CLIENTE_ALVO,
    DIRETORIO_FIGURA,
    DIRETORIO_TABELAS
)

from src.exportacao import exportar_tabela
from src.preprocessamento import preparar_historico
from src.visualizacao import(
    plotar_contribuicao_modelos,
    plotar_desempenho_segmentos
)

def main() -> None:
    """Executa o pipeline completo da análise"""

    historico, frota = carregar_dados()

    # Missão 1 - Limpeza e estruturação
    historico = preparar_historico(historico)

    # Missão 2 - Oportunidades comerciais
    indicadores_gerais = calcular_indicadores_gerais(historico)

    segmentos = analisar_segmentos(historico)

    oportunidades = identificar_oportunidades(historico)

    # Missão 3 - Fator multiplicador
    cobertura_frota = calcular_cobertura_frota(historico, frota)
    base_integrada = integrar_frota(historico, frota)

    dados_cliente = obter_dados_clientes(
        base_integrada,
        CLIENTE_ALVO
    )

    modelos_cliente = analisar_modelos_cliente(dados_cliente)

    # Exportação das tabelas
    exportar_tabela(
        segmentos,
        DIRETORIO_TABELAS / "desempenho_segmentos.csv",
        incluir_indice = True
    )

    exportar_tabela(
        oportunidades,
        DIRETORIO_TABELAS / "oportunidades_clientes.csv"
    )

    exportar_tabela(
        modelos_cliente,
        DIRETORIO_TABELAS / "mix_cliente_alvo.csv",
        incluir_indice = True
    )

    # Geração de gráficos
    plotar_desempenho_segmentos(
        segmentos = segmentos,
        win_rate_geral = indicadores_gerais["win_rate"],
        tempo_medio_geral = (
            indicadores_gerais["tempo_medio_fechamento"]
        ),
        caminho_saida = (DIRETORIO_FIGURA / "desempenho_segmentos.png")
    )

    plotar_contribuicao_modelos(
        analise_modelos = modelos_cliente,
        caminho_saida = (
            DIRETORIO_FIGURA / "contribuicao_modelos.png"
        )
    )

    exibir_resumo(
        indicadores_gerais,
        cobertura_frota,
        segmentos,
        oportunidades,
        modelos_cliente,
    )

def exibir_resumo(
        indicadores_gerais: dict,
        cobertura_frota: dict,
        segmentos,
        oportunidades,
        modelos_cliente
) -> None:
    """Exibe os princpais resultados da análise"""

    print("\n===INDICADORES GERAIS===")
    print(
        f"Win Rate geral: "
        f"{indicadores_gerais['win_rate']:.2f}%"
    )

    print(
        f"Tempo médio de fechamento: "
        f"{indicadores_gerais['tempo_medio_fechamento']:.2f} dias"
    )

    print("\n=== COBERTURA DA FROTA ===")

    print(
        f"Cobertura das cotações: "
        f"{cobertura_frota['cobertura_cotacoes']:.2f}%"
    )

    print("\n=== DESEMPENHO DOS SEGMENTOS ===")
    print(segmentos)

    print("\n=== OPORTUNIDADES ===")
    print(oportunidades)

    print("\n=== MIX DO CLIENTE ALVO ===")
    print(modelos_cliente)

if __name__ == "__main__":
    main()