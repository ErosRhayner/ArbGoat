from unittest.mock import patch
from src.arbitrage.detector import detectar_oportunidade


def test_detectar_oportunidade_com_precos_simulados():
    with patch("src.arbitrage.detector.buscar_preco_binance", return_value=100.0), \
         patch("src.arbitrage.detector.buscar_preco_bitget", return_value=101.0):

        resultado = detectar_oportunidade(
            par_binance="TESTE",
            par_bitget="TESTE",
            quantidade=10,
            taxa_compra=0.001,
            taxa_venda=0.001,
            taxa_rede=0.01,
            slippage_compra=0.0,
            slippage_venda=0.0,
            margem_minima=0.1
        )

    assert resultado["corretora_compra"] == "Binance"
    assert resultado["corretora_venda"] == "Bitget"
    assert resultado["preco_compra"] == 100.0
    assert resultado["preco_venda"] == 101.0