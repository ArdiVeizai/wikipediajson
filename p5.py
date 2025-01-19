import numpy as np
from sklearn.metrics import average_precision_score

# Επεξεργασία Ερωτημάτων (Query Processing)
def process_query(query, inverted_index):
    """
    Επεξεργασία ερωτήματος με tokenization και εφαρμογή Boolean λογικών (AND, OR, NOT).
    Ανακτά τα σχετικά έγγραφα από το ανεστραμμένο ευρετήριο.
    """
    query_terms = query.lower().split()
    retrieved_docs = set()
    
    # Βασική επεξεργασία για Boolean operations
    for term in query_terms:
        if term in inverted_index:
            retrieved_docs.update(inverted_index[term])
    
    return retrieved_docs

# Δημιουργία Ανεστραμμένου Ευρετηρίου (Inverted Index)
def create_inverted_index(documents):
    inverted_index = {}
    for doc_id, doc in enumerate(documents):
        terms = doc.lower().split()
        for term in terms:
            if term not in inverted_index:
                inverted_index[term] = set()
            inverted_index[term].add(doc_id)
    return inverted_index

# Δημιουργία Συνόλου Δοκιμής και Σχετικών Εγγράφων
test_queries = [
    "information retrieval",
    "data mining",
    "machine learning"
]

relevant_documents = {
    "information retrieval": [1, 3, 5, 7],
    "data mining": [2, 4, 6],
    "machine learning": [0, 2, 6, 8]
}

# Ανακτήσεις από τη μηχανή αναζήτησης για κάθε ερώτημα (παράδειγμα αποτελεσμάτων)
retrieved_documents = {
    "information retrieval": [1, 4, 5, 7, 9],
    "data mining": [2, 3, 6, 7],
    "machine learning": [0, 2, 6, 7]
}

# Υπολογισμός των μετρικών αξιολόγησης
def evaluate_query(query, relevant_docs, retrieved_docs):
    true_positives = len(set(retrieved_docs).intersection(set(relevant_docs)))
    false_positives = len(set(retrieved_docs).difference(set(relevant_docs)))
    false_negatives = len(set(relevant_docs).difference(set(retrieved_docs)))
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Υπολογισμός MAP (Mean Average Precision)
    average_precision = average_precision_score([1 if doc in relevant_docs else 0 for doc in retrieved_docs], [1] * len(retrieved_docs))
    
    return precision, recall, f1, average_precision

# Δημιουργία Ανεστραμμένου Ευρετηρίου από τα έγγραφα (παράδειγμα)
documents = [
    "Information retrieval is the process of obtaining relevant documents from a large collection.",
    "Data mining involves extracting useful patterns from large datasets.",
    "Machine learning is a method of data analysis that automates analytical model building."
]

inverted_index = create_inverted_index(documents)

# Επεξεργασία ερωτημάτων και αξιολόγηση
precision_list = []
recall_list = []
f1_list = []
map_list = []

for query in test_queries:
    retrieved_docs = process_query(query, inverted_index)
    relevant_docs = relevant_documents[query]
    
    precision, recall, f1, map_score = evaluate_query(query, relevant_docs, retrieved_docs)
    
    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1)
    map_list.append(map_score)

# Υπολογισμός μέσων όρων
avg_precision = np.mean(precision_list)
avg_recall = np.mean(recall_list)
avg_f1 = np.mean(f1_list)
avg_map = np.mean(map_list)

# Παρουσίαση των αποτελεσμάτων
print(f"Μέση Ακρίβεια (Precision): {avg_precision:.4f}")
print(f"Μέση Ανάκληση (Recall): {avg_recall:.4f}")
print(f"Μέσο F1-Score: {avg_f1:.4f}")
print(f"Μέση Ακρίβεια (MAP): {avg_map:.4f}")
