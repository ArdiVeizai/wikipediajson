import re
from collections import defaultdict

# 1. Δημιουργία Αντεστραμμένου Ευρετηρίου
def create_inverted_index(documents):
    """
    Δημιουργία ανεστραμμένου ευρετηρίου από τη λίστα εγγράφων.
    Επιστρέφει το ανεστραμμένο ευρετήριο.
    """
    inverted_index = defaultdict(list)
    for doc_id, doc in enumerate(documents):
        tokens = preprocess_query(doc)
        for token in set(tokens):  # Χρησιμοποιούμε set για να αποφύγουμε επαναλήψεις
            inverted_index[token].append(doc_id)
    return inverted_index

# 2. Επεξεργασία Ερωτημάτων
def preprocess_query(query):
    """
    Προεπεξεργασία του ερωτήματος:
    - Αφαίρεση ειδικών χαρακτήρων.
    - Μετατροπή σε πεζά.
    - Tokenization.
    """
    query = re.sub(r'[^\w\s]', '', query).lower()  # Αφαίρεση ειδικών χαρακτήρων
    tokens = query.split()  # Διαχωρισμός σε λέξεις
    return tokens

# 3. Boolean Αναζήτηση
def boolean_search(query, inverted_index):
    """
    Εκτέλεση Boolean αναζήτησης.
    Υποστηρίζει τις λειτουργίες AND, OR, NOT.
    """
    tokens = preprocess_query(query)
    results = set()
    operator = "OR"  # Default operator is OR

    for token in tokens:
        if token.upper() in {"AND", "OR", "NOT"}:
            operator = token.upper()
        else:
            postings = set(inverted_index.get(token, []))
            if operator == "OR":
                results = results.union(postings)
            elif operator == "AND":
                results = results.intersection(postings) if results else postings
            elif operator == "NOT":
                results = results.difference(postings)

    return results

# 4. Διεπαφή Χρήστη
def search_interface(inverted_index, documents):
    """
    Διεπαφή χρήστη για αναζήτηση εγγράφων.
    """
    print("Καλώς ήρθατε στη Μηχανή Αναζήτησης!")
    print("Μπορείτε να χρησιμοποιήσετε Boolean αναζήτηση (AND, OR, NOT).")
    print("Πληκτρολογήστε 'exit' για έξοδο.\n")

    while True:
        query = input("Εισάγετε το ερώτημα σας: ")
        if query.lower() == "exit":
            print("Έξοδος από τη Μηχανή Αναζήτησης. Αντίο!")
            break

        # Boolean Αναζήτηση
        boolean_results = boolean_search(query, inverted_index)
        if boolean_results:
            print(f"Αποτελέσματα Boolean: {sorted(boolean_results)}")
            print("Τίτλοι εγγράφων:")
            for doc_id in sorted(boolean_results):
                print(f"- {documents[doc_id]}")
        else:
            print("Δεν βρέθηκαν σχετικά έγγραφα.")

# Παράδειγμα δεδομένων
documents = [
    "Machine learning is a field of artificial intelligence.",
    "Data science is a multidisciplinary field.",
    "Learning algorithms are used in many applications.",
    "Artificial intelligence is the simulation of human intelligence processes.",
    "Data analysis and machine learning are often used together."
]

# Δημιουργία του ανεστραμμένου ευρετηρίου
inverted_index = create_inverted_index(documents)

# Εκκίνηση της διεπαφής αναζήτησης
search_interface(inverted_index, documents)
