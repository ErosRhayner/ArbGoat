from src.exchanges.binance import buscar_preco as buscar_preco_binance
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget
from src.arbitrage.calculator import operacao_e_segura, calcular_percentual_retorno


def detectar_oportunidade(par_binance: str, par_bitget: str, quantidade: float,
                           taxa_compra: float, taxa_venda: float, taxa_rede: float,
                           slippage_compra: float, slippage_venda: float,
                           margem_minima: float) -> dict:
    """
    Busca precos reais na Binance e na Bitget, descobre onde esta mais barato
    e mais caro, e avalia se a operacao de arbitragem e segura.

    Retorna um dicionario com os detalhes da analise.
    """
    preco_binance = buscar_preco_binance(par_binance)
    preco_bitget = buscar_preco_bitget(par_bitget)

    preco_compra = min(preco_binance, preco_bitget)
    preco_venda = max(preco_binance, preco_bitget)

    if preco_compra == preco_binance:
        corretora_compra = "Binance"
        corretora_venda = "Bitget"
    else:
        corretora_compra = "Bitget"
        corretora_venda = "Binance"

    percentual_retorno = calcular_percentual_retorno(
        preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede
    )

    e_segura = operacao_e_segura(
        preco_compra, preco_venda, quantidade,
        taxa_compra, taxa_venda, taxa_rede,
        slippage_compra, slippage_venda, margem_minima
    )

    resultado = {
        "corretora_compra": corretora_compra,
        "corretora_venda": corretora_venda,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "percentual_retorno": percentual_retorno,
        "operacao_segura": e_segura,
    }
    return resultado