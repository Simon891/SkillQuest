import pandas as pd

# Läs in ditt dataset i en DataFrame
jobtech_dataset = pd.read_csv('samtliga_svenska_annonser.csv')

# Plocka ut de önskade kolumnerna
filtered_dataset = jobtech_dataset[['occupation.label', 'description.text']]

# Spara det rensade datasetet till en ny CSV-fil
filtered_dataset.to_csv('rensade_svenska_annonser.csv', index=False)
