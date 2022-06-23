import pandas as pd
import json
import urllib.request as urlq
import shutil
import os
import time
import pathlib
import zipfile
from tqdm import tqdm


def JSONtoDF(filename) -> pd.DataFrame:
    """Parses the .json output of a WDQS (wikidata query service) into a
    Pandas DataFrame"""

    with open(filename) as f:
        raw_data: dict = json.load(f)
        f.close()

    raw_data = [x for x in raw_data if 'article' in x.keys()
                and 'wikipedia' in x['article']]  # Throw out duds

    for k, r in enumerate(raw_data):
        r['item'] = r['item'][31:]
        r['lang'] = r['article'][8:r['article'].find('wiki') - 1]

    return pd.DataFrame(raw_data)


"""
Example of output:
    item itemLabel                                            article      lang
0  Q1269       jam                  https://ar.wikipedia.org/wiki/Jam        ar
1  Q1269       jam           https://atj.wikipedia.org/wiki/Cikominan       atj
2  Q1269       jam                  https://az.wikipedia.org/wiki/Cem        az
3  Q1269       jam  https://be-tarask.wikipedia.org/wiki/%D0%94%D0...   be-tara
4  Q1269       jam  https://be.wikipedia.org/wiki/%D0%94%D0%B6%D1%...        be
"""


def cache_URLs(df: pd.DataFrame,
               filename: str,
               temp_directory: str = "dl_temp",
               archive: bool = True,
               wait_interval: int = 1):
    """
    Downloads webpages from the url column in the DataFrame output from
    `JSONtoDF()`. If parameter `archive` is True, will also compress each set.
    Ideal use: called in a loop on a set of articles clustered by QCode
    """

    # Make the directory for the chunk:
    directory = pathlib.Path(f"{temp_directory}/{filename}/")
    if not directory.exists():
        os.makedirs(directory)

    # Retrieve .HTML files:
    with tqdm(total=len(df), desc=filename) as pbar:

        for index, row in df.iterrows():
            url = row['article']
            name = f"{index}_{row['item']}_{row['itemLabel']}_{row['lang']}"
            try:
                urlq.urlretrieve(url, directory / f"{name}.html")
                time.sleep(wait_interval)

            except Exception as e:
                print(f"Problem with {name}")
                print(e)
            pbar.update(1)

    # Archive the files if setting is enabled:
    # I've found that lzma compression algorithm works best here
    if archive:
        with zipfile.ZipFile(
                            f"archive_cache/{filename}.zip",
                            mode="w",
                            compression=zipfile.ZIP_LZMA,
                            compresslevel=9
                            ) as archive:
            for file_path in directory.rglob("*"):
                print(f"compressing {file_path.name}", end="\r")
                archive.write(filename=file_path, arcname=file_path.name)

            archive.close()

            shutil.rmtree(directory)  # Delete uncompressed shit


def GroupFood(df: pd.DataFrame):
    """Generator, breaks up a dataframe into smaller chunks by QCode
    Returns dataframe and the QCode"""
    start = 0
    while True:
        try:
            key = df.item.unique()[start]
            name = df.itemLabel.unique()[start].replace(" ", "_")
            start += 1
            yield df.loc[df.item == key], f"{key}_{name}"
        except StopIteration:
            break


if __name__ == "__main__":
    print("Loaded datasets/food_articles_jun_9_2022.json")
    df = JSONtoDF("datasets/food_articles_jun_9_2022.json")
    start = int(input("Input starting row number"))
    end = int(input("Input end row number"))
    input("Press ENTER to continue..")

    for qf, name in GroupFood(df.iloc[start:end]):
        cache_URLs(qf, name)
