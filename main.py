print("ArbGoat iniciado!")
print("Versão: 0.0.1")
print("Status: Em desenvolvimento")
from src.arbitrage.calculator import calcular_lucro_bruto

lucro = calcular_lucro_bruto(preco_compra=100000, preco_venda=101000, quantidade=0.01)
print("Lucro bruto de teste:", lucro)
from src.arbitrage.calculator import calcular_lucro_com_taxas

lucro_liquido_teste = calcular_lucro_com_taxas(
    preco_compra=100000,
    preco_venda=101000,
    quantidade=0.01,
    taxa_compra=0.001,
    taxa_venda=0.0015
)
print("Lucro com taxas de teste:", lucro_liquido_teste)
from src.arbitrage.calculator import calcular_lucro_liquido

lucro_final_teste = calcular_lucro_liquido(
    preco_compra=100000,
    preco_venda=101000,
    quantidade=0.01,
    taxa_compra=0.001,
    taxa_venda=0.0015,
    taxa_rede=2.0
)
print("Lucro liquido de teste:", lucro_final_teste)