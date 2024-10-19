import pandas as pd

# Carregar dados
df = pd.read_csv('../Database/Segunda-Busca/repos_with_files.csv')

# Definindo palavras-chave
tool_keywords = ['prototype', 'wireframe', 'ux tool', 'design system', 'testing tool', 'sketch', 'material design', 'roadmap', 'guide', 'skills', 'color scheme', 'color palette', 'visual design']
application_keywords = ['app', 'mobile', 'website', 'user-friendly', 'UI', 'application', 'UI/UX']
automation_keywords = ['bot', 'automation', 'whatsapp', 'interaction', 'customer service', 'media sending', 'ai', 'artificial intelligence']
component_keywords = ['UI Library', 'library', 'component', 'UI component', 'plugin', 'widget', 'ui kit', 'bootstrap', 'react', 'vue', 'angular', 'react native', 'tailwind css', 'unstyled', 'accessible ui']

# Definindo pesos para as palavras-chave
keyword_weights = {
    'Outra Classificação': 2,
    'Ferramenta UX': 1.5,
    'Componente UX': 1.2,
    'Aplicação UX': 1
}

def classify_repository(description, topics):
    description = str(description).lower() if pd.notna(description) else ''
    topics = str(topics).lower() if pd.notna(topics) else ''

    # Calcular pontuações para cada categoria
    scores = {}
    for category, keywords in [
        ('Outra Classificação', automation_keywords),
        ('Ferramenta UX', tool_keywords),
        ('Componente UX', component_keywords),
        ('Aplicação UX', application_keywords)
    ]:
        score = sum(1 for word in keywords if word in description or word in topics)
        scores[category] = score * keyword_weights[category]

    # Determinar a classificação com base na maior pontuação
    classification = max(scores, key=scores.get)

    return classification


# Aplicar a função de classificação
df['category'] = df.apply(lambda row: classify_repository(
    row['description'], row['topics']), axis=1)

# Filtrar os repositórios classificados
non_classified_df = df[df['category'] == 'Não classificado']
non_classified_df = df[df['category'] == 'Outra Classificação']
classified_df = df[df['category'] != 'Não classificado']
classified_df = df[df['category'] != 'Outra Classificação']

# Salvar os CSVs
non_classified_output_path = '../Database/Segunda-Busca/repositorios_nao_classificados.csv'
classified_output_path = '../Database/Segunda-Busca/repositorios_categorizados.csv'

non_classified_df.to_csv(non_classified_output_path, index=False, sep=',', decimal=',')
classified_df.to_csv(classified_output_path, index=False, sep=',', decimal=',')

print(f"Categorização concluída.")
print(f"Repositórios não classificados salvos em '{non_classified_output_path}'.")
print(f"Repositórios classificados salvos em '{classified_output_path}'.")
