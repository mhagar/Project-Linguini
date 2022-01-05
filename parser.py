import requests
from bs4 import BeautifulSoup

def parse_title(url):
    try:
        r = requests.get(url)
        websitetext = r.text
    except:
        print 
        'Problem fetching page!'
        return 0
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('h1').get_text()
    return title 

def parse_sections(url):
    try:
        r = requests.get(url)
        websitetext = r.text
    except:
        print 
        'Problem fetching page!'
        return 0    
    soup = BeautifulSoup(r.content, 'html.parser')        
    sections = []
    i = 0
    max = len(soup.find_all('h2'))
    for i in range(0, max):
        sections.append(soup.find_all('h2')[i].get_text()) 
    return sections
