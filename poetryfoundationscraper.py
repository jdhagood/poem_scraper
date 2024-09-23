import sys
import io

# Set UTF-8 encoding for stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from bs4 import BeautifulSoup
import requests
import random

def get_poem_urls_from_page(url):
    pageToScrape = requests.get(url)
    pageToScrape.encoding = "Windows-1252"
    soup = BeautifulSoup(pageToScrape.text, "html.parser")
    poems = soup.find_all("a", {'class': 'link-underline-on link-red'})
    urls = []
    for poem in poems:
        urls.append("https://www.poetryfoundation.org" + poem["href"])
    return urls

def get_random_poem_url():
    pages = [
        "https://www.poetryfoundation.org/poems/browse/the-mind",
        "https://www.poetryfoundation.org/poems/browse/subjects",
        "https://www.poetryfoundation.org/poems/browse/love",
        "https://www.poetryfoundation.org/poems/browse/time-brevity",
        "https://www.poetryfoundation.org/poems/browse/arts-sciences",
        "https://www.poetryfoundation.org/poems/browse/humor-satire",
        "https://www.poetryfoundation.org/poems/browse/the-body",
        "https://www.poetryfoundation.org/poems/browse/relationships"
    ]
    page_url = random.choice(pages)
    return random.choice(get_poem_urls_from_page(page_url))
    

def get_poem_of_the_day_url():
    url = "https://www.poetryfoundation.org/poems"
    pageToScrape = requests.get(url)
    pageToScrape.encoding = "Windows-1252"
    soup = BeautifulSoup(pageToScrape.text, "html.parser")
    poem_of_the_day = soup.find("a", {'class': 'link-underline-on link-red'})
    url = "https://www.poetryfoundation.org" + poem_of_the_day["href"]
    print(url)
    return url


def scrape_poem(url):
    poem = {
        "url": url,
        "title": None,
        "author": None,
        "body": None
    }

    pageToScrape = requests.get(url)
    pageToScrape.encoding = 'utf-8'  # Ensure UTF-8 encoding

    soup = BeautifulSoup(pageToScrape.text, "html.parser")

    poemTitle = soup.find("h1")
    author_tag = soup.find("a", {'class': 'link-underline-off link-red'})

    if poemTitle:
        poem["title"] = poemTitle.text
        poem["author"] = author_tag.text

        poemContent = soup.find("div", {'class': 'poem-body'})
        body = ""
        for child in poemContent.children:
            line = child.text.replace("\r", "") + "\n"
            #print(repr(line))
            body += line
        poem["body"] = body

    return poem

def get_random_poem():
    while(True):
        url = get_random_poem_url()
        try:
            poem = scrape_poem(url)
            if None not in poem.values() and len(poem["body"]) > 3:
                return poem
        except:
            pass

def print_poem(poem):
    print("###########################################")
    print(f"URL: {poem['url']}")
    print(f"Title: {poem['title']}")
    print(f"By: {poem['author']}\n\n")
    print(poem['body'])
    print("###########################################")

for _ in range(10):
    #print_poem(scrape_poem("https://www.poetryfoundation.org/poems/1543385/gratitude"))
    print_poem(get_random_poem())
# scrape_poem("https://www.poetryfoundation.org/poems/1543385/gratitude") #worked!
# scrape_poem("https://www.poetryfoundation.org/poems/48377/women-56d22991710fe") #added an extra line between every line
# scrape_poem("https://www.poetryfoundation.org/poems/162299/mrs-butterworth-uncle-ben-aunt-jemima") #added an extra line between
# scrape_poem("https://www.poetryfoundation.org/poems/49303/howl") #ADDED AN EXTRA LINE BETWEEN EVERY LINE
#scrape_poem("https://www.poetryfoundation.org/poems/47311/the-waste-land")