import pandas as pd
import json
import pywikibot
# from tqdm import tqdm      (gonna use this later)


# Open the JSON containing the wikidata Q-codes
dict_data = {}
with open('food_articles_dec_23_2021.json') as f:
    dict_data = json.load(f)
    f.close()

df = pd.DataFrame.from_dict(dict_data)

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


# Remove the URL portion from the 'item' column
# i.e. http://www.wik..ty/Q6663 ---> Q6663
def stripURL(input):
    return input[31:]


df['item'] = df['item'].apply(stripURL)


# Use 'item.get()' to assemble the URLs for each data item.
def getLink(qcode):
    """
    Input: qcode (i.e. Q6663, which codes for hamburger)
    Output: List containing URLs (hamburger article in english, in russian,
    chinese, etc.)
    """
    print(f"Retrieving {qcode}..")
    item = pywikibot.ItemPage(repo, qcode)
    sites = [x for x in item.get()['sitelinks']]
    # example: sites is ['enwiki', 'itwiki', ..]
    item_labels = {item.getSitelink(site=x) for x in sites}
    # TODO: make the above output a dictionary like (language code:label)
    # example: item_labels is ['garnish (food)', 'garnishio (foodio)', ]
    item_urls = []
    try:
        for k, v in item_labels.items():
            link = f"https://{k}.wikipedia.org/wiki/{v}"
            link = link.replace(" ", "_")
            link = link.replace(",", "_")
            item_urls.append(link)

    except Exception:
        print(f"Something wrong with {qcode}")
        item_urls = ['error']

    print(f"Retrieved {qcode}")
    return item_urls
    # item_urls should be a list ['https://en.wi../garnish_(food)', ..]


df['urls'][0:5] = df['item'][0:5].apply(getLink)
# Only doing 50 items for now..

import pdb; pdb.set_trace()  # FREEZE! (lemme inspect the output pls)
