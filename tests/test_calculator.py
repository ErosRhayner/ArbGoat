from src.arbitrage.calculator import calcular_lucro_bruto


def test_calcular_lucro_bruto():
    resultado = calcular_lucro_bruto(preco_compra=100000, preco_venda=101000, quantidade=0.01)
    assert resultado == 10.0
from src.arbitrage.calculator import (
    calcular_lucro_bruto,
    calcular_lucro_com_taxas,
    calcular_lucro_liquido,
    calcular_percentual_retorno,
)

def test_calcular_lucro_com_taxas():
    resultado = calcular_lucro_com_taxas(
        preco_compra=100000, preco_venda=101000, quantidade=0.01,
        taxa_compra=0.001, taxa_venda=0.0015
    )
    assert round(resultado, 3) == 7.485


def test_calcular_lucro_liquido():
    resultado = calcular_lucro_liquido(
        preco_compra=100000, preco_venda=101000, quantidade=0.01,
        taxa_compra=0.001, taxa_venda=0.0015, taxa_rede=2.0
    )
    assert round(resultado, 3) == 5.485


def test_calcular_percentual_retorno():
    resultado = calcular_percentual_retorno(
        preco_compra=100000, preco_venda=101000, quantidade=0.01,
        taxa_compra=0.001, taxa_venda=0.0015, taxa_rede=2.0
    )
    assert round(resultado, 3) == 0.548
from src.arbitrage.calculator import (
    calcular_lucro_bruto,
    calcular_lucro_com_taxas,
    calcular_lucro_liquido,
    calcular_percentual_retorno,
    calcular_spread_percentual,
)

def test_calcular_spread_percentual():
    resultado = calcular_spread_percentual(preco_compra=100000, preco_venda=101000)
    assert round(resultado, 2) == 1.0
from src.arbitrage.calculator import (
    calcular_lucro_bruto,
    calcular_lucro_com_taxas,
    calcular_lucro_liquido,
    calcular_percentual_retorno,
    calcular_spread_percentual,
    aplicar_slippage,
)

def test_aplicar_slippage():
    preco_compra_ajustado, preco_venda_ajustado = aplicar_slippage(
        preco_compra=100000, preco_venda=101000,
        slippage_compra=0.0005, slippage_venda=0.0005
    )
    assert round(preco_compra_ajustado, 2) == 100050.0
    assert round(preco_venda_ajustado, 2) == 100949.5
from src.arbitrage.calculator import (
    calcular_lucro_bruto,
    calcular_lucro_com_taxas,
    calcular_lucro_liquido,
    calcular_percentual_retorno,
    calcular_spread_percentual,
    aplicar_slippage,
    operacao_e_segura,
)

def test_operacao_e_segura_quando_retorno_e_bom():
    resultado = operacao_e_segura(
        preco_compra=100000, preco_venda=101000, quantidade=0.01,
        taxa_compra=0.001, taxa_venda=0.0015, taxa_rede=2.0,
        slippage_compra=0.0005, slippage_venda=0.0005,
        margem_minima=0.2
    )
    assert resultado == True


def test_operacao_nao_e_segura_quando_margem_muito_alta():
    resultado = operacao_e_segura(
        preco_compra=100000, preco_venda=101000, quantidade=0.01,
        taxa_compra=0.001, taxa_venda=0.0015, taxa_rede=2.0,
        slippage_compra=0.0005, slippage_venda=0.0005,
        margem_minima=5.0
    )
    assert resultado == False