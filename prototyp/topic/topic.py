import pandas as pd
import time
import gensim
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from nltk.corpus import stopwords
from gensim.models.phrases import Phrases, Phraser
import multiprocessing

def main():
    # Specify the maximum number of rows to load
    max_rows = None
    # Define the filtering value
    jobb_filter = "förskollärare" # jobb_filter ="" kommer att inklusera alla värden


    # Read CSV file
    print("Laddar data")
    data = pd.read_csv("job_listings.csv", on_bad_lines='skip', nrows=max_rows)

    filtered_data = data[data['occupation.label'].str.contains(jobb_filter, case=False, na=False)]
    print(f"Number of rows after filtering: {len(filtered_data)}")
    
    # Extract the "description.text" column
    documents = filtered_data["description.text"].tolist()
    
    # Add custom stop words
    print("Lägger till stopord")
    swedish_stopwords = set(stopwords.words("swedish"))


    # Load the stop word list from file
    stopwords_file = "stopwords.txt"
    with open(stopwords_file, "r", encoding="utf-8") as file:
        stop_words = [word.strip() for word in file.readlines()]

    swedish_stopwords.update(stop_words)

    # Preprocess the text data
    print("Prossesar text")
    def preprocess(text):
        # Tokenize the text into individual words
        tokens = simple_preprocess(text, deacc=False)

        # Remove stopwords
        tokens = [token for token in tokens if token not in swedish_stopwords]
        return tokens

    # Apply preprocessing to each document
    print("Prossesar dokument")
    preprocessed_documents = [preprocess(doc) for doc in documents]

    """
    # Create bigram and trigram models
    print("Gennererar bigram och trigram")
    bigram = Phrases(preprocessed_documents, min_count=5, threshold=100)
    trigram = Phrases(bigram[preprocessed_documents], min_count=5, threshold=100)

    # Create a Phraser object for efficiency
    bigram_mod = Phraser(bigram)
    trigram_mod = Phraser(trigram)

    # Apply bigram and trigram models to documents
    preprocessed_documents = [trigram_mod[bigram_mod[doc]] for doc in preprocessed_documents]
    """

    # Create a dictionary and corpus for the LDA model
    dictionary = Dictionary(preprocessed_documents)
    corpus = [dictionary.doc2bow(doc) for doc in preprocessed_documents]

    # Get the number of available cores
    num_cores = multiprocessing.cpu_count()
    print("Antal CPU Kärnor:",num_cores)
    # Train the LDA model using LdaMulticore
    start_time = time.time()
    num_topics = 10
    lda_model = LdaMulticore(corpus, num_topics, id2word=dictionary, passes=10, workers=num_cores)

    end_time = time.time()

    # Print the topics and their corresponding word probabilities
    for idx, topic in lda_model.print_topics(-1):
        print(f'Topic: {idx}')
        print(f'Words: {topic}\n')

    # Print the topics and their corresponding word probabilities
    for idx, topic in lda_model.print_topics(-1):
        print(f'Topic: {idx}')
        words = [word.split('"')[1] for word in topic.split('+')]
        sentence = ' '.join(words)
        print(f'Words: {sentence}\n')
    
    # Get the keywords for each topic
    topic_keywords = lda_model.show_topics(num_topics=num_topics, num_words=10)

    # Extract the words from the topic keywords
    new_stopwords = set()
    for topic_id, keywords in topic_keywords:
        words = keywords.split('"')[1::2]  # Extract words between double quotes
        new_stopwords.update(words)

    # Print the new words for the stop list
    print("New words for the stop list:")
    print(new_stopwords)

    # Print the execution time
    execution_time = end_time - start_time
    print(f"\nExecution time: {execution_time:.2f} seconds")

if __name__ == '__main__':
    main()
