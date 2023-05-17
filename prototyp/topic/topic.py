# -*- coding: utf-8 -*-
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords
from gensim.models.phrases import Phrases

# Read CSV file
data = pd.read_csv("job_listings.csv", on_bad_lines='skip')

# Extract the "description.text" column
documents = data["description.text"].tolist()

# Add custom stop words
swedish_stopwords = set(stopwords.words("swedish"))
swedish_stopwords.update(["du", "är", "med", "att", "och", "som", "en", "vi", "pa", "har", "inom", "dig", "av", 'kommer'])  # Add additional stop words

# Preprocess the text data
def preprocess(text):
    # Tokenize the text into individual words
    tokens = simple_preprocess(text, deacc=True)

    # Remove stopwords
    tokens = [token for token in tokens if token not in swedish_stopwords]

    return tokens

# Apply preprocessing to each document
preprocessed_documents = [preprocess(doc) for doc in documents]

# Create bigram and trigram models
bigram = Phrases(preprocessed_documents, min_count=5, threshold=100)
trigram = Phrases(bigram[preprocessed_documents], min_count=5, threshold=100)

# Apply bigram and trigram models to documents
preprocessed_documents = [trigram[bigram[doc]] for doc in preprocessed_documents]

# Create a dictionary and corpus for the LDA model
dictionary = Dictionary(preprocessed_documents)
corpus = [dictionary.doc2bow(doc) for doc in preprocessed_documents]

# Train the LDA model
num_topics = 5
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)

# Print the topics and their keywords
for topic_id, topic in lda_model.show_topics(num_topics=num_topics, num_words=10):
    print(f"Topic #{topic_id}: {topic.encode('utf-8')}")
