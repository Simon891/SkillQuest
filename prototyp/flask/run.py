import os
import nltk
import pandas as pd
from gensim import corpora, models, similarities
from flask import Flask, render_template, request, Markup, jsonify, flash, redirect, url_for
import pickle
import time
import topicS

def hitta_job(documents, occupations, dictionary, tfidf, index_obj, sokord):
    # Define input words/queries
    query = sokord

    # Preprocess the query
    tokenized_query = nltk.word_tokenize(query.lower())

    # Convert the query to a TF-IDF representation
    query_bow = dictionary.doc2bow(tokenized_query)
    query_tfidf = tfidf[query_bow]

    # Calculate document similarities
    sims = index_obj[query_tfidf]

    # Get the indices of the top 10 matches (in descending order)
    match_indices = sims.argsort()[::-1][:20]

    # Retrieve the top 10 matching documents and their corresponding occupations
    top_10_documents = [documents[i] for i in match_indices]
    unique_occupations = []
    for i in match_indices:
        occupation = occupations[i]
        if occupation not in unique_occupations:
            unique_occupations.append(occupation)

    # Return the top 10 matching occupation labels as a string with line breaks
    result_string = ""
    result_string += "\n".join(f"<div class='forslag'>{occupation}</div>" for occupation in unique_occupations)

    
    return result_string


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with your desired secret key


# Read the CSV file into a pandas DataFrame
print("Read the CSV file into a pandas DataFrame")
start_time_ladda_data = time.time()
max_rows = None
data = pd.read_csv("dataset/job_listings.csv", on_bad_lines='skip', nrows=max_rows)

# Extract the "description.text" and "occupation.label" columns from the DataFrame
print("Extract the 'description.text' and 'occupation.label' columns from the DataFrame")
documents = data['description.text'].tolist()
occupations = data['occupation.label'].tolist()

# Check if tokenized documents are already saved
print('Check if tokenized documents are already saved')
tokenized_docs_path = "tokenized.pkl"
if os.path.exists(tokenized_docs_path):
    # Load tokenized documents from file
    print('Load tokenized documents from file')
    with open(tokenized_docs_path, "rb") as file:
        tokenized_docs = pickle.load(file)
else:
    # Tokenize and remove stop words from the documents
    print('Tokenize the documents')
    swedish_stopwords = nltk.corpus.stopwords.words('swedish')
    custom_stopwords_path = "stopwords.txt"
    with open(custom_stopwords_path, "r", encoding="utf-8") as file:
        custom_stopwords = file.read().splitlines()
    stop_words = set(swedish_stopwords + custom_stopwords)
    tokenized_docs = [
        [token.lower() for token in nltk.word_tokenize(doc) if token.lower() not in stop_words]
        for doc in documents
    ]

    # Save tokenized documents to file
    with open(tokenized_docs_path, "wb") as file:
        pickle.dump(tokenized_docs, file)
end_time_ladda_data = time.time()
elapsed_time = end_time_ladda_data - start_time_ladda_data
print('Tokenize time:',elapsed_time)

# Create a dictionary from the tokenized documents
print('Create a dictionary from the tokenized documents')
dictionary = corpora.Dictionary(tokenized_docs)

# Create a corpus
print('Create a corpus')
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Train the TF-IDF model on the corpus
print('Train the TF-IDF model on the corpus')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Build an index
print('Build an index')
index_obj = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=len(dictionary))




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    input_value = request.form.get('input_value')
    modified_value = hitta_job(documents, occupations, dictionary, tfidf, index_obj, input_value)
    flash('yay')
    return render_template('index.html', input_value=input_value, modified_value=Markup(modified_value))

@app.route('/send_selected', methods=['POST'])
def send_selected():
    selected_html = request.json['selected_html']
    reur_html = topicS.main(selected_html)
    flash('Selected HTML received successfully.')
    return jsonify({'selected_html': reur_html})

if __name__ == '__main__':
    app.run(debug=True)
