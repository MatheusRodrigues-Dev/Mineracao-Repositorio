# Mineração de Repositórios - Foco em UX

Este projeto utiliza técnicas de mineração de repositórios de software para investigar e melhorar a experiência do usuário (UX) no desenvolvimento de projetos de software. O objetivo é identificar padrões e práticas de UX aplicadas em projetos.

Este trabalho foi desenvolvido como parte da disciplina de **Tópicos em Engenharia de Sistemas de Software 1**.

## Objetivo

A mineração de repositórios oferece uma maneira de analisar grandes quantidades de dados de projetos de software para extrair informações valiosas. Neste projeto, buscamos explorar como as práticas de UX são integradas nos projetos de software e como isso pode ajudar equipes de desenvolvimento a criar produtos mais eficientes, acessíveis e com melhor usabilidade.

## Funcionalidades

- Coleta de dados de repositórios de software hospedados no GitHub.
- Análise de arquivos e commits relacionados a práticas de UX, protótipos, documentação de interface, etc.
- Extração de insights sobre o impacto de melhorias de UX no desenvolvimento de projetos.
- Geração de relatórios e visualizações que ajudam a entender como a UX é aplicada em diferentes repositórios.

# Bibliotecas Utilizadas

Este documento lista todas as bibliotecas utilizadas ao longo das discussões e implementações para a análise de UX em repositórios de código e outras funcionalidades.

## 1. GitHub API

### **PyGithub**
- **Descrição:** Uma biblioteca Python para acessar a API do GitHub de maneira conveniente.
- **Instalação:** 
    ```bash
    pip install PyGithub
    ```
- **Utilização:**
    - Utilizada para acessar dados de repositórios, forks, commits e arquivos relacionados a UX.
    - Exemplos de uso:
        ```python
        from github import Github
        g = Github("seu_token")
        repo = g.get_repo("repositorio/nome")
        forks = repo.get_forks()
        ```

## 2. Pandas

### **pandas**
- **Descrição:** Biblioteca poderosa para análise e manipulação de dados em Python, especialmente com dados tabulares (DataFrames).
- **Instalação:** 
    ```bash
    pip install pandas
    ```
- **Utilização:**
    - Utilizada para manipular dados de análise de forks e salvar os resultados em arquivos CSV.
    - Exemplos de uso:
        ```python
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv('caminho/arquivo.csv', index=False)
        ```

## 3. Seaborn

### **seaborn**
- **Descrição:** Biblioteca baseada no Matplotlib, utilizada para visualização de dados com gráficos estatísticos atraentes.
- **Instalação:**
    ```bash
    pip install seaborn
    ```
- **Utilização:**
    - Utilizada para gerar gráficos de barras com uma paleta de cores aprimorada.
    - Exemplos de uso:
        ```python
        import seaborn as sns
        sns.barplot(x=x_data, y=y_data, palette='viridis')
        ```

## 4. Matplotlib

### **matplotlib**
- **Descrição:** Biblioteca padrão para criação de gráficos em Python.
- **Instalação:**
    ```bash
    pip install matplotlib
    ```
- **Utilização:**
    - Utilizada para gerar gráficos e personalizar visualizações de dados.
    - Exemplos de uso:
        ```python
        import matplotlib.pyplot as plt
        plt.plot(x_data, y_data)
        plt.show()
        ```

## 5. Os

### **os**
- **Descrição:** Biblioteca padrão do Python para interações com o sistema operacional, como manipulação de arquivos e diretórios.
- **Instalação:** Não é necessária, faz parte da biblioteca padrão do Python.
- **Utilização:**
    - Utilizada para criar diretórios e manipular caminhos de arquivos.
    - Exemplos de uso:
        ```python
        import os
        os.makedirs('diretorio', exist_ok=True)
        ```

## 6. Time

### **time**
- **Descrição:** Biblioteca padrão do Python para manipulação de funções relacionadas ao tempo.
- **Instalação:** Não é necessária, faz parte da biblioteca padrão do Python.
- **Utilização:**
    - Utilizada para inserir atrasos entre as requisições para respeitar o limite da API do GitHub.
    - Exemplos de uso:
        ```python
        import time
        time.sleep(60)  # Aguardar 60 segundos
        ```

## 7. Exception Handling

### **exception handling** (nativo do Python)
- **Descrição:** Mecanismo nativo do Python para tratamento de exceções.
- **Instalação:** Não é necessária, faz parte da biblioteca padrão do Python.
- **Utilização:**
    - Utilizada para capturar exceções de limite de requisições e outras falhas na API.
    - Exemplos de uso:
        ```python
        try:
            # Código que pode lançar uma exceção
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        ```

## 8. CSV

### **pandas CSV Handling**
- **Descrição:** Utilizado o módulo `to_csv` do `pandas` para salvar dados em formato CSV.
- **Instalação:** Integrado ao `pandas`.
- **Utilização:**
    - Para salvar os dados analisados em um arquivo CSV:
        ```python
        df.to_csv('caminho/arquivo.csv', index=False)
        ```

---

Essas são as principais bibliotecas utilizadas para o desenvolvimento e análise no projeto discutido.


## Como Executar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/MatheusRodrigues-Dev/Mineracao-Repositorio.git
