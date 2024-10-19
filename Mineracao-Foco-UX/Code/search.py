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

ux_labels = {
    "Customer Experience", "CX", "User Experience",
    "Usability", "Ease of Use", "Usefulness",
    "User Interaction", "Human-Computer Interaction", "HCI", "Interaction Design",
    "User-Centered Design", "UCD", "Human-Centered Design", "HCD",
    "Interactive Experience", "Interactive Design", "User Engagement",
    "Digital Experience", "Online Experience", "Virtual Experience",
    "User Interface", "UI", "Interface Design", "UI Design",
    "Navigability", "Navigation", "User Navigation",
    "UX", "User Experience", "UX Design"
}


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
                        "updated_at": repo.updated_at,
                        "open_issues": repo.open_issues_count,
                        "default_branch": repo.default_branch,
                        "contributors_count": repo.get_contributors().totalCount,
                        "commits_count": repo.get_commits().totalCount,
                        "topics": repo.get_topics(),
                        "watchers": repo.watchers_count,
                        "size": repo.size,
                        "has_wiki": repo.has_wiki,
                        "has_projects": repo.has_projects,
                        "has_issues": repo.has_issues,
                        "has_pages": repo.has_pages,
                        "releases_count": repo.get_releases().totalCount
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
    df.to_csv('../Database/Segunda-Busca/repositorios_ux.csv',
              index=False, sep=',', decimal=',')
    print("Coleta de repositórios concluída e salva no arquivo '../Database/repositorios_ux.csv'.")


search_ux_repositories()
