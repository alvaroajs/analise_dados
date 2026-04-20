import pandas as pd
import os

def gerar_visao_fornecedores():
    print("  Lendo bases de suporte, itens e produtos...")
    
    df_tickets = pd.read_csv('data/raw/tickets_suporte.csv')
    df_itens = pd.read_csv('data/raw/itens_pedido.csv')
    df_produtos = pd.read_csv('data/raw/produtos.csv')

    print("  Cruzando Itens com Produtos...")
    df_itens_produtos = pd.merge(
        df_itens,
        df_produtos,
        left_on='produto_id',
        right_on='id',
        how='inner'
    )

    print("  Cruzando com Tickets de Suporte...")
    df_problemas = pd.merge(
        df_tickets,
        df_itens_produtos,
        on='pedido_id', 
        how='inner'
    )

    os.makedirs('data/interim', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)

    print("  Salvando base intermediária...")
    df_problemas.to_csv('data/interim/base_problemas_suporte.csv', index=False)
    
    print("  Calculando o ranking de fornecedores...")
    
    ranking_fornecedores = df_problemas.groupby('fornecedor').size().reset_index()
    ranking_fornecedores = ranking_fornecedores.rename(columns={0: 'qtd_chamados'})
    ranking_fornecedores = ranking_fornecedores.sort_values(by='qtd_chamados', ascending=False)
    
    caminho_saida = 'data/processed/ranking_fornecedores_problema.csv'
    ranking_fornecedores.to_csv(caminho_saida, index=False)
    print(f"  ✅ Visão de Qualidade salva em: {caminho_saida}")