# This script contains a function which accepts an .html file and outputs:
# - Number of characters in the ~body~ of the article
# - Number of pictures
# - Number of sections
# - Number of references
# It is used by Archive_scraper.py on the pages in 'archive_cache'
# Mostafa | Mar 7 2022

from bs4 import BeautifulSoup
import re


def analyze(article) -> dict:
    # `article` is a BeautifulSoup object
    soup = BeautifulSoup(article, "html.parser")

    pics_urls = get_pics(soup)
    pics_num = len(pics_urls)

    results = {
               'title': get_name(soup),
               'num_chars': count_chars(soup),
               'num_pics': pics_num,
               'pics_list': pics_urls,
               'num_sects': count_sects(soup),
               'num_refs': count_refs(soup)
               }

    return results


def get_name(soup) -> str:
    """Returns the first header <h1> (usually article title) """
    name = soup.find_all("h1")[0].text
    return name


def count_chars(soup) -> int:
    """Returns a count of characters inside <p> tags"""
    paragraphs = soup.find_all("p")  # List of paragraphs
    num_chars = sum([len(x.text) for x in paragraphs])

    return num_chars


def get_pics(soup) -> list:
    """Returns a list of URLs for article images in the wikipage. Naively tried
    to parse for the images; captures everything in the english language, but
    may miss edge-cases in non-english-wikis."""
    images = []

    # FILTER #1
    images += [
               img.attrs['src']
               for img in soup.find_all("img")
               if img.attrs.get('class', [None])[0] == 'thumbimage'
               ]

    # FILTER #2
    images += [
               x.find("img").attrs["src"]
               for x in
               soup.find_all("td", class_="infobox-image")
               ]

    return images


def count_sects(soup):
    subsections, subsubsections = [], []
    try:
        toc = soup.find("div", {"id": "toc"}).find_all("li")  # Finds TOC card

        subsections = [x for x in toc
                       if 'toclevel-1' in x.attrs.get('class', [None])]

        subsubsections = [x for x in toc
                          if 'toclevel-2' in x.attrs.get('class', [None])]
    except Exception as e:
        pass
    return len(subsections), len(subsubsections)


def count_refs(soup):
    # TODO: Consider having measure for "shared" references vs unique? hmm
    refs = []
    try:
        refs += [x for x in soup.find(class_='references') if x.name == 'li']

    except Exception:
        pass
    return len(refs)
