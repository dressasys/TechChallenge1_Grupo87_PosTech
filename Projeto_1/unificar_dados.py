import pandas as pd
import numpy as np

# Carregar todos os datasets
df_producao = pd.read_csv('Database/Producao.csv', sep=';')
df_comercializacao = pd.read_csv('Database/Comercializacao.csv', sep=';')
df_processamento = pd.read_csv('Database/Processamento.csv', sep=';')
df_exportacao = pd.read_csv('Database/Exportacao.csv', sep=';')
df_importacao = pd.read_csv('Database/Importacao.csv', sep=';')

# Função para transformar dados em formato longo
def transformar_para_longo(df, tipo_dado, anos_inicio=2009, anos_fim=2023):
    anos = [str(ano) for ano in range(anos_inicio, anos_fim + 1)]
    dados_longos = []
    
    for _, row in df.iterrows():
        for ano in anos:
            if ano in df.columns:
                valor = pd.to_numeric(row[ano], errors='coerce')
                if pd.notna(valor):
                    dados_longos.append({
                        'Tipo': tipo_dado,
                        'Ano': int(ano),
                        'Categoria': row.get('control', ''),
                        'Subcategoria': row.get('cultivar', ''),
                        'Pais': row.get('País', ''),
                        'Valor': valor
                    })
    
    return pd.DataFrame(dados_longos)

# Transformar cada dataset
print("Transformando dados...")
dados_producao = transformar_para_longo(df_producao, 'Producao')
dados_comercializacao = transformar_para_longo(df_comercializacao, 'Comercializacao')
dados_processamento = transformar_para_longo(df_processamento, 'Processamento')
dados_exportacao = transformar_para_longo(df_exportacao, 'Exportacao')
dados_importacao = transformar_para_longo(df_importacao, 'Importacao')

# Unificar todos os dados
dados_unificados = pd.concat([
    dados_producao,
    dados_comercializacao,
    dados_processamento,
    dados_exportacao,
    dados_importacao
], ignore_index=True)

# Limpar dados
dados_unificados = dados_unificados[dados_unificados['Valor'] > 0]
dados_unificados['Categoria'] = dados_unificados['Categoria'].fillna('')
dados_unificados['Subcategoria'] = dados_unificados['Subcategoria'].fillna('')
dados_unificados['Pais'] = dados_unificados['Pais'].fillna('')

# Salvar arquivo unificado
dados_unificados.to_csv('dados_vinhos_unificados.csv', index=False)

print(f"Dados unificados salvos! Total de registros: {len(dados_unificados)}")
print(f"Tipos de dados: {dados_unificados['Tipo'].unique()}")
print(f"Período: {dados_unificados['Ano'].min()}-{dados_unificados['Ano'].max()}")