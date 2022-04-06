# This script contains a function which accepts an .html file and outputs:
# - Number of characters in the ~body~ of the article
# - Number of pictures
# - Number of sections
# - ..?
# It is used by Archive_scraper.py on the pages in 'archive_cache'
# Mostafa | Mar 7 2022

from bs4 import BeautifulSoup
import re


def analyze(article):
    # `article` is a BeautifulSoup object
    soup = BeautifulSoup(article, "html.parser")

    results = {
               'title': get_name(soup),
               'num_chars': count_chars(soup),
               'num_pics': count_pics(soup),
               'num_sects': count_sects(soup)
               }

    return results


def get_name(soup):
    name = soup.find_all("h1")[0].text
    return name


def count_chars(soup):
    paragraphs = soup.find_all("p")  # List of paragraphs
    num_chars = sum([len(x.text) for x in paragraphs])
    return num_chars


def count_pics(soup):
    images = soup.find_all(class_=re.compile("thumb"))
    # ^^ This returns a list of all elements with 'thumb' in the name of class
    return len(images)


def count_sects(soup):
    headers = soup.find_all("h2")
    return len(headers)

# TODO: Think of other characteristics to measure.
# TODO: eg. NUMBER OF REFERENCES!!


if __name__ == "__main__":
    # This runs if you execute HtmlAnalyzer.py instead of import it
    pass
