import pandas as pd
from scipy import stats

def responder_perguntas_pdf():
    print("\n==================================================")
    print("   RELATÓRIO DE RESPOSTAS - CASE NOVASHOP (PEERS) ")
    print("==================================================\n")
    
    df_pedidos = pd.read_csv('data/interim/pedidos_clean.csv')
    df_clientes = pd.read_csv('data/interim/clientes_clean.csv')
    df_itens = pd.read_csv('data/interim/itens_clean.csv')
    df_produtos = pd.read_csv('data/raw/produtos.csv') 
    
    
    print("--- P1: Distribuição de Pedidos por Status ---")
    distribuicao = df_pedidos['status'].value_counts(normalize=True) * 100
    print(distribuicao.round(2).astype(str) + ' %')
    
    print("\n--- P2: Top 10 Produtos Mais Vendidos ---")
    df_itens_prod = pd.merge(df_itens, df_produtos, left_on='produto_id', right_on='id', how='inner')
    df_itens_prod['receita_gerada'] = df_itens_prod['quantidade'] * df_itens_prod['preco_praticado']
    
    top_10 = df_itens_prod.groupby(['produto_id', 'categoria']).agg(
        qtd_vendida=('quantidade', 'sum'),
        receita_total=('receita_gerada', 'sum')
    ).nlargest(10, 'qtd_vendida')
    print(top_10.round(2))
    
    print("\n--- P3: Ticket Médio B2C vs B2B e Relevância Estatística ---")
    df_p3 = pd.merge(df_pedidos, df_clientes, left_on='cliente_id', right_on='id', how='inner')
    vendas_b2c = df_p3[df_p3['segmento'] == 'B2C']['valor_total'].dropna()
    vendas_b2b = df_p3[df_p3['segmento'] == 'B2B']['valor_total'].dropna()
    
    print(f"Ticket Médio B2C: R$ {vendas_b2c.mean():.2f}")
    print(f"Ticket Médio B2B: R$ {vendas_b2b.mean():.2f}")
    
    t_stat, p_valor = stats.ttest_ind(vendas_b2c, vendas_b2b, equal_var=False)
    relevante = "SIM" if p_valor < 0.05 else "NÃO"
    print(f"Diferença estatisticamente relevante? {relevante} (p-value: {p_valor:.4f})")
    print("*(Nota para o PDF: P-value < 0.05 indica que a diferença não é obra do acaso).*")
    
    print("\n--- P4: Evolução Mensal (Identificação de Picos) ---")
    
    df_pedidos['data_pedido'] = pd.to_datetime(df_pedidos['data_pedido'], errors='coerce')
    pedidos_por_mes = df_pedidos.dropna(subset=['data_pedido']).groupby(
        df_pedidos['data_pedido'].dt.to_period('M')
    ).size()
    print("Volume por mês (Últimos 12 meses):")
    print(pedidos_por_mes.tail(12))
    print("*(Nota para o PDF: Analise os meses de maior volume acima para formular a hipótese no documento).*")
    
    
    print("\n--- P5: Canais de Aquisição (Cancelamentos e Ticket) ---")
    total_por_canal = df_p3.groupby('canal_aquisicao').size()
    
    
    cancelados = df_p3[df_p3['status'].str.contains('Cancelado', case=False, na=False)]
    canc_por_canal = cancelados.groupby('canal_aquisicao').size()
    
    taxa_cancelamento = (canc_por_canal / total_por_canal * 100).fillna(0).sort_values(ascending=False)
    ticket_por_canal = df_p3.groupby('canal_aquisicao')['valor_total'].mean().sort_values(ascending=False)
    
    print("Top Taxa de Cancelamento (%):")
    print(taxa_cancelamento.round(2).head(3))
    print("\nTop Ticket Médio (R$):")
    print(ticket_por_canal.round(2).head(3))
    print("==================================================\n")