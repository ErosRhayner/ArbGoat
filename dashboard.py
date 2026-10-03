import streamlit as st
import json
import os
from datetime import datetime
from src.arbitrage.detector import buscar_precos_todas_corretoras
from src.data.carteira import carregar_saldo

PARES_MONITORADOS = {
    "USDTBRL": 193,
    "BTCBRL": 0.00227,
    "ETHBRL": 0.07143,
}

CAMINHO_HISTORICO = "src/data/historico_oportunidades.jsonl"

st.set_page_config(
    page_title="ArbGoat Dashboard",
    page_icon="🐐",
    layout="wide"
)

st.title("🐐 ArbGoat — Monitor de Arbitragem")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

st.divider()

col1, col2, col3 = st.columns(3)

saldo = carregar_saldo()
with col1:
    st.metric("Saldo da Carteira", f"R$ {saldo:.2f}")
with col2:
    total_registros = 0
    operacoes_seguras = 0
    if os.path.exists(CAMINHO_HISTORICO):
        with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as f:
            for linha in f:
                r = json.loads(linha)
                total_registros += 1
                if r.get("operacao_segura"):
                    operacoes_seguras += 1
    st.metric("Total de Verificacoes", total_registros)
with col3:
    taxa = (operacoes_seguras / total_registros * 100) if total_registros > 0 else 0
    st.metric("Operacoes Seguras", f"{operacoes_seguras} ({taxa:.1f}%)")

st.divider()
st.subheader("Precos Atuais por Par")

for par in PARES_MONITORADOS:
    st.markdown(f"**{par}**")
    try:
        precos = buscar_precos_todas_corretoras(par)
        if len(precos) >= 2:
            preco_min = min(precos.values())
            preco_max = max(precos.values())
            spread = ((preco_max - preco_min) / preco_min) * 100

            cols = st.columns(len(precos) + 1)
            for i, (corretora, preco) in enumerate(precos.items()):
                with cols[i]:
                    st.metric(corretora, f"{preco:.4f}")

            with cols[-1]:
                cor = "🟢" if spread > 0.3 else "🟡" if spread > 0.1 else "🔴"
                st.metric("Spread Bruto", f"{cor} {spread:.4f}%")
        else:
            st.warning(f"Menos de 2 corretoras disponiveis para {par}")
    except Exception as e:
        st.error(f"Erro ao buscar precos de {par}: {e}")

st.divider()
st.subheader("Ultimas 10 Operacoes Seguras")

operacoes = []
if os.path.exists(CAMINHO_HISTORICO):
    with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as f:
        for linha in f:
            r = json.loads(linha)
            if r.get("operacao_segura"):
                operacoes.append({
                    "Horario": r.get("timestamp", "")[:19],
                    "Par": r.get("par", "?"),
                    "Compra em": r.get("corretora_compra", "?"),
                    "Venda em": r.get("corretora_venda", "?"),
                    "Retorno %": round(r.get("percentual_retorno", 0), 4),
                    "Lucro R$": round(r.get("lucro_liquido", 0), 2),
                })

if operacoes:
    ultimas = operacoes[-10:][::-1]
    st.table(ultimas)
else:
    st.info("Nenhuma operacao segura registrada ainda.")

st.divider()
st.caption("ArbGoat v0.0.1 — Paper Trading Mode")
