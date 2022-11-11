from pathlib import Path
import tlsh
import os
import csv
import pandas as pd

import filenames
from tools import framer


def separator(df):
    df_training = df.iloc[:1440, :]
    df_validation = df.iloc[1440:1620, :]
    df_test = df.iloc[1620:1800, :]
    df_forpoison = df.iloc[1800:2000, :]
    return df_training, df_validation, df_test, df_forpoison


df_malware_arm = framer(filenames.dir_malware_arm, 0)
df_malware_mips = framer(filenames.dir_malware_mips, 0)
df_benign_arm = framer(filenames.dir_bening_arm, 1)
df_benign_mips = framer(filenames.dir_bening_mips, 1)

df_arm_malware_training, \
df_arm_malware_validation, \
df_arm_malware_test, \
df_arm_malware_forpoison = \
    separator(df_malware_arm)

df_mips_malware_training, \
df_mips_malware_validation, \
df_mips_malware_test, \
df_mips_malware_forpoison = \
    separator(df_malware_mips)

df_arm_benign_training, \
df_arm_benign_validation, \
df_arm_benign_test, \
df_arm_benign_forpoison = \
    separator(df_benign_arm)

df_mips_benign_training, \
df_mips_benign_validation, \
df_mips_benign_test, \
df_mips_benign_forpoison = \
    separator(df_benign_mips)

df_arm_malware_training \
    .append(df_arm_benign_training) \
    .sample(frac=1) \
    .to_csv(filenames.arm_training, header=False, index=False)
df_arm_malware_validation \
    .append(df_arm_benign_validation) \
    .sample(frac=1) \
    .to_csv(filenames.arm_validation, header=False, index=False)
df_arm_malware_test \
    .append(df_arm_benign_test) \
    .sample(frac=1) \
    .to_csv(filenames.arm_test, header=False, index=False)

df_arm_malware_forpoison \
    .sample(frac=1) \
    .to_csv(filenames.forpoison_arm_malware, header=False, index=False)
df_arm_benign_forpoison \
    .sample(frac=1) \
    .to_csv(filenames.forpoison_arm_benign, header=False, index=False)

df_mips_malware_training \
    .append(df_mips_benign_training) \
    .sample(frac=1) \
    .to_csv(filenames.mips_training, header=False, index=False)
df_mips_malware_validation \
    .append(df_mips_benign_validation) \
    .sample(frac=1) \
    .to_csv(filenames.mips_validation, header=False, index=False)
df_mips_malware_test \
    .append(df_mips_benign_test) \
    .sample(frac=1) \
    .to_csv(filenames.mips_test, header=False, index=False)

df_mips_malware_forpoison \
    .sample(frac=1) \
    .to_csv(filenames.forpoison_mips_malware, header=False, index=False)
df_mips_benign_forpoison \
    .sample(frac=1) \
    .to_csv(filenames.forpoison_mips_benign, header=False, index=False)

# df_malware_arm.to_csv("files/int_malware_arm", index=False)

# print(*hashlist, sep = "\n")
# with open("int_malware_arm.csv","w") as f:
# 	csv_writer=csv.writer(f)
# 	for row in hashlist:
# 		csv_writer.writerow(row)
