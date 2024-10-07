from github import Github
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Lista de tokens do GitHub
tokens = [
    "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",
    "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",
    "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"
]

# Variável para manter o índice do token atual
current_token_index = 0

# Função para alternar o token


def get_next_token():
    global current_token_index
    current_token_index = (current_token_index + 1) % len(tokens)
    return tokens[current_token_index]


# Autenticação na API do GitHub com o primeiro token
g = Github(tokens[current_token_index])

ux_labels = [
    "Experiência do Cliente",  "Customer Experience",
    "Usabilidade",  "Usability",
    "Interação com o Usuário",  "User Interaction",
    "Design Centrado no Usuário",  "User-Centered Design",
    "Experiência Interativa",  "Interactive Experience",
    "Experiência Digital",  "Digital Experience",
    "Interface do Usuário",  "User Interface",
    "Navegabilidade",  "Navigability",
    "Fluidez de Interação",  "Interaction Fluidity",
    "Satisfação do Usuário",  "User Satisfaction"
]

# ux_labels = [
#     # Termos gerais
#     "ux", "user experience", "usability", "ui", "user interface", "design", "interaction design",
#     "human factors", "interaction", "visual design", "experience strategy", "service design",
#     "human-centered", "design principles", "design language", "branding", "identity design",

#     # Wireframes e fluxos
#     "wireflow", "wireframe", "mockup", "prototype", "user flow", "user journey",
#     "storybook", "sitemap", "user persona", "user scenario", "task flow",
#     "information architecture", "interaction flow", "design specification", "style guide",

#     # Pesquisa e análise
#     "user research", "usability testing", "a11y", "accessibility", "heuristics", "information architecture",
#     "contextual inquiry", "user interview", "survey", "analytics", "feedback",
#     "user testing", "A/B testing", "multivariate testing", "user feedback", "net promoter score",

#     # Métodos e ferramentas
#     "design thinking", "agile", "lean ux", "figma", "sketch", "adobe xd", "prototyping tools",
#     "co-design", "participatory design", "design systems", "invision", "axure", "justinmind",
#     "ux writing", "content strategy", "design ops", "service design tools", "ux metrics",

#     # Conceitos relacionados
#     "human-computer interaction", "user-centered design", "customer experience", "cx", "experience design",
#     "emotional design", "persuasive design", "gamification", "information design", "service blueprint",
#     "design innovation", "innovation design", "strategic design", "systemic design", "transitional design",

#     # Variações em inglês
#     "usercentereddesign", "uxdesign", "uxer", "iux", "uxui", "uiux",
#     "user experience design", "ux engineering", "interaction designer", "ux architect", "human-centered innovation",
#     "ux strategy", "ux design process", "ux best practices", "ux design principles", "ux design tools"
# ]

# ux_labels = ["ux", "user experience", "usability", "wireflow", "wireframe", "MVP"]
# Função para criar diretórios, caso não existam


def create_directories():
    if not os.path.exists('../Database'):
        os.makedirs('../Database')
    if not os.path.exists('../Image'):
        os.makedirs('../Image')


create_directories()


def search_ux_repositories():
    repos_data = []
    global g

    for label in ux_labels:
        search_query = f"{label} in:description"
        print(f"Buscando repositórios para: {label}")

        attempt = 0  # Contador de tentativas

        while attempt < len(tokens):  # Tentativas limitadas ao número de tokens
            try:
                repos = g.search_repositories(
                    query=search_query, sort="stars", order="desc")

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

                break  # Se a busca for bem-sucedida, saia do loop de tentativas

            except Exception as e:
                print(f"Erro ao buscar repositórios para o termo {label}: {e}")
                print("Tentando outro token...")
                g = Github(get_next_token())
                attempt += 1
                time.sleep(1)
                continue

        time.sleep(1)  # Para evitar limite de taxa da API

    # Remover duplicatas
    df = pd.DataFrame(repos_data).drop_duplicates(subset='name')
    df.to_csv('../Database/repositorios_ux.csv',
              index=False, sep=',', decimal=',')
    print("Coleta de repositórios concluída e salva no arquivo '../Database/repositorios_ux.csv'.")


search_ux_repositories()
