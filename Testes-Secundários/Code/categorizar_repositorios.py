import pandas as pd
import re
import unidecode

# Carregar dados
df = pd.read_csv('../Database/Segunda-Busca/repos_with_files.csv')

# Função para categorizar repositório


def categorize_repository(description):
    # Normalizar a descrição para minúsculas e remover acentuação
    description = str(description).lower()
    description = unidecode.unidecode(description)

    # Palavras-chave para categorização
    keywords = {
        "tool": ["tool", "framework", "library", "sdk", "api"],
        "application": ["application", "app", "mvp", "project", "software"],
        "ux": [
            "customer experience", "cx", "user experience",
            "usability", "ease of use", "usefulness",
            "user interaction", "human-computer interaction", "hci", "interaction design",
            "user-centered design", "ucd", "human-centered design", "hcd",
            "interactive experience", "interactive design", "user engagement",
            "digital experience", "online experience", "virtual experience",
            "user interface", "ui", "interface design", "ui design",
            "navigability", "navigation", "user navigation",
            "ux", "user experience", "ux design"
        ]
    }

    # Verificar palavras-chave de 'Tool'
    if any(re.search(rf'\b{kw}\b', description) for kw in keywords['tool']):
        if any(re.search(rf'\b{ux_kw}\b', description) for ux_kw in keywords['ux']):
            return "UX Tool"
        return "Tool"

    # Verificar palavras-chave de 'Application'
    if any(re.search(rf'\b{kw}\b', description) for kw in keywords['application']):
        if any(re.search(rf'\b{ux_kw}\b', description) for ux_kw in keywords['ux']):
            return "UX Application"
        return "Application"

    # Verificar se é relacionado a UX
    if any(re.search(rf'\b{ux_kw}\b', description) for ux_kw in keywords['ux']):
        return "UX Related"

    # Se não se enquadrar em nenhuma categoria
    return "Uncategorized"


# Aplicar a função de categorização
df['category'] = df['description'].apply(categorize_repository)

# Salvar o CSV categorizado na pasta Database
output_path = '../Database/Segunda-Busca/repositorios_categorizados.csv'
df.to_csv(output_path, index=False, sep=',', decimal=',')

print(f"Categorização concluída e salva em '{output_path}'.")
