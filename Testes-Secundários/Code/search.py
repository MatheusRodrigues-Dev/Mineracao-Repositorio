from github import Github
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Autenticação na API do GitHub
g = Github("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")

ux_labels = [
    # Termos gerais
    "ux", "user experience", "usability", "ui", "user interface", "design", "interaction design",
    "human factors", "interaction", "visual design", "experience strategy", "service design",
    "human-centered", "design principles", "design language", "branding", "identity design",

    # Wireframes e fluxos
    "wireflow", "wireframe", "mockup", "prototype", "user flow", "user journey",
    "storybook", "sitemap", "user persona", "user scenario", "task flow",
    "information architecture", "interaction flow", "design specification", "style guide",

    # Pesquisa e análise
    "user research", "usability testing", "a11y", "accessibility", "heuristics", "information architecture",
    "contextual inquiry", "user interview", "survey", "analytics", "feedback",
    "user testing", "A/B testing", "multivariate testing", "user feedback", "net promoter score",

    # Métodos e ferramentas
    "design thinking", "agile", "lean ux", "figma", "sketch", "adobe xd", "prototyping tools",
    "co-design", "participatory design", "design systems", "invision", "axure", "justinmind",
    "ux writing", "content strategy", "design ops", "service design tools", "ux metrics",

    # Conceitos relacionados
    "human-computer interaction", "user-centered design", "customer experience", "cx", "experience design",
    "emotional design", "persuasive design", "gamification", "information design", "service blueprint",
    "design innovation", "innovation design", "strategic design", "systemic design", "transitional design",

    # Variações em inglês
    "usercentereddesign", "uxdesign", "uxer", "iux", "uxui", "uiux",
    "user experience design", "ux engineering", "interaction designer", "ux architect", "human-centered innovation",
    "ux strategy", "ux design process", "ux best practices", "ux design principles", "ux design tools"
]
# Lista de termos UX para busca
# ux_labels = ["ux", "user experience", "usability", "wireflow", "wireframe", "MVP"]

def search_ux_repositories():
    repos_data = []

    for label in ux_labels:
        search_query = f"{label} in:description"
        print(f"Buscando repositorios para: {label}")

        try:
            for page in range(1, 11):  # Ajuste o número de páginas conforme necessário
                repos = g.search_repositories(query=search_query, sort="stars", order="desc", page=page)

                for repo in repos:
                    repo_data = {
                        "name": repo.full_name,
                        "description": repo.description,
                        "stars": repo.stargazers_count,
                        "language": repo.language,
                        "forks": repo.forks_count,
                        "url": repo.html_url,
                        "created_at": repo.created_at,
                        "updated_at": repo.updated_at
                    }
                    repos_data.append(repo_data)

                time.sleep(1)  # Para evitar limite de taxa da API

        except Exception as e:
            print(f"Erro ao buscar repositorios para o termo {label}: {e}")

    # Salvar os dados em um arquivo CSV
    df = pd.DataFrame(repos_data)
    df.to_csv('repositorios_ux.csv', index=False)
    print("Coleta de repositorios concluída e salva no arquivo 'repositorios_ux.csv'.")

search_ux_repositories()

def filter_repositories(input_csv):
    # Carregar os repositorios coletados
    df = pd.read_csv(input_csv)

    # Aplicar os critérios de filtragem
    filtered_df = df[(df['stars'] >= 5) & (df['forks'] >= 5)]
    print(f"{len(filtered_df)} repositorios encontrados após a filtragem.")

    # Salvar os repositorios filtrados em um novo CSV
    filtered_df.to_csv('repositorios_ux_filtrados.csv', index=False)
    print("repositorios filtrados salvos em 'repositorios_ux_filtrados.csv'.")

filter_repositories('repositorios_ux.csv')

def categorize_repository(description):
    keywords_tool = ["tool", "framework", "library", "sdk", "API"]
    keywords_application = ["application", "app", "MVP", "project"]

    description = str(description).lower()

    for keyword in keywords_tool:
        if keyword in description:
            return "Tool"

    for keyword in keywords_application:
        if keyword in description:
            return "Application"

    return "Uncategorized"

# Aplicar categorização
df = pd.read_csv('repositorios_ux_filtrados.csv')
df['category'] = df['description'].apply(categorize_repository)

df.to_csv('repositorios_categorizados.csv', index=False)
print("Categorização concluída e salva em 'repositorios_categorizados.csv'.")

def plot_stars_distribution(csv_file):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['stars'], bins=50, kde=True)

    plt.title('Distribuição de Stars nos repositorios de UX')
    plt.xlabel('Stars')
    plt.ylabel('Frequência')
    plt.show()

plot_stars_distribution('repositorios_categorizados.csv')