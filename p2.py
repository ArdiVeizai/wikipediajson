import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
import json

# Κατέβασμα πόρων NLTK (μόνο την πρώτη φορά)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """
    Εκτελεί προεπεξεργασία στο κείμενο.
    Περιλαμβάνει: αφαίρεση ειδικών χαρακτήρων, tokenization, αφαίρεση stop words,
    stemming και lemmatization.
    """
    # Αφαίρεση ειδικών χαρακτήρων και μετατροπή σε πεζά
    text = re.sub(r'[^\w\s]', '', text)  # Αφαίρεση σημείων στίξης
    text = text.lower()  # Μετατροπή σε πεζά

    # Tokenization
    tokens = word_tokenize(text)

    # Αφαίρεση stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(word) for word in tokens]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in stemmed_tokens]

    return lemmatized_tokens

# Παράδειγμα εφαρμογής σε ένα άρθρο
example_text = """
Natural language processing (NLP) is a subfield of linguistics, computer science, 
and artificial intelligence concerned with the interactions between computers and human language.
"""
processed_tokens = preprocess_text(example_text)
print("Προεπεξεργασμένα Tokens:", processed_tokens)


# Φόρτωση άρθρων από JSON
with open('wikipedia_articles.json', 'r') as f:
    articles = json.load(f)

# Προεπεξεργασία του περιεχομένου κάθε άρθρου
for article in articles:
    article['processed_content'] = preprocess_text(article['content'])

# Αποθήκευση του καθαρισμένου συνόλου δεδομένων
with open('cleaned_wikipedia_articles.json', 'w') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("Η προεπεξεργασία ολοκληρώθηκε. Τα δεδομένα αποθηκεύτηκαν στο 'cleaned_wikipedia_articles.json'.")
