from models import db, Article
import requests
from bs4 import BeautifulSoup
from url_manager import urls  # Import the list of URLs
from sqlalchemy.exc import SQLAlchemyError


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}


def remove_duplicates(urls):
    return list(set(urls))

urls = remove_duplicates(urls)

def scrape_content(url):
    print(f"Fetching URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'html.parser')
        content = bs.find('div', {'class': 'caas-body'})
        title_tag = bs.find('h1')
        if content and title_tag:
            content_text = content.get_text(separator=' ', strip=True)
            title_text = title_tag.text.strip()
            return title_text, content_text
        else:
            error_msg = "Content block not found" if not content else "Title block not found"
            return None, error_msg
    else:
        print(f"Failed to fetch page for URL: {url}, Status Code: {response.status_code}")
        return None, "Failed to fetch page"



def save_article(url, title, content):
    try:
        if content != "Content block not found" and content != "Failed to fetch page" and title is not None:
            new_article = Article(url=url, title=title, content=content)
            db.session.add(new_article)
            db.session.commit()
            print(f"Article saved for URL: {url}")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error saving article for URL: {url}, Error: {str(e)}")

if __name__ == "__main__":
    for url in urls:
        print(f"Processing URL: {url}") 
        title, article_text = scrape_content(url)
        save_article(url, article_text)