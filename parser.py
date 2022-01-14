import requests
from bs4 import BeautifulSoup
from requests.api import request

class ParsePage:
    def __init__(self, url = None, page = None):        
        self.url = url
        self.page = page
        try:
            r = requests.get(url)
            self.text = r.text
            self.page = BeautifulSoup(r.content, 'html.parser')
        except:
            pass
        
    def full_page(self):
        return self.page
        
    def parse_title(self):
        title = self.page.find('h1').get_text()
        return title 

    def parse_sections(self):        
        sections = []
        i = 0
        max = len(self.page.find_all('h2'))
        for i in range(0, max):
            sections.append(self.page.find_all('h2')[i].get_text()) 
        return sections
