import json

import pandas as pd
import numpy as np

import filenames

myjson = {
    "arm": {
        "malware": [],
        "benign": []
    },
    "mips": {
        "malware": [],
        "bening": []
    }
}

df_arm_malware_forpoison = pd.read_csv(filenames.forpoison_arm_malware, header=None, index_col=False)
myjson["arm"]["malware"] = \
    df_arm_malware_forpoison[df_arm_malware_forpoison.columns[-2]].tolist()
df_arm_benign_forpoison = pd.read_csv(filenames.forpoison_arm_benign, header=None, index_col=False)
myjson["arm"]["benign"] = \
    df_arm_benign_forpoison[df_arm_benign_forpoison.columns[-2]].tolist()

df_mips_malware_forpoison = pd.read_csv(filenames.forpoison_mips_malware, header=None, index_col=False)
myjson["mips"]["malware"] = \
    df_mips_malware_forpoison[df_mips_malware_forpoison.columns[-2]].tolist()
df_mips_benign_forpoison = pd.read_csv(filenames.forpoison_mips_benign, header=None, index_col=False)
myjson["mips"]["benign"] = \
    df_mips_benign_forpoison[df_mips_benign_forpoison.columns[-2]].tolist()

with open(filenames.poisonJSON, "w") as f:
    json.dump(myjson, f)
