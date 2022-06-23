# This script uses URLtoHTML.py to cache some .html files into '/archive'.
# Later on, I hope to cache *ALL* the articles - but for now this should
# enable the development of a data analysis pipeline
# Mostafa 2022/03/04

import URLtoHTML as UtH
import pandas as pd

df = pd.read_pickle('datasets/small_URL_dataset')
begin = 0
end = 4

for i in range(begin, end):
    food = UtH.item(df.loc[i])
    UtH.dl_webpages(
                    food,
                    temp_destination='dl_temp',
                    archive=True,
                    interval=1
                    )
