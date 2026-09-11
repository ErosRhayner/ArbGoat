import json
from datetime import datetime


CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"


def registrar_oportunidade(oportunidade: dict) -> None:
    """
    Salva uma oportunidade analisada no arquivo de historico,
    adicionando um timestamp (data e hora) a cada registro.

    oportunidade: o dicionario retornado por detectar_oportunidade
    """
    registro = oportunidade.copy()
    registro["timestamp"] = datetime.now().isoformat()

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arquivo:
        linha_json = json.dumps(registro, ensure_ascii=False)
        arquivo.write(linha_json + "\n")