import pandas as pd
import os

def gerar_visao_lucratividade():
    print("  Lendo bases de itens e produtos para lucratividade...")
    df_itens = pd.read_csv('data/raw/itens_pedido.csv')
    df_produtos = pd.read_csv('data/raw/produtos.csv')

    # cruzamento para obter o custo e a categoria de cada item vendido
    df_margem = pd.merge(
        df_itens,
        df_produtos,
        left_on='produto_id',
        right_on='id',
        how='inner'
    )

    df_margem['receita_total'] = df_margem['preco_praticado'] * df_margem['quantidade']
    df_margem['custo_total'] = df_margem['custo_unitario'] * df_margem['quantidade']
    df_margem['lucro_bruto'] = df_margem['receita_total'] - df_margem['custo_total']

    visao_lucro = df_margem.groupby('categoria').agg(
        faturamento=('receita_total', 'sum'),
        lucro=('lucro_bruto', 'sum')
    ).reset_index()

    visao_lucro['margem_percentual'] = (visao_lucro['lucro'] / visao_lucro['faturamento']) * 100
    visao_lucro = visao_lucro.sort_values(by='lucro', ascending=False)

    os.makedirs('data/processed', exist_ok=True)
    caminho_saida = 'data/processed/visao_lucratividade_categoria.csv'
    visao_lucro.to_csv(caminho_saida, index=False)
    print(f"  ✅ Visão de Lucratividade salva em: {caminho_saida}")