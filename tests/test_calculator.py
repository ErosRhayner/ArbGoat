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