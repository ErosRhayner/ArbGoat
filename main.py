print("ArbGoat iniciado!")
print("Versão: 0.0.1")
print("Status: Em desenvolvimento")
from src.exchanges.binance import buscar_preco

preco_usdt_brl = buscar_preco("USDTBRL")
print("Preco atual USDT/BRL na Binance:", preco_usdt_brl)
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget

preco_usdt_brl_bitget = buscar_preco_bitget("USDTBRL")
print("Preco atual USDT/BRL na Bitget:", preco_usdt_brl_bitget)
from src.arbitrage.detector import detectar_oportunidade

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
print("Resultado da analise:", oportunidade)
from src.data.registro import registrar_oportunidade

registrar_oportunidade(oportunidade)
print("Oportunidade registrada em src/data/historico_oportunidades.jsonl")
from src.data.carteira import carregar_saldo, atualizar_saldo

saldo = carregar_saldo()
print("Saldo inicial da carteira:", saldo)

novo_saldo = atualizar_saldo(50.0)
print("Saldo apos simular um lucro de R$50:", novo_saldo)
from src.utils.config import BINANCE_API_KEY

print("Chave da Binance carregada:", BINANCE_API_KEY)
from src.exchanges.mexc import buscar_preco as buscar_preco_mexc

preco_usdt_brl_mexc = buscar_preco_mexc("USDTBRL")
print("Preco atual USDT/BRL na MEXC:", preco_usdt_brl_mexc)