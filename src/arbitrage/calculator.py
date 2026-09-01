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