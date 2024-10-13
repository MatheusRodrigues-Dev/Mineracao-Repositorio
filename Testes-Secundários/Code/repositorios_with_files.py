import os
from github import Github
import pandas as pd

# Autenticação na API do GitHub
g = Github("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")  # Substitua pelo seu token do GitHub

# Lista de arquivos a serem verificados
files_to_check = [
    'package.json', 'package-lock.json', 'yarn.lock', 'webpack.config.js', 
    'vite.config.js', 'angular.json', 'tsconfig.json', 'babel.config.js', 
    '.babelrc', 'gatsby-config.js', 'nuxt.config.js', '.env'
]

# Função para verificar a presença dos arquivos no repositório
def check_files_in_repository(repo):
    repo_files = [file.path for file in repo.get_contents("")]  # Listar arquivos do repositório
    found_files = {file: False for file in files_to_check}  # Inicializar todos os arquivos como não encontrados
    
    for file in files_to_check:
        if file in repo_files:
            found_files[file] = True  # Marcar o arquivo como encontrado
    
    return found_files

# Criar o diretório se não existir
output_dir = '../Database/Segunda-Busca'
os.makedirs(output_dir, exist_ok=True)

# Carregar o arquivo CSV com os repositórios encontrados
input_csv = 'repos_found.csv'  # Substitua pelo nome do arquivo com seus repositórios
repos_df = pd.read_csv(input_csv)

# Adicionar colunas para cada arquivo a ser verificado
for file in files_to_check:
    repos_df[file] = False  # Inicializar as colunas como False

# Processar cada repositório e verificar os arquivos
for index, row in repos_df.iterrows():
    repo_name = row['name']  # Nome do repositório no GitHub
    
    try:
        repo = g.get_repo(repo_name)  # Obter o repositório
        found_files = check_files_in_repository(repo)  # Verificar os arquivos
        
        # Atualizar o DataFrame com os arquivos encontrados
        for file, found in found_files.items():
            repos_df.at[index, file] = found
        
        print(f"Arquivos verificados para o repositório: {repo_name}")
    except Exception as e:
        print(f"Erro ao acessar o repositório {repo_name}: {e}")

# Filtrar os repositórios que possuem pelo menos um dos arquivos
filtered_df = repos_df[repos_df[files_to_check].any(axis=1)]

# Caminho completo do arquivo CSV
output_csv = os.path.join(output_dir, 'repos_with_files.csv')

# Salvar o resultado em um novo arquivo CSV
filtered_df.to_csv(output_csv, index=False)

print(f"Resultados salvos em {output_csv}")
