import math
import re
from collections import defaultdict
from termcolor import colored
with open("docs.txt", "r", encoding="utf-8") as f:
    documents = f.read().split("####")

# stopliste en avance
stoplist = ["le", "la", "les", "un", "une", "de", "du", "des", "et", "à","est","au","a"]

# freq min et max
min_freq = 2
max_freq = 20

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
    if freq < min_freq or freq >= max_freq:
        del index[mot]

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
            if freq >= min_freq and freq < max_freq:
                f1.write(f"{term}: {freq}\n")
        f1.write("\n")

# Écriture des poids de chaque terme dans un fichier
with open("formule.txt", "w", encoding="utf-8") as f2:
    for i, document in enumerate(documents):
        f2.write(f"Document {i+1}:\n")
        term_freq = defaultdict(int)
        term_weight = defaultdict(float)
        for j, phrase in enumerate(re.split('[\.\?!]', document)):
            for mot in re.split('[^\w\']+', phrase):
                mot = mot.lower()
                if mot != "" and mot not in stoplist:
                    term_freq[mot] += 1
        for term, freq in term_freq.items():
            if freq >= min_freq and freq < max_freq:
                tf = freq / sum(term_freq.values())
                df = len(index[term])
                idf = math.log(len(documents) / (df+1))
                term_weight[term] = tf * idf
        for term, weight in term_weight.items():
            f2.write(f"{term}: {weight:.2f}\n")
        f2.write("\n")
# Recherche des documents pertinents pour un terme donné
while True:
    term = input("Entrez un terme : ")
    if term == "":
        break
    query_terms = term.split()
    if term not in index:
        print("Terme non trouvé.")
    else:
        relevant_docs = set([doc_id for doc_id, _ in index[term]])
        print(f"{len(relevant_docs)} documents pertinents trouvés le terme'{colored(term, 'red')}':")
        for doc_id in relevant_docs:
            doc = documents[doc_id].replace(term, colored(term, 'red'))
            term_count = doc.count(term)
            print(f"Document {doc_id + 1} - contient {term} {term_count} fois :")
            print(doc)
