import time
import requests
import winsound
from datetime import datetime
from src.arbitrage.detector import detectar_oportunidade
from src.data.registro import registrar_oportunidade
from src.data.carteira import carregar_saldo, atualizar_saldo

SALDO_INICIAL_TESTE = 1000.0

PARES_MONITORADOS = {
    "USDTBRL": 193,
    "BTCBRL": 0.00227,
    "ETHBRL": 0.07143,
}

saldo_inicial = SALDO_INICIAL_TESTE
atualizar_saldo(saldo_inicial - carregar_saldo())

operacoes_executadas = 0
lucro_acumulado = 0.0
inicio_teste = datetime.now()
inicio_hora_atual = datetime.now()
operacoes_hora = 0
lucro_hora = 0.0
numero_hora = 1

print("=" * 50)
print("Simulacao iniciada!")
print("Pares monitorados:", list(PARES_MONITORADOS.keys()))
print("Saldo inicial: R$1.000,00")
print("Inicio:", inicio_teste.strftime("%d/%m/%Y %H:%M:%S"))
print("Relatorio parcial a cada 1 hora")
print("=" * 50)

def imprimir_relatorio_hora(numero, inicio, fim, operacoes, lucro, saldo_atual):
    print("\n" + "=" * 50)
    print(f"RELATORIO HORA {numero}")
    print("=" * 50)
    print(f"Periodo:             {inicio.strftime('%H:%M:%S')} - {fim.strftime('%H:%M:%S')}")
    print(f"Operacoes seguras:   {operacoes}")
    print(f"Lucro nessa hora:    R${lucro:.2f}")
    print(f"Saldo atual:         R${saldo_atual:.2f}")
    print("=" * 50 + "\n")

try:
    while True:
        agora = datetime.now()
        segundos_desde_inicio_hora = (agora - inicio_hora_atual).total_seconds()

        if segundos_desde_inicio_hora >= 3600:
            saldo_atual = carregar_saldo()
            imprimir_relatorio_hora(
                numero_hora,
                inicio_hora_atual,
                agora,
                operacoes_hora,
                lucro_hora,
                saldo_atual
            )
            numero_hora += 1
            inicio_hora_atual = agora
            operacoes_hora = 0
            lucro_hora = 0.0

        for par, quantidade in PARES_MONITORADOS.items():
            try:
                oportunidade = detectar_oportunidade(
                    par=par,
                    quantidade=quantidade,
                    taxa_compra=0.001,
                    taxa_venda=0.0015,
                    taxa_rede=2.0,
                    slippage_compra=0.0005,
                    slippage_venda=0.0005,
                    margem_minima=0.1
                )

                oportunidade["par"] = par
                foi_registrado = registrar_oportunidade(oportunidade)

                if foi_registrado:
                    print(oportunidade)
                else:
                    print(f"{par}: preco sem mudanca, nao registrado.")

                if oportunidade["operacao_segura"]:
                    lucro = oportunidade["lucro_liquido"]
                    novo_saldo = atualizar_saldo(lucro)
                    operacoes_executadas += 1
                    operacoes_hora += 1
                    lucro_acumulado += lucro
                    lucro_hora += lucro
                    print(f"Operacao executada (simulada)! Novo saldo: R${novo_saldo:.2f}")
                    print("!!! OPORTUNIDADE SEGURA ENCONTRADA !!!")
                    winsound.Beep(1000, 300)
                    winsound.Beep(1500, 300)
                    winsound.Beep(1000, 300)

            except (requests.exceptions.RequestException, ValueError) as erro:
                print(f"Falha ao analisar o par {par}, tentando novamente no proximo ciclo:", erro)

        time.sleep(30)

except KeyboardInterrupt:
    fim_teste = datetime.now()
    saldo_final = carregar_saldo()
    lucro_total = saldo_final - SALDO_INICIAL_TESTE
    duracao = fim_teste - inicio_teste

    if operacoes_hora > 0 or lucro_hora != 0:
        imprimir_relatorio_hora(
            numero_hora,
            inicio_hora_atual,
            fim_teste,
            operacoes_hora,
            lucro_hora,
            saldo_final
        )

    print("\n" + "=" * 50)
    print("RESUMO FINAL DO TESTE")
    print("=" * 50)
    print(f"Inicio:              {inicio_teste.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Fim:                 {fim_teste.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Duracao:             {str(duracao).split('.')[0]}")
    print(f"Operacoes seguras:   {operacoes_executadas}")
    print(f"Saldo inicial:       R$1.000,00")
    print(f"Saldo final:         R${saldo_final:.2f}")
    print(f"Lucro/Prejuizo:      R${lucro_total:.2f}")
    print(f"Retorno total:       {(lucro_total / SALDO_INICIAL_TESTE * 100):.4f}%")
    print("=" * 50)
