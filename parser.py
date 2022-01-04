import requests
from bs4 import BeautifulSoup

def parsesite(url):
    try:
        r = requests.get(url)
        websitetext = r.text
    except:
        print 
        'Problem fetching page!'
        return 0
    # print websitetext
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('h1').get_text()
    sections = []
    i = 0
    max = len(soup.find_all('h2'))
    for i in range(0, max):
        sections.append(soup.find_all('h2')[i].get_text()) 