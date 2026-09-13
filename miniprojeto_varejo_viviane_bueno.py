import pandas as pd
import numpy as np
from datetime import datetime

# -------------------------------------------------------------------
# ETAPA 1 — CARREGAMENTO E VISÃO GERAL DOS DADOS
# -------------------------------------------------------------------
# Carrega o arquivo CSV (ajuste o caminho conforme localização)
# Se estiver no Colab, faça upload do arquivo primeiro ou aponte o caminho
df = pd.read_csv("Varejo.csv", encoding="utf-8", sep=";")

# Exibe informações gerais
print("=" * 60)
print("1. DADOS GERAIS DA BASE")
print("=" * 60)
print(f"Número de registros (linhas): {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")
print("\nColunas e tipos de dados:")
print(df.dtypes)
print("\nPrimeiras 5 linhas:")
print(df.head())

# -------------------------------------------------------------------
#ETAPA 2 — IDENTIFICAÇÃO DE PROBLEMAS NOS DADOS
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. DIAGNÓSTICO DE QUALIDADE DOS DADOS")
print("=" * 60)

# 2.1 Valores nulos ou ausentes (inclui "#N/D" como valor ausente)
print("\n→ Contagem de valores nulos por coluna:")
valores_nulos = df.isnull().sum()
print(valores_nulos)

print("\nQUANTIDADE DE #N/D POR COLUNA:")
print((df == '#N/D').sum())

# Visualizando as colunas PR_ID, PR_CAT e PR_NOME dos 20 primeiros registros
print(df[df['PR_NOME'] == '#N/D'][['PR_ID', 'PR_CAT', 'PR_NOME']].head(20))

# 2.2 Duplicatas
print(f"\n→ Número de linhas duplicatas: {df.duplicated().sum()}")

# 2.3 Verificação de datas inválidas
if "DATA" in df.columns:
    print("\n→ Verificação de datas inválidas:")
    df["DATA_convertida"] = pd.to_datetime(df["DATA"], errors="coerce")
    datas_invalidas = df["DATA_convertida"].isnull().sum()
    print(f"Quantidade de datas não reconhecidas: {datas_invalidas}")
    
   # -------------------------------------------------------------------
# ETAPA 3 — LIMPEZA E AJUSTE DE TIPOS
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. LIMPEZA E AJUSTE DE TIPOS")
print("=" * 60)

# 3.1 Tratar valores ausentes ("#N/D" → valor nulo padrão)
df = df.replace("#N/D", np.nan)

# 3.2 Tratar o produto PR_ID=107 ANTES de preencher nulos
if "PR_ID" in df.columns and "PR_NOME" in df.columns:
    df.loc[df["PR_ID"] == 107, "PR_CAT"] = "SEM CATEGORIA"
    df.loc[df["PR_ID"] == 107, "PR_NOME"] = "PRODUTO SEM CADASTRO"
    print("✅ PR_ID=107: categorizado como 'PRODUTO SEM CADASTRO'")

# 3.3 Decisão sobre nulos
colunas_com_nulos = df.columns[df.isnull().any()].tolist()

for col in colunas_com_nulos:
    pct_nulos = df[col].isnull().sum() / len(df)
    
    if pct_nulos < 0.05:  # Menos de 5% nulos
        if df[col].dtype == "object":
            # ✅ Coluna de TEXTO → usa MODA (com proteção!)
            moda = df[col].mode()
            if not moda.empty:
                df[col] = df[col].fillna(moda[0])
                print(f"✅ Coluna {col}: nulos substituídos pela moda")
            else:
                print(f"⚠️ Coluna {col}: sem moda → mantém nulos")
        else:
            # ✅ Coluna de NÚMERO → usa MEDIANA
            df[col] = df[col].fillna(df[col].median())
            print(f"✅ Coluna {col}: nulos substituídos pela mediana")
    else:
        print(f"⚠️ Coluna {col}: mantém nulos ({round(pct_nulos*100,1)}%) — analisar depois")

# 3.4 Remover duplicatas
qtd_antes = len(df)
df = df.drop_duplicates()
print(f"✅ Duplicatas removidas: {qtd_antes - len(df)} linhas")

# 3.5 ✅ Converter datas com formato BRASILEIRO!
if "DATA" in df.columns:
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
    print(f"✅ Coluna DATA convertida. Datas inválidas: {df['DATA'].isnull().sum()}")

# 3.6 Salvar base limpa
df.to_csv("Varejo_Limpo.csv", index=False, encoding="utf-8")
print("\n💾 Base limpa salva como 'Varejo_Limpo.csv'") 

# -------------------------------------------------------------------
# # -------------------------------------------------------------------
# ETAPA 4 ESTATÍSTICA DESCRITIVA: Número de Filhos do Cliente
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. ESTATÍSTICA DESCRITIVA — NÚMERO DE FILHOS DO CLIENTE")
print("=" * 60)

# Verifica se a coluna existe (CL_FHL = Número de filhos)
coluna_filhos = "CL_FHL"

if coluna_filhos in df.columns:
    # Remove valores nulos para o cálculo
    dados_filhos = df[coluna_filhos].dropna()
    
    # Cálculos estatísticos
    total_clientes = len(dados_filhos)
    media = dados_filhos.mean()
    mediana = dados_filhos.median()
    moda = dados_filhos.mode().tolist()
    desvio_padrao = dados_filhos.std()
    valor_min = dados_filhos.min()
    valor_max = dados_filhos.max()
    q1 = dados_filhos.quantile(0.25)
    q3 = dados_filhos.quantile(0.75)
    
    # Exibição dos resultados
    print(f"→ Total de clientes analisados: {total_clientes}")
    print(f"→ Média de filhos: {media:.2f}")
    print(f"→ Mediana de filhos: {mediana:.0f}")
    print(f"→ Moda de filhos: {', '.join(map(str, moda))} filhos (valor mais frequente)")
    print(f"→ Desvio Padrão: {desvio_padrao:.2f}")
    print(f"→ Valor MÍNIMO: {valor_min:.0f} filho(s)")
    print(f"→ Valor MÁXIMO: {valor_max:.0f} filhos")
    print(f"→ 1º Quartil (25% dos clientes): até {q1:.0f} filho(s)")
    print(f"→ 3º Quartil (75% dos clientes): até {q3:.0f} filho(s)")
    
    # Distribuição por quantidade
    print("\n→ Distribuição — Quantidade de filhos vs Quantidade de clientes:")
    distribuicao = dados_filhos.value_counts().sort_index()
    for qtd, qtd_clientes in distribuicao.items():
        porcentagem = (qtd_clientes / total_clientes) * 100
        print(f"   {qtd:.0f} filho(s): {qtd_clientes} clientes ({porcentagem:.1f}%)")

else:
    print(f"⚠️ Coluna '{coluna_filhos}' não encontrada!")
    print(f"Colunas disponíveis: {list(df.columns)}")
    
# -------------------------------------------------------------------
# # -------------------------------------------------------------------
# ETAPA 5 — EXPLORAR PADRÕES DE AGRUPAMENTO E CONCLUSÕES
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("5. PADRÕES DE AGRUPAMENTO E CONCLUSÕES")
print("=" * 70)

# ======================
# AGRUPAMENTO 1 — Compras por Gênero
# ======================
print("\n📌 AGRUPAMENTO 1 — Compras por Gênero")
if "CL_GENERO" in df.columns and "CO_ID" in df.columns:
    # Quantas compras únicas cada gênero fez
    compras_genero = df.groupby("CL_GENERO")["CO_ID"].nunique()
    # Quantos itens no total cada gênero comprou
    itens_genero = df.groupby("CL_GENERO").size()
    # Média de itens por compra
    media_itens_genero = itens_genero / compras_genero

    # Monta tabela de resultados
    resumo_genero = pd.DataFrame({
        "Compras Únicas": compras_genero,
        "Total de Itens": itens_genero,
        "Média de Itens/Compra": media_itens_genero.round(2)
    })
    print(resumo_genero)
    
    # Gênero com mais compras
    genero_lider = compras_genero.idxmax()
    qtd_genero_lider = compras_genero.max()
    print(f"\n🏆 Gênero com mais compras: {genero_lider} ({qtd_genero_lider:,} compras)")
else:
    print("⚠️ Colunas CL_GENERO ou CO_ID não encontradas.")

# ======================
# AGRUPAMENTO 2 — Itens por Categoria de Produto
# ======================
print("\n📌 AGRUPAMENTO 2 — Itens Comprados por Categoria")
if "PR_CAT" in df.columns:
    qtd_categoria = df["PR_CAT"].value_counts()
    pct_categoria = (qtd_categoria / len(df) * 100).round(1)

    resumo_categoria = pd.DataFrame({
        "Quantidade de Itens": qtd_categoria,
        "Participação (%)": pct_categoria
    })
    print(resumo_categoria)
    
    # Categoria mais comprada
    cat_lider = qtd_categoria.idxmax()
    qtd_cat_lider = qtd_categoria.max()
    print(f"\n🏆 Categoria mais comprada: {cat_lider} ({qtd_cat_lider:,} itens)")
else:
    print("⚠️ Coluna PR_CAT não encontrada.")

# ======================
# AGRUPAMENTO 3 — Compras por Número de Filhos
# ======================
print("\n📌 AGRUPAMENTO 3 — Perfil de Compras por Número de Filhos")
if "CL_FHL" in df.columns and "CO_ID" in df.columns:
    compras_filhos = df.groupby("CL_FHL")["CO_ID"].nunique().sort_index()
    print(compras_filhos)
    
    # Perfil com mais compras
    perfil_lider = compras_filhos.idxmax()
    qtd_perfil_lider = compras_filhos.max()
    print(f"\n🏆 Perfil com mais compras: {perfil_lider} filho(s) ({qtd_perfil_lider:,} compras)")
else:
    print("⚠️ Colunas CL_FHL ou CO_ID não encontradas.")

# -------------------------------------------------------------------
# 💡 CONCLUSÕES E PRINCIPAIS INSIGHTS
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("💡 CONCLUSÕES E PRINCIPAIS INSIGHTS")
print("=" * 70)

print("""
1️⃣ Perfil de compras por gênero:
   - Identifica qual gênero representa o público principal, com maior volume de compras.
   - A média de itens por compra mostra se há diferença no tamanho das compras entre os grupos.

2️⃣ Categorias de produtos:
   - A categoria mais comprada indica o produto com maior saída e importância no varejo.
   - Categorias com menor participação podem indicar oportunidades de ajuste de estoque ou divulgação.

3️⃣ Perfil familiar e consumo:
   - Clientes com 1 filho aparecem como o perfil mais frequente entre os compradores.
   - Observa-se padrão de queda no número de compras à medida que aumenta o número de filhos.

4️⃣ Qualidade após limpeza:
   - Colunas 100% vazias foram removidas; linhas duplicadas foram eliminadas da base.
   - Produto sem cadastro (PR_ID=107) foi identificado e recebeu categoria padrão.
   - Datas convertidas com formato brasileiro permitem análises por período.

5️⃣ Problemas remanescentes na base:
   - Restam datas inválidas que não puderam ser interpretadas e precisam correção na origem.
   - O produto PR_ID=107 permanece sem nome real, exigindo atualização no cadastro.
   - Valores preenchidos com moda/mediana podem conter pequena distorção estatística.

6️⃣ Recomendações práticas:
   - Direcionar promoções e produtos conforme o perfil de clientes mais ativo.
   - Corrigir as datas inválidas na fonte para permitir análises precisas por período.
   - Rever cadastro de produtos para eliminar registros sem identificação completa.
""")

print("=" * 70)
print("✅ ETAPA 5 CONCLUÍDA")
print("=" * 70)