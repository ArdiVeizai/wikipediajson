import requests
from bs4 import BeautifulSoup
import json

def scrape_wikipedia_articles(start_url, max_articles=10):
    """
    Συλλέγει άρθρα από το Wikipedia ξεκινώντας από το start_url.
    """
    articles = []  # Λίστα για αποθήκευση άρθρων
    visited = set()  # Σύνολο για αποφυγή διπλότυπων URL
    to_visit = [start_url]  # Λίστα με URL προς επίσκεψη

    while to_visit and len(articles) < max_articles:
        url = to_visit.pop(0)  # Παίρνουμε το επόμενο URL προς επίσκεψη
        if url in visited:
            continue  # Αν έχει ήδη επισκεφθεί, το αγνοούμε
        visited.add(url)

        try:
            # Ανάκτηση περιεχομένου σελίδας
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Εξαγωγή τίτλου και περιεχομένου
            title = soup.find('h1').text
            content = ' '.join([p.text for p in soup.find_all('p')])

            # Αποθήκευση άρθρου
            articles.append({'title': title, 'content': content, 'url': url})

            # Εύρεση συνδέσμων για άλλα άρθρα
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/wiki/') and ':' not in href:
                    full_url = f"https://en.wikipedia.org{href}"
                    to_visit.append(full_url)

        except Exception as e:
            print(f"Σφάλμα κατά την ανάκτηση του {url}: {e}")

    return articles

# Παράδειγμα χρήσης
start_url = "https://en.wikipedia.org/wiki/Natural_language_processing"
max_articles = 10  # Αριθμός άρθρων που θα συλλεχθούν
articles = scrape_wikipedia_articles(start_url, max_articles)

# Αποθήκευση σε αρχείο JSON
output_file = 'wikipedia_articles.json'
with open(output_file, 'w') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Η συλλογή ολοκληρώθηκε. Τα άρθρα αποθηκεύτηκαν στο αρχείο: {output_file}")
