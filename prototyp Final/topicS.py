import pandas as pd
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import heapq

def main(yrke):
    # Download NLTK resources (run once)
    nltk.download('punkt')
    nltk.download('stopwords')

    def summarize_text(sentences):
        # Read custom stopwords from a text file
        with open('stopwords.txt', 'r', encoding='utf-8') as file:
            custom_stopwords = file.read().splitlines()

        # Remove stopwords
        stop_words = set(stopwords.words('swedish') + custom_stopwords)
        
        # Tokenize and filter the sentences
        filtered_text = []
        for sentence in sentences:
            filtered_text.extend([word for word in word_tokenize(sentence) if word.lower() not in stop_words])

        # Calculate word frequency
        word_frequency = nltk.FreqDist(filtered_text)

        # Calculate sentence scores based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequency.keys():
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequency[word]
                    else:
                        sentence_scores[sentence] += word_frequency[word]

        # Select the top 3 sentences with the highest scores
        summarized_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)

        # Return the summarized sentences as a list
        return summarized_sentences


    # Read the CSV file
    df = pd.read_csv('dataset/job_listings.csv')

    # Filter based on the value of "occupation.label"
    filtered_df = df[df['occupation.label'] == yrke]

    antal_anonser = len(filtered_df)

    # Concatenate all "description.text" values into one string
    text = ' '.join(filtered_df['description.text'].tolist())

    # Create a sentence tokenizer for Swedish
    tokenizer = nltk.data.load('tokenizers/punkt/swedish.pickle')

    # Tokenize the text into sentences
    sentences = tokenizer.tokenize(text)

    # Summarize the sentences
    summary = summarize_text(sentences)

    # Print the sentences separately with corresponding numbers
    for i, sentence in enumerate(summary, 1):
        print(f"{i}. {sentence.strip()}")  # Strip any leading/trailing spaces from the sentence

    retur = '<br><br>'.join(summary)


    return retur, antal_anonser

if __name__ == '__main__':
    main()
