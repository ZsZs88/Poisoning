import numpy as np
import pandas as pd
import pprint
import filenames


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

base_colors = [
    "#FF99FF",
    "#99CCFF",
    "#66FF66",
    "#FFAC33",
    "#FF7575"
]


def myquery(df, _query):
    # print("\n\nDataset Statistics")
    # print(df.describe())
    print("\n{}".format(_query))
    print(df.query(_query).describe())


def myplot(df, plotname, acc=False):
    cols = df.columns
    len_cols = len(cols)
    # colors = list(map(lambda x: "C{}".format(x + (1 if acc else 0)), range(len_cols - 1)))
    colors = base_colors[(1 if acc else 0):(len_cols - 1 + (1 if acc else 0))]
    patches = [mpatches.Patch(color="r", label="Decision Point")]
    for i in range(len_cols - 1):
        patches.append(mpatches.Patch(color=base_colors[i + (1 if acc else 0)], label=cols[i + 1]))

    plt.figure()

    for row in list(df.itertuples(index=False, name=None)):
        x = row[0]
        data = row[1:]

        for i, (pred, color) in enumerate(sorted(zip(data, colors))):
            plt.bar(x, pred, color=color, zorder=-i, )
    plt.axhline(y=0.5, color='r', linestyle='-.', linewidth=0.6)
    plt.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig('..\\files\\plots\\{}.png'.format(plotname), dpi=1200, bbox_inches='tight')

    # plt.show()


print("\n\nPREDS")
for i in [20, 30, 40, 50]:
    df = pd.read_csv("..\\{}genetic_by_benignnumber{}_preds.csv".format(filenames.dir_aggregated, i), index_col=False)[
        ["index", "BasePred", "5%", "10%", "20%"]]
    print("\n\n{}".format(i))
    print("\n\nDataset Statistics")
    print(df.describe())
    myquery(df, '`5%` >= 0.5')
    myquery(df, '`10%` >= 0.5')
    myquery(df, '`20%` >= 0.5')
    print(f"\nVariance: \n{df.var()}")

print("\n\nACCS")
for i in [20, 30, 40, 50]:
    df = \
        pd.read_csv("..\\{}genetic_by_benignnumber{}_accs.csv".format(filenames.dir_aggregated, i), index_col=False)[
            ["index", "5%", "10%", "20%"]
        ]
    print("\n\n{}".format(i))
    print("\n\nDataset Statistics")
    print(df.describe())
    print(f"\nVariance: \n{df.var()}")


# for i in [5, 10, 20]:
#     df = pd.read_csv("..\\{}genetic_by_percent{}_preds.csv".format(filenames.dir_aggregated, i), index_col=False)[
#         ["index", "BasePred", "20", "30", "40", "50"]]
#     myplot(df, "eval_genetic_by_percent{}_preds".format(i), acc=False)
#     # input()
#
# for i in [5, 10, 20]:
#     df = pd.read_csv("..\\{}genetic_by_percent{}_accs.csv".format(filenames.dir_aggregated, i), index_col=False)[
#         ["index", "20", "30", "40", "50"]]
#     myplot(df, "eval_genetic_by_percent{}_accs".format(i), acc=True)
#     # input()
