import requests
from bs4 import BeautifulSoup
import csv

# Define a list of URLs for different categories
categories = ['politics', 'business', 'sports', 'technology', 'startup', 'entertainment']

# Create a CSV file to store the data with 'utf-8' encoding
with open('news_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write a header row to the CSV file
    csv_writer.writerow(['Category', 'Headline', 'Content'])  # Add 'Content' column to header

    for category in categories:
        # Construct the URL for the specific category
        url = f"https://inshorts.com/en/read/{category}"

        # Send a GET request to the URL and fetch the HTML content
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <span> elements with the specified attributes
            elements = soup.find_all('span', {'itemprop': 'headline', 'class': 'ddVzQcwl2yPlFt4fteIE'})

            # Find all <div> elements with the specified attributes
            content_elements = soup.find_all('div', {'class': 'KkupEonoVHxNv4A_D7UG', 'itemprop': 'articleBody'})

            if elements and content_elements:
                # Extract and write the data to the CSV file
                for element, content_element in zip(elements, content_elements):
                    headline = element.get_text()
                    content = content_element.get_text()
                    csv_writer.writerow([category, headline, content])
            else:
                print(f"No matching elements were found for {category}.")
        else:
            print(f"Failed to retrieve content for {category}. Status code: {response.status_code}")

print("Data has been saved to news_data.csv.")
