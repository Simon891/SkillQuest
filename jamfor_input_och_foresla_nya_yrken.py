import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Läs in datasetet med jobbannonser
dataset = pd.read_csv("../ny/dataset_halv_1.csv")  # Byt ut "jobbannonser.csv" med din datasetfil

# Skapa en tf-idf vektorisering baserat på jobbannonsernas text
vectorizer = TfidfVectorizer()
job_ads_vectors = vectorizer.fit_transform(dataset["description.text"])

# Skapa en interaktiv funktion för användarens input och matchning
def match_job_ads(threshold):
    user_input = input("Ange din profil och vad du har för färdigheter: ")

    # Preprocessa användarens input och skapa en vektorrepresentation
    user_input_vector = vectorizer.transform([user_input])

    # Beräkna likhetsscore mellan användarens input och jobbannonser
    similarity_scores = cosine_similarity(user_input_vector, job_ads_vectors)

    # Sortera annonserna baserat på likhetsscore
    sorted_indexes = similarity_scores.argsort()[0][::-1]

    # Skapa en mängd för att lagra unika annonser
    unique_ads = set()

    # Loopa igenom de sorterade indexen och ta bort dubbletter
    for idx in sorted_indexes:
        if similarity_scores[0][idx] >= threshold:
            job_ad = dataset.loc[idx, "occupation.label"]
            unique_ads.add(job_ad)

    # Skriv ut de unika annonserna
    for ad in unique_ads:
        print("Detta jobb skulle också kunna vara någonting för dig:", ad)


# Ange det önskade tröskelvärdet för matchning (0-1), mer exakt ju närmre 1 man väljer
troskelvarde = 0.3

# Kör matchningsfunktionen med det valda tröskelvärdet
match_job_ads(troskelvarde)