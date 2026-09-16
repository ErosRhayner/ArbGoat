import json
from datetime import datetime

CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"

FILTRAR_A_PARTIR_DE = ""

estatisticas_por_par = {}
contagem_por_hora = {}
contagem_por_data = {}

with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        registro = json.loads(linha)

        if FILTRAR_A_PARTIR_DE:
            if registro["timestamp"] < FILTRAR_A_PARTIR_DE:
                continue

        par = registro.get("par", "desconhecido")
        percentual = registro["percentual_retorno"]

        momento = datetime.fromisoformat(registro["timestamp"])
        hora = momento.hour
        data = momento.date().isoformat()

        if par not in estatisticas_por_par:
            estatisticas_por_par[par] = {
                "total": 0,
                "seguras": 0,
                "melhor_percentual": None,
                "pior_percentual": None,
                "soma_percentual": 0.0,
            }
        stats = estatisticas_por_par[par]
        stats["total"] += 1
        stats["soma_percentual"] += percentual

        if registro["operacao_segura"]:
            stats["seguras"] += 1

        if stats["melhor_percentual"] is None or percentual > stats["melhor_percentual"]:
            stats["melhor_percentual"] = percentual
        if stats["pior_percentual"] is None or percentual < stats["pior_percentual"]:
            stats["pior_percentual"] = percentual

        chave_hora = (par, hora)
        if chave_hora not in contagem_por_hora:
            contagem_por_hora[chave_hora] = {"total": 0, "soma_percentual": 0.0}
        contagem_por_hora[chave_hora]["total"] += 1
        contagem_por_hora[chave_hora]["soma_percentual"] += percentual

        chave_data = (par, data)
        contagem_por_data[chave_data] = contagem_por_data.get(chave_data, 0) + 1


print("===== Resumo geral por par =====")
if not estatisticas_por_par:
    print("Nenhuma verificacao encontrada com esse filtro.")

for par, stats in estatisticas_por_par.items():
    media = stats["soma_percentual"] / stats["total"]
    taxa_sucesso = (stats["seguras"] / stats["total"]) * 100
    print(f"\n--- {par} ---")
    print("Total de verificacoes:", stats["total"])
    print("Operacoes consideradas seguras:", stats["seguras"], f"({round(taxa_sucesso, 2)}%)")
    print("Percentual medio de retorno:", round(media, 4), "%")
    print("Melhor percentual encontrado:", round(stats["melhor_percentual"], 4), "%")
    print("Pior percentual encontrado:", round(stats["pior_percentual"], 4), "%")

print("\n===== Media de percentual por hora do dia =====")
for (par, hora), dados in sorted(contagem_por_hora.items()):
    media_hora = dados["soma_percentual"] / dados["total"]
    print(f"{par} - {hora:02d}h: {dados['total']} verificacoes, media {round(media_hora, 4)}%")

print("\n===== Verificacoes por data =====")
for (par, data), total in sorted(contagem_por_data.items()):
    print(f"{par} - {data}: {total} verificacoes")