import os
import time
import pandas as pd
from github import Github, GithubException

# Lista de tokens do GitHub
tokens = [
    "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",
    "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",
    "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"
]
current_token_index = 0

# Caminho da pasta Database
csv_dir = '../Database'
os.makedirs(csv_dir, exist_ok=True)

# Lista de palavras relacionadas a UX
ux_labels = [
    "Experiência do Cliente", "Customer Experience",
    "Usabilidade", "Usability",
    "Interação com o Usuário", "User Interaction",
    "Design Centrado no Usuário", "User-Centered Design",
    "Experiência Interativa", "Interactive Experience",
    "Experiência Digital", "Digital Experience",
    "Interface do Usuário", "User Interface",
    "Navegabilidade", "Navigability",
    "Fluidez de Interação", "Interaction Fluidity",
    "Satisfação do Usuário", "User Satisfaction"
]


def get_github_instance():
    """ Retorna a instância do GitHub com o token atual """
    global current_token_index
    return Github(tokens[current_token_index])


def switch_token():
    """ Troca para o próximo token disponível """
    global current_token_index
    current_token_index = (current_token_index + 1) % len(tokens)
    print(f"Switching to token {current_token_index + 1}")


def analyze_forks_with_rate_limit_handling(repo_name):
    """ Analisa os forks de um repositório e identifica commits relacionados a UX """
    global current_token_index
    g = get_github_instance()

    ux_contributions = []

    while True:
        try:
            # Tentar acessar o repositório
            repo = g.get_repo(repo_name)
            forks = repo.get_forks()

            # Iterar sobre os forks e analisar os commits focados em UX
            for fork in forks:
                print(f"Analyzing fork: {fork.full_name}")
                commits = fork.get_commits()
                ux_related_commits = 0

                for commit in commits:
                    commit_message = commit.commit.message.lower()

                    # Verificar se algum termo relacionado a UX está na mensagem do commit
                    if any(label.lower() in commit_message for label in ux_labels):
                        ux_related_commits += 1

                ux_contributions.append({
                    'fork': fork.full_name,
                    'ux_related_commits': ux_related_commits
                })

            return ux_contributions

        except GithubException as e:
            if e.status == 403 and "rate limit" in str(e).lower():
                # Se o limite foi atingido, trocar de token e aguardar
                print(
                    "Rate limit exceeded. Switching token and waiting for 60 seconds...")
                switch_token()
                # Aguardar 60 segundos antes de tentar novamente
                time.sleep(60)
                g = get_github_instance()
            else:
                raise e  # Levantar exceção se for outro tipo de erro

        except Exception as e:
            print(f"An error occurred: {e}")
            break


def save_fork_data_to_csv(fork_analysis, repo_name):
    """ Salva os dados de análise dos forks em um arquivo CSV """
    # Criar um DataFrame com os dados de análise
    df = pd.DataFrame(fork_analysis)

    # Caminho do arquivo CSV
    csv_filename = os.path.join(
        csv_dir, f'{repo_name.replace("/", "_")}_forks_ux_analysis.csv')

    # Salvar o DataFrame em um CSV
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")


# Exemplo de chamada para um repositório específico
repo_name = "mui/material-ui"
fork_analysis = analyze_forks_with_rate_limit_handling(repo_name)

# Salvar os resultados em um CSV
save_fork_data_to_csv(fork_analysis, repo_name)
