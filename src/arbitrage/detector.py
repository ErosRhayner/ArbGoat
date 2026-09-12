from src.exchanges.binance import buscar_preco as buscar_preco_binance
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget
from src.exchanges.mexc import buscar_preco as buscar_preco_mexc
from src.arbitrage.calculator import calcular_percentual_retorno, calcular_lucro_liquido, aplicar_slippage


CORRETORAS = {
    "Binance": buscar_preco_binance,
    "Bitget": buscar_preco_bitget,
    "MEXC": buscar_preco_mexc,
}


def buscar_precos_todas_corretoras(par: str) -> dict:
    """
    Busca o preco atual de um par em todas as corretoras cadastradas em CORRETORAS.
    Retorna um dicionario no formato {nome_da_corretora: preco}.
    """
    precos = {}
    for nome, funcao_buscar_preco in CORRETORAS.items():
        precos[nome] = funcao_buscar_preco(par)
    return precos


def detectar_oportunidade(par: str, quantidade: float,
                           taxa_compra: float, taxa_venda: float, taxa_rede: float,
                           slippage_compra: float, slippage_venda: float,
                           margem_minima: float) -> dict:
    """
    Busca precos reais em todas as corretoras cadastradas, encontra a rota
    com maior spread bruto (menor preco de compra, maior preco de venda),
    aplica slippage, e avalia se a operacao e segura.

    Retorna um dicionario com os detalhes da melhor rota encontrada.
    """
    precos = buscar_precos_todas_corretoras(par)

    corretora_compra = min(precos, key=precos.get)
    corretora_venda = max(precos, key=precos.get)

    preco_compra_bruto = precos[corretora_compra]
    preco_venda_bruto = precos[corretora_venda]

    preco_compra, preco_venda = aplicar_slippage(
        preco_compra_bruto, preco_venda_bruto, slippage_compra, slippage_venda
    )

    percentual_retorno = calcular_percentual_retorno(
        preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede
    )

    lucro_liquido = calcular_lucro_liquido(
        preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede
    )

    e_segura = percentual_retorno >= margem_minima

    resultado = {
        "corretora_compra": corretora_compra,
        "corretora_venda": corretora_venda,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "percentual_retorno": percentual_retorno,
        "lucro_liquido": lucro_liquido,
        "operacao_segura": e_segura,
        "precos_todas_corretoras": precos,
    }
    return resultado