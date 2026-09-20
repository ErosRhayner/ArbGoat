import requests

MOEDAS_COTACAO_CONHECIDAS = ["USDT", "USDC", "BRL"]


def buscar_preco(par: str) -> float:
    """
    Busca o preco atual de um par de moedas na OKX, usando a API publica.

    IMPORTANTE: a OKX usa hifen entre as moedas (ex: "USDT-BRL"), diferente
    das outras corretoras (ex: "USDTBRL"). Esta funcao converte automaticamente,
    identificando qual parte do texto e a moeda de cotacao (a que vem por ultimo).

    par: o simbolo do par no formato usado pelo resto do sistema (ex: "USDTBRL")
    Retorna o preco atual como float.
    """
    moeda_cotacao_encontrada = None
    for moeda in MOEDAS_COTACAO_CONHECIDAS:
        if par.endswith(moeda):
            moeda_cotacao_encontrada = moeda
            break

    if moeda_cotacao_encontrada is None:
        raise ValueError(f"Nao foi possivel identificar a moeda de cotacao no par {par}")

    moeda_base = par[:-len(moeda_cotacao_encontrada)]
    par_okx = f"{moeda_base}-{moeda_cotacao_encontrada}"

    url = "https://www.okx.com/api/v5/market/ticker"
    parametros = {"instId": par_okx}

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    primeiro_resultado = dados["data"][0]
    preco = float(primeiro_resultado["last"])
    return preco