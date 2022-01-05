import pytest
import parser

def test_parse_titles():
    url = 'https://en.wikipedia.org/wiki/Tom_yum'
    title = parser.parse_title(url) 
    assert title == 'Tom yum'

def test_bad_site():
    url = 'https://en.wikipedia.cag/wiki/Tom_yum'
    title = parser.parse_title(url) 
    assert title == 0

def test_parse_sections():
    url = 'https://en.wikipedia.org/wiki/Tom_yum'
    sections = parser.parse_sections(url) 
    assert sections == ['Contents', 'Preparation[edit]', 'Selected types[edit]', 
        'Other spicy and sour soups[edit]', 'Beyond Thailand[edit]', 'See also[edit]', 
        'References[edit]', 'External links[edit]', 'Navigation menu']
