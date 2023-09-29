import requests
import bs4 as bs
from json import dumps


def extract_tags_values(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    tag_names = []
    tag_values = []
    result = {}

    for tag_name in soup.find_all("span", class_="adPage__content__features__key"):
        tag_names.append(tag_name.text.strip())

    for tag_value in soup.find_all("span", class_="adPage__content__features__value"):
        tag_values.append(tag_value.text.strip())

    for tag_name in tag_names:
        result[tag_name] = tag_values[tag_names.index(tag_name)] if tag_names.index(tag_name) < len(tag_values) else True

    return result


def main():
    urls = [
        'https://999.md/ro/84118451',
    ]

    results = {}

    for url in urls:
        results[url] = extract_tags_values(url)

    print(dumps(results, indent=4))


if __name__ == '__main__':
    main()