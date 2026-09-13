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
# 