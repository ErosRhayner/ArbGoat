import json
import os

CAMINHO_ARQUIVO = "src/data/carteira.json"
SALDO_INICIAL = 1000.0


def carregar_saldo() -> float:
    """
    Le o saldo fictitious atual do arquivo carteira.json.
    Se o arquivo ainda nao existir, cria ele com o saldo inicial.
    """
    if not os.path.exists(CAMINHO_ARQUIVO):
        atualizar_saldo(0.0)

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados["saldo"]


def atualizar_saldo(valor_a_somar: float) -> float:
    """
    Soma (ou subtrai, se negativo) um valor ao saldo atual, e salva no arquivo.
    Retorna o novo saldo.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            saldo_atual = dados["saldo"]
    else:
        saldo_atual = SALDO_INICIAL

    novo_saldo = saldo_atual + valor_a_somar

    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump({"saldo": novo_saldo}, arquivo)

    return novo_saldo