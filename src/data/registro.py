import json
from datetime import datetime


CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"

_ultimo_precos_por_par = {}


def registrar_oportunidade(oportunidade: dict) -> bool:
    """
    Salva uma oportunidade analisada no arquivo de historico, adicionando
    um timestamp a cada registro.

    Para evitar registros duplicados (quando o preco nao mudou desde a ultima
    verificacao do mesmo par), a funcao compara com o ultimo preco registrado
    para aquele par nesta execucao do programa. Se for identico, nao registra.

    oportunidade: o dicionario retornado por detectar_oportunidade
    Retorna True se o registro foi salvo, False se foi ignorado por ser duplicado.
    """
    par = oportunidade.get("par", "desconhecido")
    precos_atuais = oportunidade.get("precos_todas_corretoras")

    if _ultimo_precos_por_par.get(par) == precos_atuais:
        return False

    _ultimo_precos_por_par[par] = precos_atuais

    registro = oportunidade.copy()
    registro["timestamp"] = datetime.now().isoformat()

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arquivo:
        linha_json = json.dumps(registro, ensure_ascii=False)
        arquivo.write(linha_json + "\n")

    return True