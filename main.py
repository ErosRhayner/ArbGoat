print("ArbGoat iniciado!")
print("Versão: 0.0.1")
print("Status: Em desenvolvimento")
from src.exchanges.binance import buscar_preco

preco_usdt_brl = buscar_preco("USDTBRL")
print("Preco atual USDT/BRL na Binance:", preco_usdt_brl)
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget

preco_usdt_brl_bitget = buscar_preco_bitget("USDTBRL")
print("Preco atual USDT/BRL na Bitget:", preco_usdt_brl_bitget)