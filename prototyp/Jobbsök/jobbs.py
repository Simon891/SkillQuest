import nltk
import pandas as pd
from gensim import corpora, models, similarities

# Read the CSV file into a pandas DataFrame
max_rows = 5000
data = pd.read_csv("job_listings.csv", on_bad_lines='skip', nrows=max_rows)

# Extract the "description.text" and "occupation.label" columns from the DataFrame
documents = data['description.text'].tolist()
occupations = data['occupation.label'].tolist()

# Tokenize the documents
tokenized_docs = [nltk.word_tokenize(doc.lower()) for doc in documents]

# Create a dictionary from the tokenized documents
dictionary = corpora.Dictionary(tokenized_docs)

# Create a TF-IDF representation of the documents
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Build an index
index = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=len(dictionary))

while True:
    # Define an input word/query
    query = input()

    # Preprocess the query
    tokenized_query = nltk.word_tokenize(query.lower())

    # Convert the query to a TF-IDF representation
    query_bow = dictionary.doc2bow(tokenized_query)
    query_tfidf = tfidf[query_bow]

    # Calculate document similarities
    sims = index[query_tfidf]

    # Get the index of the best match
    best_match_index = sims.argmax()

    # Retrieve the best matching document and its corresponding occupation
    best_match_document = documents[best_match_index]
    best_match_occupation = occupations[best_match_index]

    # Display the best matching occupation label
    print(f"Best matching occupation: {best_match_occupation}")
