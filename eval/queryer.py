import numpy as np
import pandas as pd
import filenames


def myquery(filename, _query):
    df = pd.read_csv(filename, index_col=False)
    print("\n\nDataset Statistics")
    print(df.describe())
    print("\n{}".format(_query))
    print(df.query(_query).describe())


# myquery(filenames.dir_aggregated + "adversary_by_idx.csv", '`5%` >= 0.5')
# myquery(filenames.dir_aggregated + "adversary_by_idx.csv", '`10%` >= 0.5')
# myquery(filenames.dir_aggregated + "adversary_by_idx.csv", '`20%` >= 0.5')