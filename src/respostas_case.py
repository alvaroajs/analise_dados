import pandas as pd
from scipy import stats
import os

def responder_perguntas_pdf():
    print("\n==================================================")
    print("   RELATÓRIO DE RESPOSTAS - CASE NOVASHOP (PEERS) ")
    print("==================================================\n")

    os.makedirs('data/processed', exist_ok=True)

    df_pedidos = pd.read_csv('data/interim/pedidos_clean.csv')
    df_clientes = pd.read_csv('data/interim/clientes_clean.csv')
    df_itens = pd.read_csv('data/interim/itens_clean.csv')
    df_produtos = pd.read_csv('data/raw/produtos.csv')

    # P1: Distribuição de Pedidos por Status# -------------------------------------------------------
    print("--- P1: Distribuição de Pedidos por Status ---")

    distribuicao = df_pedidos['status'].value_counts().reset_index()
    distribuicao.columns = ['status', 'volume']
    distribuicao['percentual'] = (distribuicao['volume'] / distribuicao['volume'].sum() * 100).round(2)

    print(distribuicao.to_string(index=False))

    distribuicao.to_csv('data/processed/p1_status_distribuicao.csv', index=False)
    print("  ✅ Exportado: p1_status_distribuicao.csv\n")

    # P2: Top 10 Produtos Mais Vendidos# -------------------------------------------------------
    print("--- P2: Top 10 Produtos Mais Vendidos ---")

    df_itens_prod = pd.merge(df_itens, df_produtos, left_on='produto_id', right_on='id', how='inner')
    df_itens_prod['receita_gerada'] = df_itens_prod['quantidade'] * df_itens_prod['preco_praticado']

    top_10 = (
        df_itens_prod
        .groupby(['produto_id', 'nome', 'categoria'])
        .agg(qtd_vendida=('quantidade', 'sum'), receita_total=('receita_gerada', 'sum'))
        .reset_index()
        .nlargest(10, 'qtd_vendida')
        .round(2)
    )

    print(top_10.to_string(index=False))

    top_10.to_csv('data/processed/p2_top10_produtos.csv', index=False)
    print("  ✅ Exportado: p2_top10_produtos.csv\n")

    # P3: Ticket Médio B2C vs B2B# -------------------------------------------------------
    print("--- P3: Ticket Médio B2C vs B2B e Relevância Estatística ---")

    df_p3 = pd.merge(df_pedidos, df_clientes, left_on='cliente_id', right_on='id', how='inner')
    vendas_b2c = df_p3[df_p3['segmento'] == 'B2C']['valor_total'].dropna()
    vendas_b2b = df_p3[df_p3['segmento'] == 'B2B']['valor_total'].dropna()

    t_stat, p_valor = stats.ttest_ind(vendas_b2c, vendas_b2b, equal_var=False)

    ticket_segmento = pd.DataFrame([
        {'segmento': 'B2C', 'ticket_medio': round(vendas_b2c.mean(), 2), 'volume_pedidos': len(vendas_b2c)},
        {'segmento': 'B2B', 'ticket_medio': round(vendas_b2b.mean(), 2), 'volume_pedidos': len(vendas_b2b)},
    ])
    ticket_segmento['diferenca_relevante'] = 'SIM' if p_valor < 0.05 else 'NÃO'
    ticket_segmento['p_value'] = round(p_valor, 4)

    print(ticket_segmento.to_string(index=False))

    ticket_segmento.to_csv('data/processed/p3_ticket_segmento.csv', index=False)
    print("  ✅ Exportado: p3_ticket_segmento.csv\n")

    # P4: Evolução Mensal 2023-2024
    print("--- P4: Evolução Mensal (2023-2024) ---")

    df_pedidos['data_pedido'] = pd.to_datetime(df_pedidos['data_pedido'], errors='coerce')

    evolucao_mensal = (
        df_pedidos
        .dropna(subset=['data_pedido'])
        .groupby(df_pedidos['data_pedido'].dt.to_period('M'))
        .size()
        .reset_index()
    )
    evolucao_mensal.columns = ['mes', 'volume_pedidos']
    evolucao_mensal['mes'] = evolucao_mensal['mes'].astype(str)

    print(evolucao_mensal.to_string(index=False))

    evolucao_mensal.to_csv('data/processed/p4_evolucao_mensal.csv', index=False)
    print("  ✅ Exportado: p4_evolucao_mensal.csv\n")

    # P5: Canais de Aquisição — Cancelamentos e Ticket Médio
    print("--- P5: Canais de Aquisição (Cancelamentos e Ticket) ---")

    total_por_canal = df_p3.groupby('canal_aquisicao').size()
    cancelados = df_p3[df_p3['status'].str.contains('Cancelado', case=False, na=False)]
    canc_por_canal = cancelados.groupby('canal_aquisicao').size()

    cancelamento_canal = pd.DataFrame({
        'canal_aquisicao': total_por_canal.index,
        'total_pedidos': total_por_canal.values,
        'pedidos_cancelados': canc_por_canal.reindex(total_por_canal.index, fill_value=0).values,
    })
    cancelamento_canal['taxa_cancelamento_pct'] = (
        cancelamento_canal['pedidos_cancelados'] / cancelamento_canal['total_pedidos'] * 100
    ).round(2)

    ticket_canal = df_p3.groupby('canal_aquisicao')['valor_total'].mean().round(2).reset_index()
    ticket_canal.columns = ['canal_aquisicao', 'ticket_medio']

    canais_consolidado = pd.merge(cancelamento_canal, ticket_canal, on='canal_aquisicao')
    canais_consolidado = canais_consolidado.sort_values('taxa_cancelamento_pct', ascending=False)

    print(canais_consolidado.to_string(index=False))

    canais_consolidado.to_csv('data/processed/p5_cancelamento_canal.csv', index=False)
    print("  ✅ Exportado: p5_cancelamento_canal.csv\n")

    print("==================================================\n")