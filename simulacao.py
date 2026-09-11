import time
import requests
from src.arbitrage.detector import detectar_oportunidade
from src.data.registro import registrar_oportunidade

print("Simulacao iniciada. Pressione Ctrl+C para parar.")

while True:
    try:
        oportunidade = detectar_oportunidade(
            par_binance="USDTBRL",
            par_bitget="USDTBRL",
            quantidade=1000,
            taxa_compra=0.001,
            taxa_venda=0.0015,
            taxa_rede=2.0,
            slippage_compra=0.0005,
            slippage_venda=0.0005,
            margem_minima=0.1
        )

        registrar_oportunidade(oportunidade)
        print(oportunidade)

    except requests.exceptions.RequestException as erro:
        print("Falha ao buscar dados de uma corretora, tentando novamente no proximo ciclo:", erro)

    time.sleep(30)