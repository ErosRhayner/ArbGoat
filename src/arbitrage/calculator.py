def calcular_lucro_bruto(preco_compra: float, preco_venda: float, quantidade: float) -> float:
    """
    Calcula o lucro bruto de uma operação de arbitragem,
    SEM considerar taxas, spread real ou slippage ainda.

    preco_compra: preço pelo qual o ativo foi comprado na Exchange A
    preco_venda: preço pelo qual o ativo foi vendido na Exchange B
    quantidade: quantidade do ativo negociado
    """
    custo_total = preco_compra * quantidade
    receita_total = preco_venda * quantidade
    lucro_bruto = receita_total - custo_total
    return lucro_bruto

def calcular_lucro_com_taxas(preco_compra: float, preco_venda: float, quantidade: float,
                              taxa_compra: float, taxa_venda: float) -> float:
    """
    Calcula o lucro considerando as taxas de negociacao de cada corretora.

    preco_compra: preco pelo qual o ativo foi comprado na Exchange A
    preco_venda: preco pelo qual o ativo foi vendido na Exchange B
    quantidade: quantidade do ativo negociado
    taxa_compra: taxa da corretora de compra, em decimal (ex: 0.001 para 0.1%)
    taxa_venda: taxa da corretora de venda, em decimal (ex: 0.0015 para 0.15%)
    """
    custo_real = preco_compra * quantidade * (1 + taxa_compra)
    receita_real = preco_venda * quantidade * (1 - taxa_venda)
    lucro_com_taxas = receita_real - custo_real
    return lucro_com_taxas

def calcular_lucro_liquido(preco_compra: float, preco_venda: float, quantidade: float,
                            taxa_compra: float, taxa_venda: float, taxa_rede: float) -> float:
    """
    Calcula o lucro liquido final, considerando taxas de negociacao
    das duas corretoras E a taxa fixa de transferencia entre elas.

    preco_compra: preco pelo qual o ativo foi comprado na Exchange A
    preco_venda: preco pelo qual o ativo foi vendido na Exchange B
    quantidade: quantidade do ativo negociado
    taxa_compra: taxa da corretora de compra, em decimal (ex: 0.001 para 0.1%)
    taxa_venda: taxa da corretora de venda, em decimal (ex: 0.0015 para 0.15%)
    taxa_rede: custo fixo, em dinheiro, para transferir o ativo entre as corretoras
    """
    lucro_com_taxas = calcular_lucro_com_taxas(preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda)
    lucro_liquido = lucro_com_taxas - taxa_rede
    return lucro_liquido

def calcular_percentual_retorno(preco_compra: float, preco_venda: float, quantidade: float,
                                 taxa_compra: float, taxa_venda: float, taxa_rede: float) -> float:
    """
    Calcula o percentual de retorno de uma operacao de arbitragem,
    com base no lucro liquido dividido pelo capital investido.

    Os parametros sao os mesmos de calcular_lucro_liquido.
    Retorna o percentual (ex: 0.55 significa 0.55%).
    """
    lucro_liquido = calcular_lucro_liquido(preco_compra, preco_venda, quantidade, taxa_compra, taxa_venda, taxa_rede)
    custo_investido = preco_compra * quantidade * (1 + taxa_compra)
    percentual_retorno = (lucro_liquido / custo_investido) * 100
    return percentual_retorno

def calcular_spread_percentual(preco_compra: float, preco_venda: float) -> float:
    """
    Calcula a diferenca percentual bruta entre o preco de compra e o preco de venda,
    sem considerar taxas. Usado como filtro rapido antes do calculo completo.

    preco_compra: preco do ativo na corretora mais barata
    preco_venda: preco do ativo na corretora mais cara
    Retorna o percentual (ex: 1.0 significa 1.0%).
    """
    spread_percentual = ((preco_venda - preco_compra) / preco_compra) * 100
    return spread_percentual

def aplicar_slippage(preco_compra: float, preco_venda: float,
                      slippage_compra: float, slippage_venda: float) -> tuple:
    """
    Ajusta os precos de compra e venda para refletir o slippage estimado.
    O slippage sempre piora o preco: aumenta o preco de compra
    e diminui o preco de venda.

    slippage_compra: percentual estimado de piora na compra, em decimal (ex: 0.0005 para 0.05%)
    slippage_venda: percentual estimado de piora na venda, em decimal (ex: 0.0005 para 0.05%)

    Retorna uma tupla: (preco_compra_ajustado, preco_venda_ajustado)
    """
    preco_compra_ajustado = preco_compra * (1 + slippage_compra)
    preco_venda_ajustado = preco_venda * (1 - slippage_venda)
    return (preco_compra_ajustado, preco_venda_ajustado)

def operacao_e_segura(preco_compra: float, preco_venda: float, quantidade: float,
                       taxa_compra: float, taxa_venda: float, taxa_rede: float,
                       slippage_compra: float, slippage_venda: float,
                       margem_minima: float) -> bool:
    """
    Decide se uma operacao de arbitragem e segura o suficiente para prosseguir,
    considerando taxas, rede, slippage estimado e uma margem de seguranca minima.

    margem_minima: percentual minimo de retorno exigido, em decimal
                   (ex: 0.2 significa exigir pelo menos 0.2% de retorno)

    Retorna True se a operacao atende a margem minima, False caso contrario.
    """
    preco_compra_ajustado, preco_venda_ajustado = aplicar_slippage(
        preco_compra, preco_venda, slippage_compra, slippage_venda
    )

    percentual_retorno = calcular_percentual_retorno(
        preco_compra_ajustado, preco_venda_ajustado, quantidade,
        taxa_compra, taxa_venda, taxa_rede
    )

    return percentual_retorno >= margem_minima