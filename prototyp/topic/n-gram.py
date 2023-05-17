# -*- coding: utf-8 -*-
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.models.phrases import Phrases
from nltk.corpus import stopwords

# Read CSV file
data = pd.read_csv("job_listings.csv", on_bad_lines='skip')

# Extract the "description.text" column
documents = data["description.text"].tolist()

# Add custom stop words
swedish_stopwords = set(stopwords.words("swedish"))
swedish_stopwords.update(["du", "är", "med", "att", "och", "som", "en", "vi", "pa", "har", "inom", "dig", "av", "kommer"])  # Add additional stop words

# Preprocess the text data
def preprocess(text):
    # Tokenize the text into individual words
    tokens = simple_preprocess(text, deacc=True)

    # Remove stopwords
    tokens = [token for token in tokens if token not in swedish_stopwords]

    return tokens

# Apply preprocessing to each document
preprocessed_documents = [preprocess(doc) for doc in documents]

# Create n-gram models
ngram_documents = preprocessed_documents[:]  # Make a copy of preprocessed documents

ngram_models = []
n_values = [2, 3]  # Specify the n-gram values you want to extract, e.g., bigrams (2), trigrams (3), etc.

for n in n_values:
    model = Phrases(ngram_documents, min_count=5, threshold=100)
    ngram_models.append(model)
    ngram_documents = [model[doc] for doc in ngram_documents]

# Print the extracted n-grams
for i, n in enumerate(n_values):
    print(f"{n}-grams:")
    for doc in ngram_documents:
        ngrams = [gram for gram in doc if len(gram) == n]
        print(ngrams)

    print("\n")

