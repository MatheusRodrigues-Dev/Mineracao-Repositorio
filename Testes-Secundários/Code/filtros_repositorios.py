import pandas as pd

# Carregar dados
df = pd.read_csv('../Database/Segunda-Busca/repositories_data.csv')

# Filtro 1: Estrelas maiores que 5
df = df[df['stars'] > 10]

# Filtro 2: Forks maiores que 5
df = df[df['forks'] > 10]

# Filtro 3: Idioma em inglês
df = df[df['language_detected'].isin(['en'])]

# Filtro 4: Data de criação nos últimos 10 anos
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')  # Converter a coluna para datetime
ten_years_ago = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=10)  # Comparar com timezone UTC
df = df[df['created_at'] > ten_years_ago]

# Filtro 5: Converter a coluna 'updated_at' para o tipo datetime (caso ainda não esteja)
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Filtrar repositórios que foram atualizados em 2024
df = df[df['updated_at'].dt.year == 2024]

# Filtro 6: Nome e descrição não nulos e não vazios
df = df[(df['name'].notna()) & (df['description'].notna()) & 
        (df['name'].str.strip() != '') & (df['description'].str.strip() != '')]

# Verificar se o DataFrame está vazio após os filtros
if df.empty:
    print("Nenhum repositório atende aos critérios de filtro.")
else:
    # Salvar o DataFrame filtrado
    df.to_csv('../Database/Segunda-Busca/repositories_ux_filtrados.csv',
              index=False, sep=',', decimal=',')
    print("Repositórios filtrados com sucesso.")

    # Exemplo de resumo de dados filtrados
    print(df.describe())

    # Adicione aqui mais análises conforme necessário