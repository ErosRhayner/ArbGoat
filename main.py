print("ArbGoat iniciado!")
print("Versão: 0.0.1")
print("Status: Em desenvolvimento")
from src.arbitrage.calculator import calcular_lucro_bruto

lucro = calcular_lucro_bruto(preco_compra=100000, preco_venda=101000, quantidade=0.01)
print("Lucro bruto de teste:", lucro)