import pywikibot
from pywikibot import pagegenerators


site = pywikibot.Site()
cat = pywikibot.Category(site,'Category:Afghan cuisine')
gen = pagegenerators.CategorizedPageGenerator(cat)

for page in gen:
    page.get()
    food = page.title