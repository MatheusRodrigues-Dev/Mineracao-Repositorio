import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from langdetect import detect, DetectorFactory

# Configurar o gerador de números aleatórios para a detecção de idioma
DetectorFactory.seed = 0

# Verificar e criar pastas
if not os.path.exists("../Image"):
    os.makedirs("../Image")
if not os.path.exists("../Database"):
    os.makedirs("../Database")

# Criar DataFrame
df = pd.read_csv('../Database/repositorios_categorizados.csv')

# Função para detectar o idioma
def detect_language(text):
    if pd.isnull(text) or text.strip() == "":
        return "unknown"
    try:
        return detect(text)
    except Exception:
        return "unknown"

# Adicionar coluna de idioma
df['language_detected'] = df['description'].apply(detect_language)

# Salvar o DataFrame em CSV
# df.to_csv('../Database/repositories_data.csv', index=False)

# 1. Contagem de repositórios por linguagem detectada (filtrando valores menores que 10)
language_counts = df['language_detected'].value_counts()
language_counts_filtered = language_counts[language_counts >= 10]  # Filtrar valores menores que 10
language_counts_filtered.to_csv('../Database/language_counts.csv', index=True)

# Plotar contagem de linguagens filtrada
plt.figure(figsize=(10, 6))
sns.barplot(x=language_counts_filtered.index, y=language_counts_filtered.values)
plt.title('Contagem de Repositórios por Linguagem Detectada (≥ 10)')
plt.xlabel('Linguagem')
plt.ylabel('Número de Repositórios')
plt.xticks(rotation=45)
plt.savefig('../Image/language_counts.png')
plt.close()

# 2. Contagem de repositórios por categoria (filtrando valores menores que 10)
category_counts = df['category'].value_counts()
category_counts_filtered = category_counts[category_counts >= 10]  # Filtrar valores menores que 10
category_counts_filtered.to_csv('../Database/category_counts.csv', index=True)

# Plotar contagem de categorias filtrada
plt.figure(figsize=(10, 6))
sns.barplot(x=category_counts_filtered.index, y=category_counts_filtered.values)
plt.title('Contagem de Repositórios por Categoria (≥ 10)')
plt.xlabel('Categoria')
plt.ylabel('Número de Repositórios')
plt.xticks(rotation=45)
plt.savefig('../Image/category_counts.png')
plt.close()

# 3. Média de stars e forks por categoria
stars_by_category = df.groupby('category')['stars'].mean().sort_values(ascending=False)
stars_by_category.to_csv('../Database/stars_by_category.csv', index=True)

forks_by_category = df.groupby('category')['forks'].mean().sort_values(ascending=False)
forks_by_category.to_csv('../Database/forks_by_category.csv', index=True)

# 4. Top repositórios por stars e forks
top_stars = df[['name', 'stars', 'url']].sort_values(by='stars', ascending=False).head(5)
top_stars.to_csv('../Database/top_stars.csv', index=False)

top_forks = df[['name', 'forks', 'url']].sort_values(by='forks', ascending=False).head(5)
top_forks.to_csv('../Database/top_forks.csv', index=False)

# 5. Análise de Descrição (Word Cloud)
descriptions = ' '.join(df['description'].dropna())

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(descriptions)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud das Descrições dos Repositórios')
plt.savefig('../Image/wordcloud_descriptions.png')
plt.close()

# 6. Correlação entre Stars e Forks
correlation = df[['stars', 'forks']].corr()
correlation.to_csv('../Database/correlation_stars_forks.csv', index=True)

# Plotar relação entre Stars e Forks
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='stars', y='forks')
plt.title('Relação entre Stars e Forks')
plt.xlabel('Stars')
plt.ylabel('Forks')
plt.savefig('../Image/stars_vs_forks.png')
plt.close()

print("Análises concluídas. Dados salvos nas pastas '../Image' e '../Database'.")
