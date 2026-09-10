import requests


def buscar_preco(par: str) -> float:
    """
    Busca o preco atual de um par de moedas na Binance, usando a API publica
    (nao precisa de chave/login, pois e um dado publico de mercado).

    par: o simbolo do par, no formato da Binance (ex: "USDTBRL", "BTCUSDT")
    Retorna o preco atual como float.
    """
    url = "https://api.binance.com/api/v3/ticker/price"
    parametros = {"symbol": par}

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    preco = float(dados["price"])
    return preco