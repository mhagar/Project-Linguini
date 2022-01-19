import pandas as pd
import json
import pywikibot
# from tqdm import tqdm      (gonna use this later)


def loadJSON(filename, cleanQCodes=False):
    """
    Input: filename for a .json containing wikidata SPARQL query output
    Output: Pandas dataframe
    """
    # Open the JSON containing the wikidata Q-codes
    dict_data = {}
    with open(filename) as f:
        dict_data = json.load(f)
        f.close()

    df = pd.DataFrame.from_dict(dict_data)

    if cleanQCodes:
        # Remove the URL portion from the 'item' column
        # i.e. http://www.wik..ty/Q6663 ---> Q6663
        df['item'] = df['item'].apply(lambda a: a[31:])
    return df


def retrieveItemURLs(df, begin=0, end=None):
    """
    Input:
        df:     Dataframe, rows of item Q-codes and their labels
        begin:  Beginning of range to process
        end:    End of range to process

    Output:
        Dataframe with columns "item, itemLabel, urls", where 'urls' contains
        a list of all the URLs for the different language articles an item is
        available in.
    """
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
        # returns ['enwiki', 'itwiki', ..]
        item_labels = {x[0:2]: item.getSitelink(site=x) for x in sites}
        # returns {'en':'garnish (food)', 'it':'garnishio (foodio)',}
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
        # item_urls is a list ['https://en.wi../garnish_(food)', ..]

    # Initializing pywikibot:
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    # Creates a list of article URLs for each item
    df['urls'] = df['item']
    df['urls'][begin:end] = df['item'][begin:end].apply(getLink)
    return df


def expandRows(df):
    """
    Input: dataframe that looks like this:
    index   |item   |itemLabel  | urls  |
    1       |QXXXX  | Garnish   | ['url1', 'url2',..]
    2       ..
    3       ...

    Output: dataframe that looks like this:
    index   |item   |itemLabel  | language  | url   |
    1       |QXXXX  | Garnish   |   en      | 'url1'|
    1       |QXXXX  | Garnish   |   it      | 'url2'|
            ...
    """
    expand_df = pd.DataFrame(columns=['item', 'itemLabel', 'language', 'url'])
    for i in range(0, len(df)):
        raw_row = df.loc[i].to_dict()
        expanded_row = []
        for n in raw_row['urls']:
            expanded_row.append({'index': i,
                                 'item': raw_row['item'],
                                 'itemLabel': raw_row['itemLabel'],
                                 'language': n[8:10],
                                 'url': n})

        expansion = pd.DataFrame(expanded_row).set_index('index')

        expand_df = expand_df.append(expansion)
    return expand_df


if __name__ == "__main__":
    input("Default code is to load food_articles_dec_23_2021.json \n"
          "Press ENTER to retrieve URLs for first 5 items and load debugger\n"
          "Otherwise, import this script as a module")

    df = loadJSON('food_articles_dec_23_2021.json', cleanQCodes=True)
    df = retrieveItemURLs(df.loc[0:5], begin=0, end=5)
    df = expandRows(df)

    print(df.head())
    input(...)

    import pdb; pdb.set_trace()  # FREEZE! (lemme inspect the output pls)
