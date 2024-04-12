from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://finance.yahoo.com/news/scotiabank-ing-bearish-loonie-canadian-182803041.html')
bs = BeautifulSoup(html, 'html.parser')

content = bs.find('div', {'class': 'caas-body'})
print(content.get_text())