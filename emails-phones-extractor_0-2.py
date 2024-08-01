import requests
from bs4 import BeautifulSoup
import re
import csv
import os

# Function to search for company URL using Google Custom Search API
def search_company_url(company_name, api_key, cx):
    search_url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': company_name,
        'key': api_key,
        'cx': cx
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    
    if 'items' in results:
        first_result = results['items'][0]
        return first_result.get('link')
    return None

def extract_emails_and_phones(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return set(), set()

    soup = BeautifulSoup(response.content, 'html.parser')
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text))
    phones = set(re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.text))

    return emails, phones

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "URL", "Phone", "Email"])
        writer.writerows(data)

def read_companies_from_csv(input_filename):
    companies = []
    with open(input_filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present
        for row in reader:
            companies.append(row[0])  # Assuming company names are in the first column
    return companies

def main():
    api_key = 'your_google_api_key'
    cx = 'your_custom_search_engine_id'
    
    print("Welcome to the Company Data Extractor!")

    input_csv_filename = '/content/sample_data/companies.csv'
    companies = read_companies_from_csv(input_csv_filename)
    if not companies:
        print("No companies found in the input file.")
        return

    table_data = []

    for company in companies:
        url = search_company_url(company, api_key, cx)
        if url:
            emails, phones = extract_emails_and_phones(url)
            for email in emails:
                table_data.append([company, url, ', '.join(phones), email])
            if not emails:
                table_data.append([company, url, ', '.join(phones), "No emails found"])
            if not phones:
                table_data.append([company, url, "No phones found", ', '.join(emails)])
        else:
            table_data.append([company, "URL not found", "N/A", "N/A"])

    csv_filename = 'results.csv'
    save_to_csv(csv_filename, table_data)
    print(f"\nResults have been saved to {csv_filename}")
    print(f"Download your results from: {os.path.abspath(csv_filename)}")

if __name__ == "__main__":
    main()
