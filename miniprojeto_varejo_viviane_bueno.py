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
#
