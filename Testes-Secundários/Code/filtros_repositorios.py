import pandas as pd

# Carregar dados
df = pd.read_csv('C:/Users/smart/Desktop/Matheus/Codigo-Git/Mineracao-Repositorio/Testes-Secundários/Database/repositorios_data.csv')

# Filtro 1: Estrelas maiores que 5
df = df[df['stars'] > 5]

# Filtro 2: Forks maiores que 5
df = df[df['forks'] > 5]

# Filtro 3: Idioma em inglês ou português
df = df[df['language_detected'].isin(['en', 'pt'])]

# Filtro 4: Data de criação nos últimos 10 anos
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')  # Converter a coluna para datetime
ten_years_ago = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=10)  # Comparar com timezone UTC
df = df[df['created_at'] > ten_years_ago]

# Filtro 5: Nome e descrição não nulos e não vazios
df = df[(df['name'].notna()) & (df['description'].notna()) & 
        (df['name'].str.strip() != '') & (df['description'].str.strip() != '')]

# Verificar se o DataFrame está vazio após os filtros
if df.empty:
    print("Nenhum repositório atende aos critérios de filtro.")
else:
    # Salvar o DataFrame filtrado
    df.to_csv('C:/Users/smart/Desktop/Matheus/Codigo-Git/Mineracao-Repositorio/Testes-Secundários/Database/repositorios_ux_filtrados2.csv',
              index=False, sep=',', decimal=',')
    print("Repositórios filtrados com sucesso.")

    # Exemplo de resumo de dados filtrados
    print(df.describe())

    # Adicione aqui mais análises conforme necessário