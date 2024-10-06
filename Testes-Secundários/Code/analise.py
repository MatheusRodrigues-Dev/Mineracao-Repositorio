import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the CSV file
df = pd.read_csv('../Database/repositorios_categorizados.csv')

# 1. Distribution of Stars and Forks
plt.hist(df['stars'], bins=50)
plt.title('Distribution of Stars')
plt.xlabel('Stars')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['forks'], bins=50)
plt.title('Distribution of Forks')
plt.xlabel('Forks')
plt.ylabel('Frequency')
plt.show()

# Correlation analysis
corr_coef = df['stars'].corr(df['forks'])
print(f'Correlation coefficient between stars and forks: {corr_coef:.2f}')

# 2. Analysis by Language
lang_counts = df['language'].value_counts()
print('Count of repositories by language:')
print(lang_counts)

avg_stars_by_lang = df.groupby('language')['stars'].mean()
print('Average stars by language:')
print(avg_stars_by_lang)

avg_forks_by_lang = df.groupby('language')['forks'].mean()
print('Average forks by language:')
print(avg_forks_by_lang)

# 3. Temporal Analysis
creation_dates = pd.to_datetime(df['created_at'])
print('Creation dates:')
print(creation_dates.dt.year.value_counts())

recent_updates = pd.to_datetime(df['updated_at'])
print('Recent updates:')
print(recent_updates.dt.year.value_counts())

# 4. Categorization of Repositories
category_counts = df['category'].value_counts()
print('Count of repositories by category:')
print(category_counts)

avg_stars_by_category = df.groupby('category')['stars'].mean()
print('Average stars by category:')
print(avg_stars_by_category)

avg_forks_by_category = df.groupby('category')['forks'].mean()
print('Average forks by category:')
print(avg_forks_by_category)

# 5. Top Repositories
top_repos_by_stars = df.nlargest(3, 'stars')
print('Top repositories by stars:')
print(top_repos_by_stars)

top_repos_by_forks = df.nlargest(3, 'forks')
print('Top repositories by forks:')
print(top_repos_by_forks)

# 6. Analysis of Description
desc_words = df['description'].str.split().explode()
word_counts = Counter(desc_words)
print('Common keywords in descriptions:')
print(word_counts.most_common(10))