from collections import defaultdict
import json

def build_inverted_index(articles):
    """
    Δημιουργεί ένα ανεστραμμένο ευρετήριο από τα δεδομένα άρθρων.
    """
    inverted_index = defaultdict(list)  # Χρησιμοποιούμε defaultdict για ευκολία

    for doc_id, article in enumerate(articles):
        tokens = article['processed_content']  # Λέξεις του άρθρου (μετά την προεπεξεργασία)
        for token in set(tokens):  # Χρησιμοποιούμε set για μοναδικούς όρους
            inverted_index[token].append(doc_id)

    return inverted_index

# Φόρτωση καθαρισμένων δεδομένων
with open('cleaned_wikipedia_articles.json', 'r') as f:
    articles = json.load(f)

# Δημιουργία ανεστραμμένου ευρετηρίου
inverted_index = build_inverted_index(articles)

# Αποθήκευση του ευρετηρίου σε αρχείο JSON
with open('inverted_index.json', 'w') as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=4)

print("Το ανεστραμμένο ευρετήριο αποθηκεύτηκε στο 'inverted_index.json'.")

# Φόρτωση ανεστραμμένου ευρετηρίου
with open('inverted_index.json', 'r') as f:
    inverted_index = json.load(f)

# Παράδειγμα αναζήτησης όρου
search_term = "nlp"
if search_term in inverted_index:
    print(f"Ο όρος '{search_term}' εμφανίζεται στα έγγραφα: {inverted_index[search_term]}")
else:
    print(f"Ο όρος '{search_term}' δεν βρέθηκε στο ευρετήριο.")
