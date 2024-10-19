import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from langdetect import detect, DetectorFactory

# Configurar o gerador de números aleatórios para a detecção de idioma
DetectorFactory.seed = 0

# Verificar e criar pastas
if not os.path.exists("../Database/Segunda-Busca"):
    os.makedirs("../Database/Segunda-Busca")

df = pd.read_csv('../Database/Segunda-Busca/repositorios_ux.csv')

# Função para detectar o idioma
def detect_language(text):
    if pd.isnull(text) or text.strip() == "":
        return "unknown"
    try:
        return detect(text)
    except Exception:
        return "unknown"

# Adicionar coluna de idioma
df['language_detected'] = df['description'].apply(detect_language)

# Salvar o DataFrame em CSV
df.to_csv('../Database/Segunda-Busca/repositories_data.csv', index=False)