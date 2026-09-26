import time
import requests
import winsound
from src.arbitrage.detector import detectar_oportunidade
from src.data.registro import registrar_oportunidade
from src.data.carteira import carregar_saldo, atualizar_saldo

# Quantidade de cada par equivalente a aproximadamente R$1.000 investidos
# USDT/BRL: R$1.000 / R$5.18 = ~193 unidades
# USDC/BRL: R$1.000 / R$5.18 = ~193 unidades
# BTC/BRL:  R$1.000 / R$440.000 = ~0.00227 BTC
# ETH/BRL:  R$1.000 / R$14.000 = ~0.07143 ETH
PARES_MONITORADOS = {
    "USDTBRL": 193,
    "USDCBRL": 193,
    "BTCBRL": 0.00227,
    "ETHBRL": 0.07143,
}

print("Simulacao iniciada. Pressione Ctrl+C para parar.")
print("Pares monitorados:", list(PARES_MONITORADOS.keys()))
print("Saldo inicial da carteira:", carregar_saldo())
print("Valor simulado por par: ~R$1.000")

while True:
    for par, quantidade in PARES_MONITORADOS.items():
        try:
            oportunidade = detectar_oportunidade(
                par=par,
                quantidade=quantidade,
                taxa_compra=0.001,
                taxa_venda=0.0015,
                taxa_rede=2.0,
                slippage_compra=0.0005,
                slippage_venda=0.0005,
                margem_minima=0.1
            )

            oportunidade["par"] = par
            foi_registrado = registrar_oportunidade(oportunidade)

            if foi_registrado:
                print(oportunidade)
            else:
                print(f"{par}: preco sem mudanca, nao registrado.")

            if oportunidade["operacao_segura"]:
                novo_saldo = atualizar_saldo(oportunidade["lucro_liquido"])
                print("Operacao executada (simulada)! Novo saldo:", novo_saldo)
                print("!!! OPORTUNIDADE SEGURA ENCONTRADA !!!")
                winsound.Beep(1000, 300)
                winsound.Beep(1500, 300)
                winsound.Beep(1000, 300)

        except (requests.exceptions.RequestException, ValueError) as erro:
            print(f"Falha ao analisar o par {par}, tentando novamente no proximo ciclo:", erro)

    time.sleep(30)