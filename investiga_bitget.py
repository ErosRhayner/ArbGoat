import json
from datetime import datetime

CAMINHO_ARQUIVO = "src/data/historico_oportunidades.jsonl"

print("===== Investigando comportamento da Bitget =====\n")

registros_bitget_venda = []

with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        registro = json.loads(linha)
        if registro.get("corretora_venda") == "Bitget":
            registros_bitget_venda.append(registro)

print(f"Total de registros onde Bitget foi corretora_venda: {len(registros_bitget_venda)}")
print()

pares_bitget = {}
for r in registros_bitget_venda:
    par = r.get("par", "desconhecido")
    preco_bitget = r.get("precos_todas_corretoras", {}).get("Bitget")
    timestamp = r.get("timestamp", "")
    if par not in pares_bitget:
        pares_bitget[par] = []
    if preco_bitget:
        pares_bitget[par].append((timestamp, preco_bitget))

for par, dados in pares_bitget.items():
    if len(dados) < 2:
        continue

    precos = [p for _, p in dados]
    preco_min = min(precos)
    preco_max = max(precos)
    variacao = ((preco_max - preco_min) / preco_min) * 100

    precos_unicos = len(set(precos))
    total = len(precos)
    percentual_estatico = ((total - precos_unicos) / total) * 100

    print(f"--- {par} ---")
    print(f"Registros analisados: {total}")
    print(f"Preço mínimo da Bitget: {preco_min:.4f}")
    print(f"Preço máximo da Bitget: {preco_max:.4f}")
    print(f"Variação total: {variacao:.4f}%")
    print(f"Preços únicos: {precos_unicos} de {total} ({100-percentual_estatico:.1f}% variaram)")
    print(f"Preços repetidos (estáticos): {percentual_estatico:.1f}%")
    print()

    print("Primeiros 5 preços registrados:")
    for ts, p in dados[:5]:
        print(f"  {ts[:19]}: {p:.4f}")
    print("Últimos 5 preços registrados:")
    for ts, p in dados[-5:]:
        print(f"  {ts[:19]}: {p:.4f}")
    print()