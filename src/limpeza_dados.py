import pandas as pd
import os

def executar_limpeza():
    print(">>> INICIANDO LIMPEZA E TRATAMENTO DE DADOS (DATA QUALITY)")
    os.makedirs('data/interim', exist_ok=True)
    
    df_pedidos = pd.read_csv('data/raw/pedidos.csv')
    df_clientes = pd.read_csv('data/raw/clientes.csv')
    df_itens = pd.read_csv('data/raw/itens_pedido.csv')
    
    linhas_antes = len(df_pedidos)
    
    df_pedidos = df_pedidos.dropna(subset=['id', 'cliente_id'])
    df_pedidos = df_pedidos.rename(columns={'id': 'id_pedido'})
    df_pedidos['valor_total'] = df_pedidos['valor_total'].apply(lambda x: abs(x) if pd.notna(x) else x)
    
    if 'status' in df_pedidos.columns:
        df_pedidos['status'] = df_pedidos['status'].str.strip().str.title()
        
    linhas_removidas_pedidos = linhas_antes - len(df_pedidos)

    df_clientes['segmento'] = df_clientes['segmento'].str.strip().str.upper()

    print(f"  ✅ Tratamento concluído:")
    print(f"  - Pedidos nulos removidos: {linhas_removidas_pedidos}")
    print(f"  - Valores negativos convertidos para absoluto.")
    print(f"  - Textos de status e segmentos padronizados.")

    df_pedidos.to_csv('data/interim/pedidos_clean.csv', index=False)
    df_clientes.to_csv('data/interim/clientes_clean.csv', index=False)
    df_itens.to_csv('data/interim/itens_clean.csv', index=False)