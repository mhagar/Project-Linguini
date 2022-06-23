# This script defines a function which uses 'URLtoHTML.py' to cache a given
# number of items into the archive
# Mostafa 2022/03/04

import URLtoHTML as UtH
import pandas as pd


def cache(begin=0, end=4, URL_set='datasets/small_URL_dataset'):
    df = pd.read_pickle(URL_set)

    for i in range(begin, end):
        food = UtH.item(df.loc[i])
        UtH.dl_webpages(
                        food,
                        temp_destination='dl_temp',
                        archive=True,
                        interval=1
                        )
