import requests


def buscar_preco(par: str) -> float:
    """
    Busca o preco atual de um par de moedas na MEXC, usando a API publica.

    IMPORTANTE: a MEXC usa o par invertido para USDT/BRL (chama-se "BRLUSDT",
    nao "USDTBRL" como na Binance/Bitget). Esta funcao ja faz a inversao
    matematica automaticamente para o par "USDTBRL", para manter a
    interface igual a das outras corretoras.

    par: o simbolo do par no formato da Binance/Bitget (ex: "USDTBRL")
    Retorna o preco atual como float, ja no mesmo sentido das outras corretoras.
    """
    if par == "USDTBRL":
        par_mexc = "BRLUSDT"
        precisa_inverter = True
    else:
        par_mexc = par
        precisa_inverter = False

    url = "https://api.mexc.com/api/v3/ticker/price"
    parametros = {"symbol": par_mexc}

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    preco = float(dados["price"])

    if precisa_inverter:
        preco = 1 / preco

    return preco