from urllib.request import urlopen
from bs4 import BeautifulSoup
def getTitle(url): # reusable function
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title
title = getTitle("http://www.pythonscraping.com/pages/page1.html")

if title == None:
    print("Title could not be found")
else:
    print(title)