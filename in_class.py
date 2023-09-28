import requests
from bs4 import BeautifulSoup
import re


def webcrawl(url, page=1):
    list_of_urls = set()

    try:
        # Send a GET request to the URL
        response = requests.get(url + "?page=" + str(page))
        print(url + "?page=" + str(page))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all anchor (link) tags in the HTML
            links = soup.find_all('a')

            # Extract and print the href attribute of each link
            regex = re.compile("/ro/[0-9]")
            for link in links:
                href = link.get('href')
                if href is not None and regex.match(href):
                    list_of_urls.add("https://999.md" + href)

            if len(list_of_urls) == 0:
                return list_of_urls

            list_of_urls.update(webcrawl(url, page + 1))

            return list_of_urls

        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
