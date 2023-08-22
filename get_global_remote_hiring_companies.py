import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# Read input CSV file and extract URLs
def read_csv(input_filename):
    urls = []
    with open(input_filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['URL'])
    return urls

# Extract country from location string
def extract_country(location):
    return location.split(', ')[-1]

# Check if the job listing is remote
def is_remote_job(job_listing_url):
    response = requests.get(job_listing_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        location_elements = soup.find_all('span', class_='workplaceTypes')
        locations = [element.text.strip() for element in location_elements]
        return all("Remote" in location for location in locations)
    return False

# Write filtered companies to a new CSV file
def write_csv(filtered_companies, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'URL'])
        writer.writerows(filtered_companies)

# Main function
def main():
    input_filename = 'input_urls.csv'
    output_filename = 'global_remote_multicountry_companies.csv'

    urls = read_csv(input_filename)
    companies_data = defaultdict(list)

    for url in urls:
        print ("Fetch %s", url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            company_name = soup.find('title').text.strip()
            location_elements = soup.find_all('span', class_='location')
            locations = [element.text.strip() for element in location_elements]
            
            if is_remote_job(url) and len(locations) >= 5:
                countries = set(extract_country(location) for location in locations)
                if len(countries) >= 5:
                    companies_data[company_name].append(url)

    filtered_companies = [[company, urls[0]] for company, urls in companies_data.items()]
    write_csv(filtered_companies, output_filename)

if __name__ == "__main__":
    main()
