import pandas as pd

# Carregar dados
df = pd.read_csv('../Database/repositorios_ux_filtrados.csv')

def categorize_repository(description):
    # Palavras-chave para categorizar como 'Tool' e 'Application'
    keywords_tool = ["tool", "framework", "library", "sdk", "api"]
    keywords_application = ["application", "app", "mvp", "project", "software"]

    # Palavras-chave relacionadas a UX (em inglês e português)
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

    # Converter a descrição para minúsculas
    description = str(description).lower()

    # Verificar se a descrição contém alguma palavra-chave de 'Tool'
    for keyword in keywords_tool:
        if keyword in description:
            # Verificar se também contém palavras relacionadas a UX
            for ux_keyword in ux_labels:
                if ux_keyword in description:
                    return "UX Tool"
            return "Tool"

    # Verificar se a descrição contém alguma palavra-chave de 'Application'
    for keyword in keywords_application:
        if keyword in description:
            # Verificar se também contém palavras relacionadas a UX
            for ux_keyword in ux_labels:
                if ux_keyword in description:
                    return "UX Application"
            return "Application"

    # Verificar se contém apenas palavras relacionadas a UX (mas não 'Tool' ou 'Application')
    for ux_keyword in ux_labels:
        if ux_keyword in description:
            return "UX Related"

    # Se não se enquadrar em nenhuma categoria
    return "Uncategorized"

df['category'] = df['description'].apply(categorize_repository)

# Salvar o CSV categorizado na pasta Database
df.to_csv('../Database/repositorios_categorizados.csv', index=False, sep=',', decimal=',')
print("Categorização concluída e salva em '../Database/repositorios_categorizados.csv'.")
