from src.exchanges.binance import buscar_preco as teste_binance
from src.exchanges.bitget import buscar_preco as teste_bitget
from src.exchanges.mexc import buscar_preco as teste_mexc
from src.exchanges.okx import buscar_preco as teste_okx

CORRETORAS_TESTE = {
    "Binance": teste_binance,
    "Bitget": teste_bitget,
    "MEXC": teste_mexc,
    "OKX": teste_okx,
}

for par_teste in ["BTCBRL", "ETHBRL"]:
    print(f"--- Testando {par_teste} ---")
    for nome, funcao in CORRETORAS_TESTE.items():
        try:
            preco = funcao(par_teste)
            print(f"{nome}: {preco}")
        except Exception as erro:
            print(f"{nome} falhou: {erro}")
    print()