# 🛒 Análise e Tratamento de Dados — Base de Varejo
*Projeto Acadêmico | Curso de Análise de Dados*

---

## 📋 Descrição do Projeto
Este projeto consiste em um *processo completo de análise de dados*, desde o carregamento da base bruta até a geração de relatórios e insights. Trabalhamos com dados de compras de um varejo, aplicando técnicas de limpeza, tratamento de inconsistências, conversão de formatos, cálculos estatísticos e agrupamentos para extrair informações úteis.

O objetivo principal é demonstrar o fluxo de trabalho de um analista: *carregar → entender → limpar → analisar → concluir*.

---

## 📂 Estrutura dos Arquivos
📁 Projeto_Varejo/
├── Varejo.csv ← Base de dados original (bruta)
├── Varejo_Limpo.csv ← Base tratada e limpa (gerada pelo código)
├── analise_varejo.py ← Código completo em Python
└── README.md ← Documentação do projeto
---

## 🛠️ Tecnologias Utilizadas
- *Python 3* — Linguagem de programação
- *Pandas* → Leitura, manipulação e análise de dados
- *NumPy* → Tratamento de valores nulos e operações matemáticas

---

## 🔄 Etapas Realizadas no Código

### 🟦 ETAPA 1 — Carregamento e Visão Geral
- Leitura do arquivo CSV com codificação UTF-8 e separador ;
- Exibição de quantidade de linhas, colunas e tipos de dados
- Visualização das primeiras linhas para conhecer a estrutura

> *Objetivo:* Entender o tamanho e a organização dos dados antes de qualquer alteração.

---

### 🟦 ETAPA 2 — Diagnóstico de Qualidade
- Contagem de valores nulos por coluna
- Identificação de valores #N/D (ausentes)
- Verificação de registros sem cadastro (produto PR_ID=107)
- Contagem de linhas duplicadas
- Teste …
