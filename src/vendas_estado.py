import pandas as pd
import os

def gerar_visao_geografica():
    print("  Lendo bases de pedidos e clientes...")

    df_pedidos = pd.read_csv('data/raw/pedidos.csv')
    df_clientes = pd.read_csv('data/raw/clientes.csv')

    print("  Cruzando dados (JOIN de Pedidos e Clientes)...")
    df_vendas_clientes = pd.merge(
        df_pedidos,
        df_clientes,
        left_on='cliente_id',
        right_on='id',
        how='inner'
    )

    os.makedirs('data/processed', exist_ok=True)

    print("  Agregando vendas por estado...")
    visao_estado = df_vendas_clientes.groupby('estado').agg(
        total_pedidos=('id_x', 'count'),
        receita_total=('valor_total', 'sum'),
        ticket_medio=('valor_total', 'mean')
    ).reset_index().round(2)

    caminho_saida = 'data/processed/visao_vendas_estado.csv'
    visao_estado.to_csv(caminho_saida, index=False)
    print(f"  ✅ Visão por Estado salva em: {caminho_saida}")