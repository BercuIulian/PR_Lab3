import requests
from bs4 import BeautifulSoup
import json

def extract_urls(url, max_page_num=None):
    parsed_urls = []
    
    # Helper function to extract absolute URLs
    def absolute_url(base_url, link):
        if link.startswith("http"):
            return link
        elif link.startswith("/"):
            return base_url + link
        else:
            return "/".join(base_url.split("/")[:-1]) + "/" + link

    # Function to extract URLs from a page
    def extract_page_urls(page_url):
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = soup.find_all('a', href=True)
        for link in urls:
            absolute_link = absolute_url(page_url, link['href'])
            if "boosters" not in absolute_link:
                parsed_urls.append(absolute_link)

        # Check if there are more pages to parse
        next_page = soup.find('a', class_='pager__item--next')
        if next_page and (max_page_num is None or max_page_num > 1):
            next_page_url = absolute_url(page_url, next_page['href'])
            parsed_urls.extend(extract_page_urls(next_page_url, max_page_num - 1 if max_page_num else None))

    extract_page_urls(url)
    
    # Save the parsed URLs to a JSON file
    with open('parsed_urls.json', 'w') as f:
        json.dump(parsed_urls, f)

    return parsed_urls

if __name__ == "__main__":
    url = "https://999.md/ru/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"
    max_page_num = None  # Set max_page_num to limit the number of pages to parse (optional)
    result = extract_urls(url, max_page_num)
    print(f"Total URLs extracted: {len(result)}")
