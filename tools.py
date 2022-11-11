import os
from pathlib import Path

import pandas as pd
import tlsh

def featurer(hash, filename, bit):
    hash = hash[4:]
    hash_bin_str = (bin(int(hash, base=16))[2:]).zfill(len(hash) * 4)
    featurelist = []
    featurelist.append(int(hash_bin_str[:8], 2))
    featurelist.append(int(hash_bin_str[8:12], 2))
    featurelist.append(int(hash_bin_str[12:16], 2))
    twobits = hash_bin_str[16:]
    n = 2
    for i in range(0, len(twobits), n):
        featurelist.append(int(twobits[i:i + n], 2))
    featurelist.append(filename)
    featurelist.append(bit)
    return featurelist

def framer(dirname, bit):
    pathlist = Path(dirname).rglob('*')

    hashlist = []

    namefile = dirname.split("\\")[-2:]
    namefile = "files\\filenames\\" + str(namefile[1]) + "_" + str(namefile[0]) + ".csv"
    with open(namefile, "w") as filenames:
        for path in pathlist:
            path_in_str = str(path)
            if (not os.path.isdir(path_in_str)):
                filenames.write(path_in_str.split("\\")[-1] + "\n")
                with open(path_in_str, "rb") as f:
                    hash = str(tlsh.hash(f.read()))
                    hashlist.append(featurer(hash, path_in_str.split("\\")[-1], bit))
    return pd.DataFrame(hashlist).sample(frac=1)


def concatenator(file1, file2, bit, byte1=-1, byte2=-1):
    with open(file1, "rb") as f1:
        with open(file2, "rb") as f2:
            # print(file1, file2)
            return featurer(str(tlsh.hash(f1.read(byte1) + f2.read(byte2))), str(file1).split("\\")[-1] + "_" + str(file2).split("\\")[-1], bit)