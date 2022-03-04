# This script expands the dataset using URLs
# This file isn't needed, the code's been refactored into "getURLs.py"

import pandas as pd

raw_df = pd.read_pickle('small_URL_dataset')  # picks up where I left off
# 'test_URL_dataset' is just a test with 50 entries

expanded_df = pd.DataFrame(columns=['item', 'itemLabel', 'language', 'url'])

for i in range(0, 50):
    raw_row = raw_df.loc[i].to_dict()
    expanded_row = []
    for n in raw_row['urls']:
        expanded_row.append({'index': i,
                             'item': raw_row['item'],
                             'itemLabel': raw_row['itemLabel'],
                             'language': n[8:10],
                             'url': n})

    expansion = pd.DataFrame(expanded_row).set_index('index')

    expanded_df = expanded_df.append(expansion)


import pdb; pdb.set_trace()
# expanded_df.to_pickle('small_URL_dataset_expanded')
