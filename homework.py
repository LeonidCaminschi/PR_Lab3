import requests
from bs4 import BeautifulSoup

def parsehtml(div1, attributes):
    for div in div1:
        ul_elements = div.find_all("ul")
        if ul_elements:
            for ul in ul_elements:
                li_elements = ul.find_all("li")
                if li_elements:
                    for li in li_elements:
                        span = li.find_all('span')
                        if span:
                            for spa in span:
                                a = spa.find('a')
                                if a:
                                    text = a.text
                                else:
                                    text = spa.text

                                attributes += text
                                print(text + " ", end="")
                            print()

def analyzeproduct(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # print(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all divs with the useful information
            div1 = soup.find_all('div', class_='adPage__content__features__col grid_9 suffix_1')
            div2 = soup.find_all('div', class_='adPage__content__features__col grid_7 suffix_1')
            # print(div1)
            # print(div2)

            # Extract and print the divs with data
            attributes = ""
            parsehtml(div1, attributes)
            parsehtml(div2, attributes)
            return attributes
        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
