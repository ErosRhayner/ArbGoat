import requests
from src.exchanges.binance import buscar_preco as buscar_preco_binance
from src.exchanges.bitget import buscar_preco as buscar_preco_bitget
from src.exchanges.mexc import buscar_preco as buscar_preco_mexc
from src.exchanges.okx import buscar_preco as buscar_preco_okx
from src.arbitrage.calculator import calcular_percentual_retorno, calcular_lucro_liquido, aplicar_slippage


CORRETORAS = {
    "Binance": buscar_preco_binance,
    "Bitget": buscar_preco_bitget,
    "MEXC": buscar_preco_mexc,
    "OKX": buscar_preco_okx,
}


def buscar_precos_todas_corretoras(par: str) -> dict:
    """
    Busca o preco atual de um par em todas as corretoras cadastradas em CORRETORAS.
    Corretoras que nao tem esse par (ou falham por qualquer motivo) sao
    simplesmente ignoradas, em vez de quebrar a busca inteira.

    Diferencia falhas de rede (temporarias) de respostas em formato inesperado
    (geralmente sinal de que o par nao existe naquela corretora).

    Retorna um dicionario no formato {nome_da_corretora: preco}, contendo
    apenas as corretoras que responderam com sucesso.
    """
    precos = {}
    for nome, funcao_buscar_preco in CORRETORAS.items():
        try:
            precos[nome] = funcao_buscar_preco(par)
        except requests.exceptions.RequestException as erro:
            print(f"Aviso: falha de rede ao consultar {nome} para o par {par}. Ignorando. Detalhe: {erro}")
        except (KeyError, TypeError) as erro:
            print(f"Aviso: {nome} provavelmente nao possui o par {par} (resposta em formato inesperado). Ignorando.")
        except Exception as erro:
            print(f"Aviso: erro inesperado ao consultar {nome} para o par {par}. Ignorando. Detalhe: {erro}")
    return precos


def detectar_oportunidade(par: str, quantidade: float,
                           taxa_compra: float, taxa_venda: float, taxa_rede: float,
                           slippage_compra: float, slippage_venda: float,
                           margem_minima: float) -> dict:
    """
    Busca precos reais em todas as corretoras cadastradas, encontra a rota
    com maior spread bruto (menor preco de compra, maior preco de venda),
    aplica slippage, e avalia se a operacao e segura.

    Corretoras que nao tem o par sao ignoradas automaticamente.
    Levanta ValueError se menos de 2 corretoras tiverem preco disponivel.

    Retorna um dicionario com os detalhes da melhor rota encontrada.
    """
    precos = buscar_precos_todas_corretoras(par)

    if len(precos) < 2:
        raise ValueError(f"Menos de 2 corretoras disponiveis para o par {par}. Nao e possivel calcular arbitragem.")

    corretora_compra = min(precos, key=precos.get)
    corretora_venda = max(precos, key=precos.get)

    preco_compra_bruto = precos[corretora_compra]
    preco_venda_bruto = precos[corretora_venda]

    preco_compra, preco_venda = aplicar_slippage(
        preco_compra_bruto, preco_venda_bruto, slippage_compra, slippage_venda
    )

    percentual_retorno = calcular_percentual_retorno(
        preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede
    )

    lucro_liquido = calcular_lucro_liquido(
        preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede
    )

    e_segura = percentual_retorno >= margem_minima

    resultado = {
        "corretora_compra": corretora_compra,
        "corretora_venda": corretora_venda,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "percentual_retorno": percentual_retorno,
        "lucro_liquido": lucro_liquido,
        "operacao_segura": e_segura,
        "precos_todas_corretoras": precos,
    }
    return resultado