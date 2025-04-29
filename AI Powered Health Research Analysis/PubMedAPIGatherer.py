from Bio import Entrez
import csv
import time
import os

#------------------------------------Config--------------------------------------------------------------------------------------------------------
ABSTRACT_LIMIT   = 1000                                                     # Number of Results to Pull
WAIT_TIME        = 0.34                                                     # Wait time inbetween pulls for to respect PubMed's Servers
SEARCH_TERM      = "(walking AND treadmill) OR (treadmill AND insurance)"   #The search query for the databse (pubmed) being searched
#--------------------------------------------------------------------------------------------------------------------------------------------------


# Function to load email from a text file
def get_email(email_file ="email.txt"):
    try:
        with open(email_file, 'r', encoding='utf-8') as f:
            email = f.read().strip()
            return email
    except FileNotFoundError:
        print(f"Error: {email_file} not found. Please create  ")
        exit(1)

# Load the email
Entrez.email = get_email()

# Function to fetch PMIDs (PubMed IDs)
def search_pubmed(query, max_results=100):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

# Function to fetch article details (abstract, title)
def fetch_details(id_list):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    records = handle.read()
    handle.close()
    return records

# Save abstracts to a CSV file
def save_to_csv(data, filename="abstracts.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PMID", "Abstract"])
        for pmid, abstract in data.items():
            writer.writerow([pmid, abstract])

# Main Function
def main():
    query = SEARCH_TERM
    max_results = ABSTRACT_LIMIT  # Number of abstracts you want

    pmid_list = search_pubmed(query, max_results)
    print(f"Found {len(pmid_list)} articles")

    abstracts = {}

    # Fetch abstracts individually (safer for large batches)
    for counter, pmid in enumerate(pmid_list, start = 1):
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
            abstract = handle.read()
            abstracts[pmid] = abstract.strip()
            handle.close()
            print(f"Pulling abstract {counter} of {ABSTRACT_LIMIT}. PMID: {pmid}")
            time.sleep(WAIT_TIME)  # Small pause to respect NCBI servers
        except Exception as e:
            print(f"Error fetching {pmid}: {e}")

    save_to_csv(abstracts)
    print(f"Saved {len(abstracts)} abstracts to CSV")


if __name__ == "__main__":
    main()
