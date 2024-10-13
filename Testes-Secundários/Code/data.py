import pandas as pd

# Carregue a tabela
df = pd.read_csv('../Database/Segunda-Busca/repositorios_categorizados.csv')

# Formate as colunas "created_at" e "updated_at" como datas
df['created_at'] = pd.to_datetime(df['created_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Formate as datas como "YYYY-MM-DD"
df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d')
df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d')

# Imprima a tabela formatada
print(df)

df.to_csv('../Database/Segunda-Busca/repositories.csv', index=False, sep=',', decimal=',')