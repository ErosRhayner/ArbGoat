import requests


def buscar_preco(par: str) -> float:
    """
    Busca o preco atual de um par de moedas na Bitget, usando a API publica.

    par: o simbolo do par, no formato da Bitget (ex: "USDTBRL", "BTCUSDT")
    Retorna o preco atual como float.
    """
    url = "https://api.bitget.com/api/v2/spot/market/tickers"
    parametros = {"symbol": par}

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    primeiro_resultado = dados["data"][0]
    preco = float(primeiro_resultado["lastPr"])
    return preco