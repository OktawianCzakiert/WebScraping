import requests
from bs4 import BeautifulSoup
import json


def scrap_webpage():
    page_number = 1
    quotes_list = []
    authors_list = []
    home = "https://quotes.toscrape.com"

    while page_number < 11:
        url = f"{home}/page/{page_number}/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        tags = soup.find_all("div", class_="tags")
        authors_links = soup.find_all("a", string='(about)', href=True)
        quotes = soup.find_all("span", class_="text")

        for author_link in authors_links:
            author_url = f"{home}{author_link['href']}"
            # print(f"url: {author_url}")
            new_response = requests.get(author_url)
            if new_response.status_code == 200:
                soup2 = BeautifulSoup(new_response.text, "lxml")
                authors_list.append({
                    "fullname": soup2.find("h3", class_="author-title").text,
                    "born_date": soup2.find("span", class_="author-born-date").text,
                    "born_location": soup2.find("span", class_="author-born-location").text,
                    "description": soup2.find("div", class_="author-description").text.replace("\n","").strip()
                })

        for i in range(0, len(quotes)):
            tags_list = []
            tagsforquote = tags[i].find_all('a', class_='tag')
            for tagforquote in tagsforquote:
                tags_list.append(tagforquote.text)

            quotes_list.append({
                "tags": tags_list,
                "author": authors_list[i]["fullname"],
                "quote": quotes[i].text
            })

        page_number += 1

    # print(quotes_list)
    with open('quotes_hw9.json', 'w') as file:
        json.dump(quotes_list, file, indent=4)

    # print(authors_list)
    with open('authors_hw9.json', 'w') as file:
        json.dump(authors_list, file, indent=4)


if __name__ == "__main__":
    scrap_webpage()
