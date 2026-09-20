import requests


def buscar_preco(par: str) -> float:
    """
    Busca o preco atual de um par de moedas na OKX, usando a API publica.

    IMPORTANTE: a OKX usa hifen entre as moedas (ex: "USDT-BRL"), diferente
    das outras corretoras (ex: "USDTBRL"). Esta funcao converte automaticamente
    do formato sem hifen (usado no resto do sistema) para o formato da OKX.

    par: o simbolo do par no formato usado pelo resto do sistema (ex: "USDTBRL")
    Retorna o preco atual como float.
    """
    if len(par) == 7:
        moeda_base = par[:4]
        moeda_cotacao = par[4:]
    else:
        moeda_base = par[:3]
        moeda_cotacao = par[3:]

    par_okx = f"{moeda_base}-{moeda_cotacao}"

    url = "https://www.okx.com/api/v5/market/ticker"
    parametros = {"instId": par_okx}

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    primeiro_resultado = dados["data"][0]
    preco = float(primeiro_resultado["last"])
    return preco