from in_class import webcrawl
from homework import analyzeproduct

# Replace with the URL of the web page you want to scrape
url1 = "https://999.md/ro/list/computers-and-office-equipment/laptops"

list_of_urls = webcrawl(url1)
print(list_of_urls)

for url in list_of_urls:
    analyzeproduct(url)
    break

# analyzeproduct("https://999.md/ro/82806968")

# with open("urls.txt", 'w') as file:
#     for url in list_of_urls:
#         file.write(url + '\n')
