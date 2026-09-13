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