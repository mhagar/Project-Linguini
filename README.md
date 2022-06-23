# wiki-food-lang
Need a better project name tbh. Maybe 'The Linguini Project'?

## Project Aims:

**To analyze geographic discrepancies between article comprehensiveness for food/cuisine-related articles on wikipedia across different languages, and present the data in an interactive website/dashboard.**


## Planning:

1) Come up with some "`article comprehensiveness score`" (ACS), possibly derived from article length, number of pictures, number of sections, and number of references. More descriptors could be included.

2) Come up with some "`geographical relation score`" (GRS). For example, for '*Borscht*', eastern European languages should have a high geographical relation score and Asiatic should have a low score. 

3) Assemble data + findings into an interactive website where users can compare and explore foods/languages. Present striking examples.

In theory, article comprehensiveness should correlate with geographical relation. Striking examples could be cases where this isn't true: for example, Japanese and Afrikaan wikipedias have surprisingly comprehensive articles for *Borscht*. Another striking example could be hypercorrellations, like the discrepancy between the French and English articles for *Omelette* (the French article is 10x longer).

## TODO:

- Write tools for data exploration:
    - function for labelling scatterplots by language in a non-crowded manner (i.e. only labels outliers)
    
    - function for quickly displaying a zoomed out version of a page, and able to flip through the pages rapidly

- Improve `HTMLAnalyzer.py`:
    - ~~`count_pics()` returns an inaccurate number of actual article images (gets muddled with random thumbnail stuff)~~
    - Add a `count_unique_pics()` and `count_unique_refs()` function
    - Implement logging so that 'failed' analyses are recorded for inspection later
        (to check and see where it goes wrong/what the blindspots are): web-scraping is finicky lol
- 

- Implement ACS scoring.
    - Proposal: assess each descriptor (number of lines, images, etc) relative to the whole population. i.e. '*this article's image count is in the 96th percentile in the whole database*'. The total score could be the sum of all such descriptor percentiles.

    - Problems with the above approach: it seems like article comprehensiveness is distributed such that there's a pretty tight mean for most languages, and a handful of really far outliers. It's the outliers that are of interest here.

        - This could potentially be alleviated by operating on log scales.

- 

- Implement GRS scoring.
    - No idea how to go about this. Should start with each food's Q-code.

## Script Descriptions:

`datasets/food_articles_jun_9_2022.json` contains a list of all food articles in all languages, according to the SPARQL query in `query_food_articles.rq`.

`Article_cacher.py` opens that `.json` file, visits the URLs, and caches static HTML files in `archive_cache/`. They're compressed by food to save space. `archive_cache` is not on github and should be downloaded separately here: https://www.dropbox.com/sh/0z4yi79f5mzf1e8/AAC0yRfyEzUY746Jxw9WZEp6a?dl=0 . Make sure you place it in the main working directory.

`Article_scraper.py` loops through the cache mentioned above and applies the functions described in `HTMLAnalyzer.py` to extract infromation about the articles (such as number of pictures, etc).

