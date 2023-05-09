import math
import re
from collections import defaultdict
from termcolor import colored
with open("Corpuse.txt", "r", encoding="utf-8") as f:
    documents = f.read().split("####")

# stopliste 
stoplist = ["le","la","les","un", "une", "de", "du", "des", "et", "à","est","au","a","dans","en","ce","l'","qui","que","pour","d'un","par","sur","plus","d'une","sont","son","avec","ne","pas","se","sa","ses","ou","dans","cette"]

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
with open("Frequence.txt", "w", encoding="utf-8") as f1:
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
with open("Poids.txt", "w", encoding="utf-8") as f2:
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
# Recherche des documents pertinents pour une requête de termes donnée 
affiches = set()
while True:
    query = input("Entrez une requête: ")
    if query == "":
        break
    query = query.lower()    
    query_terms = re.split("[^\w']+", query) 
    query_terms = [term for term in query_terms if term != "" and term not in stoplist] 
    query_terms = set(query_terms) 
    query_terms = list(query_terms)  
    query_terms.sort() 
    docs = set() 
    for term in query_terms:
        if term in index:
            docs.update(index[term])
    docs = list(docs)
    docs.sort()
    #print("Documents pertinents:", colored(" ".join(str(doc[0]+1) for doc in docs), "green"))
    scores = []
    for doc in docs:
        doc_id = doc[0]
        if doc_id in affiches:
            continue
        phrases = documents[doc_id].split("####")
        found_terms = []
        for phrase in phrases:
            for term in query_terms:
                if term in phrase.lower():
                    found_terms.append(term)
        if len(found_terms) > 0:
            tf = {term: found_terms.count(term) for term in query_terms}
            idf = {term: math.log(len(documents) / len(index[term])) for term in query_terms if term in index and len(index[term]) > 0}
        
            score = sum(tf[term] * idf[term] for term in query_terms if term in idf)
            scores.append((doc_id, score, found_terms))
    if len(scores) > 0:
        scores.sort(key=lambda x: x[1], reverse=True)
        for doc_id, score, found_terms in scores:
            if doc_id in affiches: 
                continue
            affiches.add(doc_id)
            print(f"Document {doc_id+1}:{colored('{:.3f}'.format(score), 'yellow')}") 
            print("Termes trouvés:", colored(" ".join(found_terms), "green"))  
            print()
    else:
        print("Aucun document trouvé")

 

