📋 Descrição do Projeto
O objetivo deste projeto é realizar uma análise de dados abrangente da base Varejo.csv. Isso envolveu:
Carregamento e inspeção inicial dos dados.
Diagnóstico de problemas como valores nulos, duplicatas e inconsistências.
Limpeza e tratamento dos dados, incluindo imputação de valores ausentes e ajuste de tipos.
Análise da estrutura de compras e validação de regras de negócio.
Estatística descritiva detalhada para a coluna de número de filhos.
Exploração de padrões através de agrupamentos por gênero e categoria de produto.
Geração de conclusões e insights com base nos achados.
📂 Estrutura dos Arquivos
plaintext
📁 Projeto_Analise_Varejo/
├── Varejo.csv              ← Base de dados original (bruta)
├── Varejo_Limpo.csv        ← Base tratada e limpa (gerada pelo código)
├── analise_varejo.py        ← Código completo em Python
└── README.md                ← Documentação do projeto (este arquivo)
🛠️ Tecnologias Utilizadas
Python 3 — Linguagem de programação principal.
Pandas — Biblioteca essencial para manipulação e análise de dados (DataFrame, leitura CSV, limpeza, agrupamentos, estatísticas).
NumPy — Usado para tratamento de valores nulos (np.nan) e operações numéricas.
Datetime — Módulo para manipulação de datas.
🔄 Etapas Realizadas no Código
🟦 ETAPA 1 — Carregamento e Visão Geral
Carregamento: A base Varejo.csv foi carregada utilizando pandas.read_csv, especificando encoding="utf-8" e sep=";".
Inspeção Inicial:
Número de registros (linhas): [Número de Linhas]
Número de colunas: [Número de Colunas]
Tipos de dados de cada coluna: Exibidos usando df.dtypes.
Primeiras 5 linhas: Visualizadas com df.head() para entender a estrutura.
🟦 ETAPA 2 — Diagnóstico de Qualidade
Foram identificados os seguintes problemas na base original:
Valores Nulos:
Contagem de nulos por coluna: Reportado usando df.isnull().sum().
Valores #N/D (String): Identificados e contados separadamente, indicando ausência de informação em algumas colunas, especialmente em produtos.
Duplicatas:
Número de linhas totalmente duplicadas: Reportado usando df.duplicated().sum().
Inconsistências:
Datas Inválidas: Verificadas através da conversão para datetime com errors="coerce", contando quantos valores resultaram em NaT (Not a Time).
Categorias Vazias (#N/D): Observado em colunas como PR_CAT e PR_NOME, indicando produtos sem classificação adequada.
🟦 ETAPA 3 — Limpeza e Ajuste de Tipos
Foram aplicadas as seguintes correções:
Remoção de Colunas Vazias: Colunas que continham apenas valores nulos (NaN ou #N/D) foram removidas usando df.dropna(axis=1, how='all').
Tratamento de #N/D: String #N/D foi substituída por np.nan para padronização.
Tratamento de Produto Específico: Para PR_ID == 107, PR_CAT e PR_NOME foram definidos como "SEM CATEGORIA" e "PRODUTO SEM CADASTRO", respectivamente.
Imputação de Nulos:
Escolha: Para colunas com menos de 5% de valores nulos, optou-se por preencher:
Colunas de texto (object): com a moda (valor mais frequente).
Colunas numéricas: com a mediana (valor central, menos sensível a outliers).
Colunas com mais de 5% de nulos foram mantidas com nulos para análise posterior.
Eliminação de Duplicatas: Linhas completamente idênticas foram removidas usando df.drop_duplicates().
Ajuste de Tipos de Dados:
Coluna DATA foi convertida para o tipo datetime usando pd.to_datetime(..., dayfirst=True, errors="coerce") para reconhecer o formato brasileiro (dia/mês/ano).
Salvamento: A base limpa foi salva em Varejo_Limpo.csv.
🟦 Validação da Regra de Compra
Confirmado que cada linha representa um item comprado, e não uma compra completa.
A coluna CO_ID (Código da Compra) foi utilizada para agrupar itens pertencentes à mesma transação, permitindo análises como:
Total de compras distintas (df.groupby('CO_ID').size().count()).
Média, máximo e mínimo de itens por compra.
🟦 ETAPA 4 — Estatística Descritiva (Número de Filhos)
Análise da coluna CL_FHL (Número de Filhos):
Total de clientes analisados (com informação de filhos): [Contagem de Filhos]
Média de filhos: [Média]
Mediana de filhos: [Mediana]
Moda de filhos: [Moda] (valor mais frequente)
Desvio Padrão: [Desvio Padrão]
Valor MÍNIMO: [Mínimo] filho(s)
Valor MÁXIMO: [Máximo] filhos
1º Quartil (25% dos clientes têm até): [Q1] filho(s)
3º Quartil (75% dos clientes têm até): [Q3] filho(s)
Distribuição percentual por quantidade de filhos: Detalhada na saída do script.
🟦 ETAPA 5 — Exploração de Padrões de Agrupamento
Agrupamento 1: Compras por Gênero do Cliente
Análise realizada agrupando por CL_GENERO e utilizando CO_ID para contar compras únicas.
Gênero com mais compras: [Gênero Líder] com [Quantidade de Compras] compras.
Média de itens por compra por gênero: [Valores calculados].
Agrupamento 2: Itens por Categoria de Produto
Análise realizada agrupando por PR_CAT e contando a quantidade de itens.
Categoria mais comprada: [Categoria Líder] com [Quantidade de Itens] itens.
Participação percentual das categorias: Detalhada na saída do script.
Agrupamento 3: Compras por Número de Filhos
Análise realizada agrupando por CL_FHL e contando compras únicas.
Perfil com mais compras: [Perfil Líder de Filhos] filho(s) com [Quantidade de Compras] compras.
💡 Principais Conclusões e Insights
Perfil de Compradores: O gênero [Gênero Líder] representa o público principal, com maior volume de compras. Recomenda-se focar campanhas e comunicação neste grupo.
Produtos em Destaque: A categoria [Categoria Líder] é a mais vendida, indicando ser o carro-chefe do faturamento. Categorias com pouca saída podem necessitar de revisão ou promoção.
Perfil Familiar: Clientes com 1 filho são o perfil mais frequente, embora o número total de compras tenda a diminuir à medida que o número de filhos aumenta.
Qualidade dos Dados: A limpeza foi crucial. Remoção de colunas vazias, eliminação de duplicatas e padronização de formatos (datas, #N/D) tornaram a base confiável.
Pontos de Atenção: Datas inválidas e o produto PR_ID=107 sem cadastro adequado são problemas que necessitam correção na origem dos dados para análises mais precisas.
Recomendações: Direcionar ofertas com base no perfil de clientes mais ativo; corrigir dados na fonte; e utilizar a base limpa para dashboards contínuos.
⚠️ Problemas Remanescentes e Limitações
Algumas datas não puderam ser interpretadas e permanecem como valor nulo, exigindo correção na fonte.
O produto PR_ID=107 foi categorizado como "SEM CATEGORIA", mas seu nome real precisa ser atualizado no cadastro de origem.
A imputação de nulos (moda/mediana) pode introduzir uma pequena distorção estatística, sendo uma aproximação aceitável devido à baixa proporção de nulos (<5%).
✅ Resultado Final
Ao final deste projeto, foram alcançados os seguintes resultados:
✅ Base de dados limpa e padronizada (Varejo_Limpo.csv).
✅ Entendimento do perfil de clientes e seus hábitos de compra.
✅ Identificação dos produtos e categorias mais relevantes.
✅ Relatório de conclusões com insights acionáveis e recomendações.
✅ Código documentado e reproduzível.
Projeto concluído como parte do curso de Análise de Dados. 🎓
plaintext

---

### 📌 Como usar este arquivo:
1.  **Copie TODO o conteúdo** acima (desde `# 🛒` até o final).
2.  Abra um editor de texto (como Bloco de Notas, VS Code, Sublime Text).
3.  **Cole todo o conteúdo** no arquivo.
4.  **Salve o arquivo com o nome exato:** `README.md`
    *   **Importante:** Certifique-se de que o nome seja `README.md` e não `README.md.txt`.
5.  Coloque este arquivo `README.md` na mesma pasta onde estão seu código Python e os arquivos CSV.

---

### 💡 Dica:
Substitua os colchetes `[Valor]` (como `[Número de Linhas]`, `[Gênero Líder]`, etc.) pelos **valores reais** que apareceram na saída do seu script Python quando você o executou. Assim, o README ficará totalmente personalizado com os resultados da sua análise!

Ficou perfeito assim? 😊
