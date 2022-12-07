import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

import pandas as pd

import filenames


base_colors = [
    "#FF99FF",
    "#99CCFF",
    "#66FF66",
    "#FFAC33",
    "#FF7575"
]

def myplot(filename, plotname):
    df = pd.read_csv(filename, index_col=False)
    cols = df.columns
    len_cols = len(cols)
    # print(len_cols)
    # print(base_colors[:len_cols-1])
    # colors = list(map(lambda x: "C{}".format(x), range(len_cols - 1)))
    colors = base_colors[:len_cols-1]
    patches = [mpatches.Patch(color = "r", label = "Decision Point")]
    for i in range(len_cols - 1):
        patches.append(mpatches.Patch(color = colors[i], label = cols[i+1]))

    plt.figure()

    for row in list(df.itertuples(index=False, name=None)):
        x = row[0]
        data = row[1:]

        for i, (pred, color) in enumerate(sorted(zip(data, colors))):
            plt.bar(x, pred, color=color, zorder=-i, )
    plt.axhline(y=0.5, color='r', linestyle='-.', linewidth=0.6)
    plt.legend(handles = patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig('files\\plots\\{}.png'.format(plotname), dpi=1200, bbox_inches = 'tight')

    # plt.show()


myplot("{}adversary_by_idx.csv".format(filenames.dir_aggregated), "adversary_by_idx")
# for i in range(10, 101, 10):
#     for name in ["accs", "preds"]:
#         myplot("{}iterative_by_benignnumber{}_{}.csv".format(filenames.dir_aggregated, i, name), "iterative_by_benignnumber{}_{}".format(i, name))
# for i in [5, 10, 20, 50, 100]:
#     for name in ["accs", "preds"]:
#         myplot("{}iterative_by_percent{}_{}.csv".format(filenames.dir_aggregated, i, name), "iterative_by_percent{}_{}".format(i, name))
#         # input()