# This script defines a function which downloads a list of URLs as .html files
# and saves them in a given directory
# Mostafa 2022/02/16

import urllib.request as urlq
import urllib.parse as urlp
import shutil
import os
import time
import pathlib
import zipfile

# TODO: implement progress bar
# TODO: implement error logging


class item:
    """
    An object that contains a food item's set of URLs in their corresponding
    languages

    Data structure:
    item
    ├─index
    ├─QCode
    ├─itemLabel
    └─urls (tuple of tuples)
        ├ ((lang1, url1),
        ├   lang2, url2),
        └   lang3, url3)..)
        ..
    """
    def __init__(self, df):
        self.df = df  # input df containing a set of URLs from getURLS.py
        self.index = self.df.index[0]
        self.qcode = self.df.iloc[0]['item']
        self.itemLabel = self.df.iloc[0]['itemLabel']
        a, b = (self.df.loc[:, x].to_list() for x in ['language', 'url'])
        self.urls = tuple(zip(a, b))

    def __str__(self):
        # This is the output when you do 'print(item)'
        output = {'index': self.index,
                  'Qcode': self.qcode,
                  'Label': self.itemLabel,
                  'Number of URLs': len(self.urls)}
        return str(output)


def dl_webpages(item, temp_destination='dl_temp', archive=False, interval=1):
    """
    Downloads webpages in `item.urls` and stores them in the `destination`
    folder in the format: `destination/index_qcode_itemLabel/language`

    :param item: an `item` object
    :param destination: directory to save the webpage.html's into
    :param archive: Default False, saves the .htmls of each item into a zipfile
    :param interval: Time (in seconds) between each request. Default 1 second
    """
    print(f"Downloading webpages for {item.itemLabel}..")

    # Make the directory:
    filename = f"{item.index}_{item.qcode}_{item.itemLabel}"
    directory = pathlib.Path(f"{temp_destination}/{filename}/")
    if not directory.exists():
        os.makedirs(directory)

    # Retrieve .HTML files:
    for pair in item.urls:
        lang, url_raw = (pair[x] for x in [0, 1])
        # This next line converts non-ASCII characters into URL-safe ones
        url = url_raw[0:30] + urlp.quote(url_raw[30:])
        try:
            urlq.urlretrieve(url, (f"{directory}/{lang}.html"))
            time.sleep(interval)

        except Exception as e:
            print(f'Problem with {item}:')
            print(e)
            time.sleep(interval)

    if archive:
        """
        If true, will compress .html files into a zip for each food
        (I've tried a few compression algorithms;
        lzma is the best algorithm for this, it seems).
        """
        with zipfile.ZipFile(
                            directory.cwd() / f"archive_cache/{filename}.zip",
                            mode="w",
                            compression=zipfile.ZIP_LZMA,
                            compresslevel=9
                            ) as archive:

            for file_path in directory.rglob("*"):
                # file_path is like: dl_test/0_Q4287_margarine/ast.html'
                archive.write(filename=file_path,       # file to compress
                              arcname=file_path.name)   # filename in archive
                # Note: file_path.name yields 'ast.html'

        shutil.rmtree(directory)

    print("Done!")
