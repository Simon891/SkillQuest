import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Läs in datasetet med jobbannonser
print('# Läs in datasetet med jobbannonser')
dataset = pd.read_csv("dataset/job_listings.csv")  # Byt ut "jobbannonser.csv" med din datasetfil

# Skapa en tf-idf vektorisering baserat på jobbannonsernas text
print('# Skapa en tf-idf vektorisering baserat på jobbannonsernas text')
vectorizer = TfidfVectorizer()
job_ads_vectors = vectorizer.fit_transform(dataset["description.text"])

# Skapa en interaktiv funktion för användarens input och matchning
print('# Skapa en interaktiv funktion för användarens input och matchning')
def match_job_ads(sokord):
    threshold = 0.2
    user_input = sokord

    # Preprocessa användarens input och skapa en vektorrepresentation
    print('# Preprocessa användarens input och skapa en vektorrepresentation')
    user_input_vector = vectorizer.transform([user_input])

    # Beräkna likhetsscore mellan användarens input och jobbannonser
    print('# Beräkna likhetsscore mellan användarens input och jobbannonser')
    similarity_scores = cosine_similarity(user_input_vector, job_ads_vectors)

    # Sortera annonserna baserat på likhetsscore
    print('# Sortera annonserna baserat på likhetsscore')
    sorted_indexes = similarity_scores.argsort()[0][::-1]

    # Skapa en mängd för att lagra unika annonser
    print('# Skapa en mängd för att lagra unika annonser')
    unique_ads = set()

    # Loopa igenom de sorterade indexen och ta bort dubbletter
    print('# Loopa igenom de sorterade indexen och ta bort dubbletter')
    for idx in sorted_indexes:
        if similarity_scores[0][idx] >= threshold:
            job_ad = dataset.loc[idx, "occupation.label"]
            unique_ads.add(job_ad)

    # Skriv ut de unika annonserna
    print('# Skriv ut de unika annonserna')
    for ad in unique_ads:
        print("Detta jobb skulle också kunna vara någonting för dig:", ad)
    
    # Skapa en variabel för att lagra resultatet som sträng
    result_string = ""

    # Wrapa varje unik annons i en <div> med klassen "forslag" och lägg till i result_string
    print('# Wrapa varje unik annons i en <div> med klassen "forslag" och lagra i result_string')
    for ad in unique_ads:
        result_string += f'<div class="forslag">{ad}</div>'

    return result_string


if __name__ == '__main__':
    # Kör matchningsfunktionen
    print('# Kör matchningsfunktionen med det valda tröskelvärdet')
    match_job_ads(troskelvarde)