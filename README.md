# wiki-food-lang

We want to inspect Wikipedia articles about food and compare them across languages. This project is currently split into three steps:
1. Pull all the Wikipedia food article URLs 
2. Put the URLs through a parser to save the HTMl file into a dataset
3. Inspect and analyze the data


`getURLs.py` is a script that retrieves the list of all food-related wiki articles using a `SPARQL` query to wikidata. In principle, this could be used to retrieve all 2858 foods, but for now we generated a "small" dataset using the first 5 foods (`/datasets/small_URL_dataset`). This amounts to about 300 pages of wiki articles available in all languages!!


`URLtoHTML.py` is a script that downloads an item's articles in all the available languages as `.html` files. It can compress the each food's article set together into a `.zip`, and leaves it in `/archive_cache`


`cache_4_items.py` uses `URLtoHTML.py` to cache the first 4 items in `/datasets/small_URL_dataset`. The output resides in `/archive_cache`, which is not on github and should be downloaded separately here: https://www.dropbox.com/sh/0z4yi79f5mzf1e8/AAC0yRfyEzUY746Jxw9WZEp6a?dl=0

Make sure you place it in the main working directory.