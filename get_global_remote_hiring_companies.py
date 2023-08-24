import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class GlobHiringCo():
    def __init__(self, name, url, locations, jobCount, remoteJobCount):
        self.name = name
        self.url = url
        self.locations = locations
        self.jobCount = jobCount
        self.remoteJobCount = remoteJobCount

class RemoteJobsSummary():
    def __init__(self, numJobs, numRemoteJobs):
        self.numJobs = numJobs
        self.numRemoteJobs = numRemoteJobs

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
def get_job_data(job_listing_url):
    response = requests.get(job_listing_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        location_elements = soup.find_all('span', class_='workplaceTypes')
        locations = [element.text.strip() for element in location_elements]
        remoteJobsCount = locations.count('Remote');
        return RemoteJobsSummary(locations.count, remoteJobsCount)
        #return any("Remote" in location for location in locations)
    #return False

# Write filtered companies to a new CSV file
def write_csv(filtered_companies, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'URL', 'Countries', 'Job Count', 'Remote Job Count'])
        #writer.writerows(filtered_companies)
        for company in filtered_companies:
            writer.writerow([company.name, company.url, company.locations, company.jobCount, company.remoteJobCount])

# Main function
def main():
    input_filename = 'input_urls.csv'
    output_filename = 'global_remote_multicountry_companies.csv'

    urls = read_csv(input_filename)
    #companies_data = defaultdict(list)
    companies_data = []

    for url in urls:
        print ("Fetch %s", url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            company_name = soup.find('title').text.strip()
            location_elements = soup.find_all('span', class_='location')
            locations = [element.text.strip() for element in location_elements]

            jobData = get_job_data(url)
            
            if jobData.numRemoteJobs > 0 and len(locations) >= 5:
                countries = set(extract_country(location) for location in locations)
                if len(countries) >= 5:
                    #companies_data[company_name].append(url)
                    companies_data.append(GlobHiringCo(company_name, url, countries, len(locations), jobData.numRemoteJobs))

    #filtered_companies = [[company, urls[0]] for company, urls in companies_data.items()]
    write_csv(companies_data, output_filename)

if __name__ == "__main__":
    main()
