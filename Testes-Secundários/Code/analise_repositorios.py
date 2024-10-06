import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from langdetect import detect, DetectorFactory

# Configurações iniciais
DetectorFactory.seed = 0

# Verificar e criar pastas
output_dir = '../'
image_dir = os.path.join(output_dir, 'Image')
database_dir = os.path.join(output_dir, 'Database')

if not os.path.exists(image_dir):
    os.makedirs(image_dir)
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# Carregar dados
df = pd.read_csv(os.path.join(database_dir, 'repositorios_categorizados.csv'))

# Função para detectar idioma
def detect_language(text):
    if pd.isnull(text) or text.strip() == "":
        return "unknown"
    try:
        return detect(text)
    except Exception:
        return "unknown"

# Adicionar coluna de idioma
df['language_detected'] = df['description'].apply(detect_language)

# Salvar dados
df.to_csv(os.path.join(database_dir, 'repositories_data.csv'), index=False)

# Função para plotar gráficos de barras
def plot_bar_chart(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=data.index, y=data.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(image_dir, filename))
    plt.close()

# Função para plotar gráficos de dispersão
def plot_scatter_plot(data, x, y, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(os.path.join(image_dir, filename))
    plt.close()

# 1. Contagem de repositórios por linguagem detectada (filtrando valores menores que 10)
language_counts = df['language_detected'].value_counts()
language_counts_filtered = language_counts[language_counts >= 10]

# Salvar dados
language_counts_filtered.to_csv(os.path.join(database_dir, 'language_counts.csv'), index=True)

# Plotar contagem de linguagens filtrada
plot_bar_chart(language_counts_filtered, 'Contagem de Repositórios por Linguagem Detectada (≥ 10)', 'Linguagem', 'Número de Repositórios', 'language_counts.png')

# 2. Contagem de repositórios por categoria (filtrando valores menores que 10)
category_counts = df['category'].value_counts()
category_counts_filtered = category_counts[category_counts >= 10]

# Salvar dados
category_counts_filtered.to_csv(os.path.join(database_dir, 'category_counts.csv'), index=True)

# Plotar contagem de categorias filtrada
plot_bar_chart(category_counts_filtered, 'Contagem de Repositórios por Categoria (≥ 10)', 'Categoria', 'Número de Repositórios', 'category_counts.png')

# 3. Média de stars e forks por categoria
stars_by_category = df.groupby('category')['stars'].mean().sort_values(ascending=False)
forks_by_category = df.groupby('category')['forks'].mean().sort_values(ascending=False)

# Salvar dados
stars_by_category.to_csv(os.path.join(database_dir, 'stars_by_category.csv'), index=True)
forks_by_category.to_csv(os.path.join(database_dir, 'forks_by_category.csv'), index=True)

# 4. Top repositórios por stars e forks
top_stars = df[['name', 'stars', 'url']].sort_values(by='stars', ascending=False).head(5)
top_forks = df[['name', 'forks', 'url']].sort_values(by='forks', ascending=False).head(5)

# Salvar dados
top_stars.to_csv(os.path.join(database_dir, 'top_stars.csv'), index=False)
top_forks.to_csv(os.path.join(database_dir, 'top_forks.csv'), index=False)

# 5. Análise de Descrição (Word Cloud)
descriptions = ' '.join(df['description'].dropna())

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(descriptions)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud das Descrições dos Repositórios')
plt.savefig(os.path.join(image_dir, 'wordcloud_descriptions.png'))
plt.close()

# 6. Correlação entre Stars e Forks
correlation = df[['stars', 'forks']].corr()

# Salvar dados
correlation.to_csv(os.path.join(database_dir, 'correlation.csv'), index=False)