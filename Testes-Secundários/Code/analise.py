import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Load the CSV file
df = pd.read_csv('../Database/repositorios_categorizados.csv')

# Função para contar palavras-chave em todas as descrições


def total_keyword_count(df, keywords):
    total_counts = {keyword: 0 for keyword in keywords}
    for description in df['description']:
        for keyword in keywords:
            total_counts[keyword] += description.lower().count(keyword.lower())
    return total_counts

# Função para criar diretórios


def create_dirs(output_dir, image_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

# Função para salvar gráfico


def save_plot(fig, filename):
    fig.tight_layout()
    # Ajuste a resolução para melhorar a qualidade
    plt.savefig(filename, dpi=300)
    plt.close(fig)

# Função para criar histogramas


def plot_histogram(data, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Adiciona linhas de grade
    save_plot(fig, filename)

# Função para plotar gráficos de barras


def plot_bar_chart(x, y, hue, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(12, 7))
    # Usando Seaborn para uma paleta de cores melhor
    sns.barplot(x=x, y=y, hue=hue, palette='viridis', ax=ax, legend=False)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Adiciona linhas de grade
    save_plot(fig, filename)

# Função para exportar DataFrame para CSV


def export_to_csv(df, filename):
    df.to_csv(filename, index=False, sep=',', decimal=',')


# Palavras-chave de UX
ux_labels = [
    "experiência do cliente", "customer experience",
    "usabilidade", "usability",
    "interação com o usuário", "user interaction",
    "design centrado no usuário", "user-centered design",
    "experiência interativa", "interactive experience",
    "experiência digital", "digital experience",
    "interface do usuário", "user interface",
    "navegabilidade", "navigability",
    "fluidez de interação", "interaction fluidity",
    "satisfação do usuário", "user satisfaction"
]

# Contar total de palavras-chave
total_counts = total_keyword_count(df, ux_labels)

# Criar a pasta 'analises' e 'Image/analise' se não existirem
output_dir = '../Database/analises'
image_dir = '../Image/analise'
create_dirs(output_dir, image_dir)

# 1. Distribution of Stars and Forks
plot_histogram(df['stars'], 'Distribution of Stars', 'Stars',
               'Frequency', os.path.join(image_dir, 'stars_distribution.png'))
plot_histogram(df['forks'], 'Distribution of Forks', 'Forks',
               'Frequency', os.path.join(image_dir, 'forks_distribution.png'))

# Correlation analysis
corr_coef = df['stars'].corr(df['forks'])

# 2. Analysis by Language
lang_counts = df['language'].value_counts()

# Manter os 50 idiomas mais populares e somar os restantes como "Outros"
if len(lang_counts) > 50:
    other_count = lang_counts[50:].sum()
    lang_counts = lang_counts[:50]
    lang_counts['Outros'] = other_count

# Gráficos por Linguagem
plot_bar_chart(lang_counts.index, lang_counts.values, hue=None, title='Count of Repositories by Language',
               xlabel='Language', ylabel='Count', filename=os.path.join(image_dir, 'repositories_by_language.png'))


# Estrelas e Forks Médios por Linguagem
avg_stars_by_lang = df.groupby('language')['stars'].mean()
avg_forks_by_lang = df.groupby('language')['forks'].mean()

# Filtrar os valores com menos de 100 ocorrências e ordenar do maior para o menor
avg_stars_by_lang = avg_stars_by_lang[avg_stars_by_lang.index.map(
    df['language'].value_counts()) >= 30].sort_values(ascending=False)
avg_forks_by_lang = avg_forks_by_lang[avg_forks_by_lang.index.map(
    df['language'].value_counts()) >= 30].sort_values(ascending=False)

# Plotar os gráficos de estrelas
plot_bar_chart(avg_stars_by_lang.index, avg_stars_by_lang.values, hue=None, title='Average Stars by Language',
               xlabel='Language', ylabel='Average Stars', filename=os.path.join(image_dir, 'average_stars_by_language.png'))

# Plotar os gráficos de forks
plot_bar_chart(avg_forks_by_lang.index, avg_forks_by_lang.values, hue=None, title='Average Forks by Language',
               xlabel='Language', ylabel='Average Forks', filename=os.path.join(image_dir, 'average_forks_by_language.png'))


# 3. Temporal Analysis
creation_dates = pd.to_datetime(df['created_at'])
creation_year_counts = creation_dates.dt.year.value_counts()

recent_updates = pd.to_datetime(df['updated_at'])
recent_updates_counts = recent_updates.dt.year.value_counts()

# 3. Temporal Analysis
plot_bar_chart(creation_year_counts.index, creation_year_counts.values, hue=None, title='Creation Year Counts',
               xlabel='Year', ylabel='Count', filename=os.path.join(image_dir, 'creation_year_counts.png'))

plot_bar_chart(recent_updates_counts.index, recent_updates_counts.values, hue=None, title='Recent Updates Counts',
               xlabel='Year', ylabel='Count', filename=os.path.join(image_dir, 'recent_updates_counts.png'))

# 4. Categorization of Repositories
category_counts = df['category'].value_counts()
avg_stars_by_category = df.groupby('category')['stars'].mean()
avg_forks_by_category = df.groupby('category')['forks'].mean()

# Categorization of Repositories
plot_bar_chart(category_counts.index, category_counts.values, hue=None, title='Count of Repositories by Category',
               xlabel='Category', ylabel='Count', filename=os.path.join(image_dir, 'repositories_by_category.png'))

plot_bar_chart(avg_stars_by_category.index, avg_stars_by_category.values, hue=None, title='Average Stars by Category',
               xlabel='Category', ylabel='Average Stars', filename=os.path.join(image_dir, 'average_stars_by_category.png'))

plot_bar_chart(avg_forks_by_category.index, avg_forks_by_category.values, hue=None, title='Average Forks by Category',
               xlabel='Category', ylabel='Average Forks', filename=os.path.join(image_dir, 'average_forks_by_category.png'))


# Salvar cada análise em um arquivo CSV separado
export_to_csv(pd.DataFrame({'Correlation coefficient between stars and forks': [
              corr_coef]}), os.path.join(output_dir, 'correlation_coefficient.csv'))
export_to_csv(lang_counts.reset_index().rename(columns={
              'index': 'Language', 'language': 'Count of Repositories'}), os.path.join(output_dir, 'repositories_by_language.csv'))
export_to_csv(avg_stars_by_lang.reset_index().rename(columns={
              'language': 'Language', 'stars': 'Average Stars'}), os.path.join(output_dir, 'average_stars_by_language.csv'))
export_to_csv(avg_forks_by_lang.reset_index().rename(columns={
              'language': 'Language', 'forks': 'Average Forks'}), os.path.join(output_dir, 'average_forks_by_language.csv'))
export_to_csv(creation_year_counts.reset_index().rename(columns={
              'index': 'Year', 'created_at': 'Count'}), os.path.join(output_dir, 'creation_year_counts.csv'))
export_to_csv(recent_updates_counts.reset_index().rename(columns={
              'index': 'Year', 'updated_at': 'Count'}), os.path.join(output_dir, 'recent_updates_counts.csv'))
export_to_csv(category_counts.reset_index().rename(columns={
              'index': 'Category', 'category': 'Count of Repositories'}), os.path.join(output_dir, 'repositories_by_category.csv'))
export_to_csv(avg_stars_by_category.reset_index().rename(columns={
              'category': 'Category', 'stars': 'Average Stars'}), os.path.join(output_dir, 'average_stars_by_category.csv'))
export_to_csv(avg_forks_by_category.reset_index().rename(columns={
              'category': 'Category', 'forks': 'Average Forks'}), os.path.join(output_dir, 'average_forks_by_category.csv'))
