import math
import re
from collections import defaultdict

with open("docs.txt", "r", encoding="utf-8") as f:
    documents = f.read().split("####")

# stopliste en avance
stoplist = ["le", "la", "les", "un", "une", "de", "du", "des", "et", "à"]

# freq min et max
min_freq = 1
max_freq = 100

index = defaultdict(list)

for i, document in enumerate(documents):
    for j, phrase in enumerate(re.split("[\.\?!]", document)):
        for mot in re.split("[^\w']+", phrase):
            mot = mot.lower()
            if mot != "" and mot not in stoplist:
                index[mot].append((i, j))

# Élimination des mots dont la fréquence est en dehors des seuils
for mot, occurrences in list(index.items()):
    freq = len(occurrences)
    if freq < min_freq or freq > max_freq:
        del index[mot]

term = input("Entrez un terme à rechercher: ").lower()

if term in index:
    occurrences = index[term]
    print(f'Le terme "{term}"se trouve dans :')
    for occurrence in occurrences:
        doc_index, phrase_index = occurrence
        document = documents[doc_index]
        phrase = re.split("[\.\?!]", document)[phrase_index]
        print(f'- Document {doc_index+1}, phrase {phrase_index+1}: "{phrase.strip()}"')
else:
    print(f'Le terme "{term}" n\'a pas été trouvé.')
    # Écriture les termes et freq dans un fichier

with open("output.txt", "w", encoding="utf-8") as f1:
    for i, document in enumerate(documents):
        f1.write(f"Document {i+1}:\n")
        term_freq = defaultdict(int)
        for j, phrase in enumerate(re.split('[\.\?!]', document)):
            for mot in re.split('[^\w\']+', phrase):
                mot = mot.lower()
                if mot != "" and mot not in stoplist:
                    term_freq[mot] += 1
        for term, freq in term_freq.items():
            f1.write(f"{term}: {freq}\n")
        f1.write("\n")
        
        
        
  # Calcul des poids des termes et écriture dans un deuxième fichier
  
with open("formule.txt", "w", encoding="utf-8") as f:
    for i, document in enumerate(documents):
        f.write(f"Document {i+1}:\n")
        term_weight = defaultdict(float)
        for j, phrase in enumerate(re.split('[\.\?!]', document)):
            for mot in re.split('[^\w\']+', phrase):
                mot = mot.lower()
                if mot != "" and mot not in stoplist:
                    tf = term_freq[mot]
                    idf = math.log(len(documents) / len(index[mot]))
                    term_weight[mot] = tf * idf
        for term, weight in term_weight.items():
            f.write(f"{term}: {weight:.2f}\n")
        f.write("\n")        
