## import pytest
import parser

# test page Tom yum 
test_page = parser.ParsePage('https://en.wikipedia.org/wiki/Tom_yum')

def test_parse_titles():
    title = test_page.parse_title() 
    assert title == 'Tom yum'

##### will have to come back to this ##### 
## def test_bad_site():
    ## pass

def test_parse_sections():
    sections = test_page.parse_sections() 
    assert sections == ['Contents', 'Preparation[edit]', 'Selected types[edit]', 
        'Other spicy and sour soups[edit]', 'Beyond Thailand[edit]', 'See also[edit]', 
        'References[edit]', 'External links[edit]', 'Navigation menu']