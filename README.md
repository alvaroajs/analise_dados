# 📦 NovaShop · Pipeline de Análise de Dados


---

## Contexto

A NovaShop é um e-commerce brasileiro com operações B2C e B2B que enfrenta um problema real: alta taxa de cancelamentos, devoluções crescentes e tickets de suporte sem causa raiz identificada. O objetivo deste projeto é transformar os dados brutos da empresa em evidências que expliquem esses padrões.

A análise cobre mais de **15.000 pedidos**, **3.000 clientes** e múltiplos canais de aquisição — tudo respondido via código Python e visualizado no Looker Studio.

---

## Estrutura do Projeto

```
metrics_extrator/
│
├── data/
│   ├── raw/                        # Bases originais (não versionadas)
│   │   ├── pedidos.csv
│   │   ├── clientes.csv
│   │   ├── itens_pedido.csv
│   │   ├── produtos.csv
│   │   └── tickets_suporte.csv
│   │
│   ├── interim/                    # Bases tratadas (geradas pelo pipeline)
│   │   ├── pedidos_clean.csv
│   │   ├── clientes_clean.csv
│   │   ├── itens_clean.csv
│   │   └── base_problemas_suporte.csv
│   │
│   └── processed/                  # Saídas finais para o BI
│       ├── visao_vendas_geografia.csv
│       ├── ranking_fornecedores_problema.csv
│       └── visao_lucratividade_categoria.csv
│
├── src/
│   ├── main.py                     # Ponto de entrada do pipeline
│   ├── limpeza_dados.py            # Q6 — Tratamento e qualidade dos dados
│   ├── respostas_case.py           # Q1 a Q5 — Respostas às perguntas do case
│   ├── metrics_financeiras.py      # BI — Visão geográfica de vendas
│   ├── metrics_qualidade.py        # BI — Ranking de fornecedores por chamados
│   └── metrics_lucratividade.py    # BI — Margem e lucratividade por categoria
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Como Rodar

### 1. Clone o repositório e entre na pasta

```bash
git clone <https://github.com/alvaroajs/analise_dados>
cd metrics_extrator
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione as bases de dados

Coloque os arquivos `.csv` originais dentro de `data/raw/` antes de rodar. As pastas `interim/` e `processed/` são criadas automaticamente pelo pipeline.

### 5. Execute o pipeline completo

```bash
python3 src/main.py
```

Ao finalizar, os arquivos de saída estarão em `data/processed/` — prontos para importar no Looker Studio.

---

## O que o Pipeline Faz

O `main.py` orquestra tudo em sequência:

1. **Limpeza dos dados** — remove nulos, corrige valores negativos e padroniza textos
2. **Respostas do case** — calcula as 5 métricas pedidas no PDF e imprime no terminal
3. **Geração de bases de BI** — cria 3 CSVs enriquecidos para uso em dashboards

---

## Perguntas do Case

### P1 — Volume de pedidos por status
Calculado com distribuição percentual. A maioria dos pedidos foi entregue com sucesso, mas a fatia de cancelados e devolvidos juntos ultrapassa 24% — um número expressivo que merece atenção.

### P2 — Top 10 produtos mais vendidos
Ranqueados por quantidade total de itens vendidos, com a receita gerada por cada um. Os produtos de **Esporte & Lazer** e **Eletrônicos** dominam o topo tanto em volume quanto em receita.

### P3 — Ticket médio B2C vs B2B
O ticket B2B é aproximadamente **6x maior** que o B2C. O teste estatístico (Welch's t-test) confirma que essa diferença não é por acaso — p-value ≈ 0.0000, ou seja, os dois segmentos se comportam de forma estruturalmente diferente e devem ser tratados com estratégias distintas.

### P4 — Evolução mensal 2023–2024
O volume mensal oscila em torno de 530–610 pedidos ao longo de quase todo o período — com uma única exceção: **novembro/2023 registrou mais de 2.300 pedidos**, claramente impulsionado pela Black Friday. Fora isso, não há sazonalidade forte, o que indica que a empresa ainda tem oportunidade de criar picos em outras datas estratégicas (Dia das Mães, volta às aulas, etc.).

### P5 — Canal de aquisição: cancelamentos e ticket médio
O canal **paid_search** apresenta uma taxa de cancelamento de ~30% — muito acima dos demais canais, que ficam na faixa de 11–12%. Isso sugere desalinhamento entre a promessa do anúncio e a experiência real de compra. Em contrapartida, **redes sociais** lidera em ticket médio, indicando uma base de clientes com maior poder de compra vinda desse canal.

### P6 — Qualidade dos dados
Foram identificadas e tratadas as seguintes inconsistências:

- Pedidos com `id` ou `cliente_id` nulos → removidos
- Valores `valor_total` negativos → convertidos para absoluto
- Campos de texto (`status`, `segmento`) com espaços e capitalização inconsistente → normalizados com `.strip()` e `.title()` / `.upper()`

---

## Bases Geradas para o BI 

O pipeline gera três visões consolidadas prontas para uso no Looker Studio:

| Arquivo | Conteúdo |
|---|---|
| `visao_vendas_geografia.csv` | Pedidos cruzados com dados de clientes (região, segmento, canal) |
| `ranking_fornecedores_problema.csv` | Fornecedores ranqueados por volume de tickets de suporte abertos |
| `visao_lucratividade_categoria.csv` | Faturamento, lucro bruto e margem percentual por categoria de produto |

---

## Dependências

```
numpy==2.4.4
pandas==3.0.2
scipy==1.15.3
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
six==1.17.0
```

---
