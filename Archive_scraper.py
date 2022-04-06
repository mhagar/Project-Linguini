# This script scrapes the pages archived in `archive_cache/` using the function
# defined in `HTMLAnalyzer.py`
# Mostafa | 2022/03/14

import zipfile
import HTMLAnalyzer
import pathlib
import pandas as pd
import re


def scrape_archive(
                   range=(0, 5),
                   source="archive_cache/",
                   destination="archive_scrapings/"
                   ):
    """
    Scrapes the `.zip` files in `/archive_cache` and uses the `analyze()`
    function in `HTMLAnalyzer.py`.

        :param: range - tuple which describes which files to scrape
                        (default:`(0,5)`)

        :param: source - location of cache archive
                        (default:`archive_cache/`)

        :param: destination - path to save pickled DataFrame
                        (default:`archive_scrapings/`)
    """
    archive_directory = pathlib.Path(source)
    archive_list = [x for x in archive_directory.rglob('*_Q*.zip')]
    df_list = []

    # import pdb; pdb.set_trace();

    for dir in archive_list:  # each `dir` is like "0_Q4287_margarine.zip"
        rows = []  # rows that will be added to `df`
        with zipfile.ZipFile(
                             dir,
                             mode="r",
                             compression=zipfile.ZIP_LZMA,
                             compresslevel=9
                             ) as archive:

            files = [x.filename for x in archive.infolist()]
            # Outputs list of files in the `.zip`
            for article in files:  # `file` is like "en.html"
                name = dir.name  # '0_Q4287_margarine'
                row = {
                       'Index': re.search('(.*)_Q[0-9]', name).group()[:-3],
                       'QCode': re.search('_Q(.*)_', name).group()[1:-1]
                      }  # i.e '0' and 'Q4287'
                lang_code = article[:-5]  # this removes the `.html`
                analysis = HTMLAnalyzer.analyze(archive.read(article))
                row.update({'lang': lang_code})
                row.update(analysis)
                rows.append(row)

        df_list.append(rows)

    # import pdb; pdb.set_trace()
    # So what you can do is..
    df = pd.concat([pd.DataFrame(x) for x in df_list])

    return df


if __name__ == "__main__":
    scrape_archive()
