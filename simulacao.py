import time
import requests
from src.arbitrage.detector import detectar_oportunidade
from src.data.registro import registrar_oportunidade
from src.data.carteira import carregar_saldo, atualizar_saldo

PARES_MONITORADOS = ["USDTBRL", "USDCBRL"]

print("Simulacao iniciada. Pressione Ctrl+C para parar.")
print("Pares monitorados:", PARES_MONITORADOS)
print("Saldo inicial da carteira:", carregar_saldo())

while True:
    for par in PARES_MONITORADOS:
        try:
            oportunidade = detectar_oportunidade(
                par=par,
                quantidade=1000,
                taxa_compra=0.001,
                taxa_venda=0.0015,
                taxa_rede=2.0,
                slippage_compra=0.0005,
                slippage_venda=0.0005,
                margem_minima=0.1
            )

            oportunidade["par"] = par
            registrar_oportunidade(oportunidade)
            print(oportunidade)

            if oportunidade["operacao_segura"]:
                novo_saldo = atualizar_saldo(oportunidade["lucro_liquido"])
                print("Operacao executada (simulada)! Novo saldo:", novo_saldo)

        except (requests.exceptions.RequestException, ValueError) as erro:
            print(f"Falha ao analisar o par {par}, tentando novamente no proximo ciclo:", erro)

    time.sleep(30)