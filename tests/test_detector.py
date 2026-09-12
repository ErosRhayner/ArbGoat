from unittest.mock import patch
from src.arbitrage.detector import detectar_oportunidade


def test_detectar_oportunidade_com_precos_simulados():
    precos_falsos = {
        "Binance": 100.0,
        "Bitget": 101.0,
        "MEXC": 99.0,
    }

    with patch("src.arbitrage.detector.buscar_precos_todas_corretoras", return_value=precos_falsos):
        resultado = detectar_oportunidade(
            par="TESTE",
            quantidade=10,
            taxa_compra=0.001,
            taxa_venda=0.001,
            taxa_rede=0.01,
            slippage_compra=0.0,
            slippage_venda=0.0,
            margem_minima=0.1
        )

    assert resultado["corretora_compra"] == "MEXC"
    assert resultado["corretora_venda"] == "Bitget"
    assert resultado["preco_compra"] == 99.0
    assert resultado["preco_venda"] == 101.0