import nltk
import pandas as pd
from gensim import corpora, models, similarities

def hitta_job():
    # Define input words/queries
    query = input("Enter multiple words separated by spaces: ")

    # Preprocess the query
    tokenized_query = nltk.word_tokenize(query.lower())

    # Convert the query to a TF-IDF representation
    query_bow = dictionary.doc2bow(tokenized_query)
    query_tfidf = tfidf[query_bow]

    # Calculate document similarities
    sims = index[query_tfidf]

    # Get the indices of the top 10 matches (in descending order)
    top_10_indices = sims.argsort()[::-1][:10]

    # Retrieve the top 10 matching documents and their corresponding occupations
    top_10_documents = [documents[i] for i in top_10_indices]
    unique_occupations = []
    for i in top_10_indices:
        occupation = occupations[i]
        if occupation not in unique_occupations:
            unique_occupations.append(occupation)

    # Display the top 10 matching occupation labels
    print("Top 10 matching occupations:")
    for occupation in unique_occupations:
        print(f"Occupation: {occupation}")


# Read the CSV file into a pandas DataFrame
max_rows = 100
data = pd.read_csv("job_listings.csv", on_bad_lines='skip', nrows=max_rows)

# Extract the "description.text" and "occupation.label" columns from the DataFrame
documents = data['description.text'].tolist()
occupations = data['occupation.label'].tolist()

# Tokenize the documents
tokenized_docs = [nltk.word_tokenize(doc.lower()) for doc in documents]

# Create a dictionary from the tokenized documents
dictionary = corpora.Dictionary(tokenized_docs)

# Create a corpus
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Train the TF-IDF model on the corpus
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Build an index
index = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=len(dictionary))

hitta_job()