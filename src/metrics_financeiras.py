import pandas as pd
import os

def gerar_visao_geografica():
    print("  Lendo bases de pedidos e clientes...")
    
    # lendo a partir da raiz do projeto
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

    # Cria a pasta caso ela não exista ainda (boa prática para não dar erro)
    os.makedirs('data/processed', exist_ok=True)

    caminho_saida = 'data/processed/visao_vendas_geografia.csv'
    df_vendas_clientes.to_csv(caminho_saida, index=False)
    print(f"  ✅ Visão Financeira salva em: {caminho_saida}")