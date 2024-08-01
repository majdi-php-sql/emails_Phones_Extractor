import requests  # Importing requests to handle the HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse the HTML content
import re  # Importing re to use regular expressions for finding emails and phone numbers
import csv  # Importing csv to handle CSV file operations
import os  # Importing os to handle file operations

def extract_emails_and_phones(url):
    # Sending a GET request to fetch the page content
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")  # Print an error if the request failed
        return set(), set()  # Return empty sets if retrieval failed

    # Parsing the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding all email addresses in the page content
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text))
    # Finding all phone numbers in the page content
    phones = set(re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.text))

    return emails, phones  # Return the found emails and phone numbers

def save_to_csv(filename, data):
    # Write the data to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Phone", "Email"])  # Write the header
        writer.writerows(data)  # Write the data rows

def read_urls_from_csv(input_filename):
    urls = []
    with open(input_filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present
        for row in reader:
            urls.append(row[0])  # Assuming URLs are in the first column
    return urls

def main():
    print("Welcome to the URL Data Extractor!")  # Welcome message

    # Read URLs from the input CSV file
    input_csv_filename = '/content/sample_data/url - Sheet1.csv'
    urls = read_urls_from_csv(input_csv_filename)
    if not urls:
        print("No URLs found in the input file.")
        return

    # Prepare data for the table
    table_data = []

    # Process each URL and extract data
    for url in urls:
        emails, phones = extract_emails_and_phones(url)  # Extract data from the URL
        # Format the data for the table
        for email in emails:
            table_data.append([url, ', '.join(phones), email])
        if not emails:  # Handle case where no emails are found
            table_data.append([url, ', '.join(phones), "No emails found"])
        if not phones:  # Handle case where no phones are found
            table_data.append([url, "No phones found", ', '.join(emails)])

    # Save results to CSV file
    csv_filename = 'results.csv'
    save_to_csv(csv_filename, table_data)
    print(f"\nResults have been saved to {csv_filename}")

    # Provide a link to download the CSV file
    print(f"Download your results from: {os.path.abspath(csv_filename)}")

if __name__ == "__main__":
    main()
