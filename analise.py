import json
from datetime import datetime

CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"

# Deixe em branco ("") para analisar TODO o historico.
# Ou coloque uma data/hora no formato "AAAA-MM-DDTHH:MM:SS" para ignorar
# tudo que foi registrado ANTES desse momento.
FILTRAR_A_PARTIR_DE = ""

total_verificacoes = 0
operacoes_seguras = 0
melhor_percentual = None

with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        registro = json.loads(linha)

        if FILTRAR_A_PARTIR_DE:
            if registro["timestamp"] < FILTRAR_A_PARTIR_DE:
                continue

        total_verificacoes += 1

        if registro["operacao_segura"]:
            operacoes_seguras += 1

        percentual = registro["percentual_retorno"]
        if melhor_percentual is None or percentual > melhor_percentual:
            melhor_percentual = percentual

print("===== Resumo do historico =====")
if FILTRAR_A_PARTIR_DE:
    print("Considerando apenas registros a partir de:", FILTRAR_A_PARTIR_DE)
print("Total de verificacoes:", total_verificacoes)
print("Operacoes consideradas seguras:", operacoes_seguras)

if melhor_percentual is not None:
    print("Melhor percentual de retorno encontrado:", round(melhor_percentual, 4), "%")

if total_verificacoes > 0:
    taxa_sucesso = (operacoes_seguras / total_verificacoes) * 100
    print("Taxa de oportunidades seguras:", round(taxa_sucesso, 2), "%")
else:
    print("Nenhuma verificacao encontrada com esse filtro.")