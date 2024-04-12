# import requests
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
# }

# url = 'https://finance.yahoo.com/news/canadian-dollar-trades-tight-range-191803920.html'
# response = requests.get(url, headers=headers)

# bs = BeautifulSoup(response.text, 'html.parser')

# content = bs.find('div', {'class': 'caas-body'})
# print(content.get_text())

######
from app import db, Article

import requests
from bs4 import BeautifulSoup
from url_manager import urls  # Import the list of URLs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}


def remove_duplicates(urls):
    return list(set(urls))

urls = remove_duplicates(urls)

def scrape_content(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'html.parser')
        content = bs.find('div', {'class': 'caas-body'})
        if content:
            return content.get_text(separator=' ', strip=True)
        else:
            return "Content block not found"
    else:
        return "Failed to fetch page"


def save_article(url, content):
    if content != "Content block not found" and content != "Failed to fetch page":
        new_article = Article(url=url, content=content)
        db.session.add(new_article)
        db.session.commit()

if __name__ == "__main__":
    for url in urls:
        article_text = scrape_content(url)
        save_article(url, article_text)