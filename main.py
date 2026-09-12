print("ArbGoat iniciado!")
print("Versão: 0.0.1")
print("Status: Em desenvolvimento")

from src.arbitrage.detector import detectar_oportunidade

print("--- Testando USDCBRL (Bitget deve ser ignorada) ---")
oportunidade_usdc = detectar_oportunidade(
    par="USDCBRL",
    quantidade=1000,
    taxa_compra=0.001,
    taxa_venda=0.0015,
    taxa_rede=2.0,
    slippage_compra=0.0005,
    slippage_venda=0.0005,
    margem_minima=0.1
)
print(oportunidade_usdc)