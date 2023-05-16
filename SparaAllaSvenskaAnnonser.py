import pandas as pd

# Läs in datasetet
df = pd.read_csv('jobtech_temp2022Rall_UPDATED.csv')

# Skapa en funktion för att identifiera språket i en given textsträng
def identifiera_sprak(text):
    # Här kan du använda valfri språkdetectionsmetod, till exempel språkbiblioteket langdetect
    from langdetect import detect
    try:
        sprak = detect(text)
        return sprak
    except:
        return None

# Skapa en ny kolumn med språket för varje annons
df['sprak'] = df['description.text'].apply(identifiera_sprak)

# Filtrera och spara endast de svenska annonserna
test_svenska_annonser = df[df['sprak'] == 'sv']
test_svenska_annonser.to_csv('samtliga_svenska_annonser.csv', index=False)




