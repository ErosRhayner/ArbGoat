import json

CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"

# Deixe em branco ("") para analisar TODO o historico.
# Ou coloque uma data/hora no formato "AAAA-MM-DDTHH:MM:SS" para ignorar
# tudo que foi registrado ANTES desse momento.
FILTRAR_A_PARTIR_DE = ""

estatisticas_por_par = {}

with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        registro = json.loads(linha)

        if FILTRAR_A_PARTIR_DE:
            if registro["timestamp"] < FILTRAR_A_PARTIR_DE:
                continue

        par = registro.get("par", "desconhecido")

        if par not in estatisticas_por_par:
            estatisticas_por_par[par] = {
                "total": 0,
                "seguras": 0,
                "melhor_percentual": None,
            }

        stats = estatisticas_por_par[par]
        stats["total"] += 1

        if registro["operacao_segura"]:
            stats["seguras"] += 1

        percentual = registro["percentual_retorno"]
        if stats["melhor_percentual"] is None or percentual > stats["melhor_percentual"]:
            stats["melhor_percentual"] = percentual

print("===== Resumo do historico =====")
if FILTRAR_A_PARTIR_DE:
    print("Considerando apenas registros a partir de:", FILTRAR_A_PARTIR_DE)

if not estatisticas_por_par:
    print("Nenhuma verificacao encontrada com esse filtro.")

for par, stats in estatisticas_por_par.items():
    print(f"\n--- {par} ---")
    print("Total de verificacoes:", stats["total"])
    print("Operacoes consideradas seguras:", stats["seguras"])
    print("Melhor percentual de retorno encontrado:", round(stats["melhor_percentual"], 4), "%")
    taxa_sucesso = (stats["seguras"] / stats["total"]) * 100
    print("Taxa de oportunidades seguras:", round(taxa_sucesso, 2), "%")