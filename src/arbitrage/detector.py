from src.exchanges.binance import buscar_preco as buscar_preco_binance
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget
from src.arbitrage.calculator import calcular_percentual_retorno, calcular_lucro_liquido, aplicar_slippage


def detectar_oportunidade(par_binance: str, par_bitget: str, quantidade: float,
                           taxa_compra: float, taxa_venda: float, taxa_rede: float,
                           slippage_compra: float, slippage_venda: float,
                           margem_minima: float) -> dict:
    """
    Busca precos reais na Binance e na Bitget, descobre onde esta mais barato
    e mais caro, aplica o slippage estimado, e avalia se a operacao e segura.

    Todos os valores no resultado (percentual_retorno, lucro_liquido, operacao_segura)
    ja consideram o slippage aplicado.

    Retorna um dicionario com os detalhes da analise.
    """
    preco_binance = buscar_preco_binance(par_binance)
    preco_bitget = buscar_preco_bitget(par_bitget)

    preco_compra_bruto = min(preco_binance, preco_bitget)
    preco_venda_bruto = max(preco_binance, preco_bitget)

    if preco_compra_bruto == preco_binance:
        corretora_compra = "Binance"
        corretora_venda = "Bitget"
    else:
        corretora_compra = "Bitget"
        corretora_venda = "Binance"

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
    }
    return resultado