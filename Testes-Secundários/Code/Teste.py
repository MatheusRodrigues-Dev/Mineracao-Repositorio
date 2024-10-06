from github import Github

label = 'ux'
search_query = f"{label} in:description"
print(f"Buscando repositórios para: {label}")
g = Github('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')

repos_data = []
repos = g.search_repositories(query=search_query, sort="stars", order="desc")
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

print(repos_data)
