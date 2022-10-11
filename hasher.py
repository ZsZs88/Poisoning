from pathlib import Path
import tlsh
import os
import csv
import pandas as pd


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

    namefile = dirname.split("/")[-2:]
    namefile = str(namefile[1]) + "_" + str(namefile[0]) + ".txt"
    with open(namefile) as filenames:
        for path in pathlist:
            path_in_str = str(path)
            if (not os.path.isdir(path_in_str)):
                filenames.write(path_in_str.split("/")[-1] + "\n")
                with open(path_in_str, "rb") as f:
                    hash = str(tlsh.hash(f.read()))
                    hashlist.append(featurer(hash, path_in_str.split("/")[-1], bit))
    return pd.DataFrame(hashlist).sample(frac=1)


def separator(df):
    df_clean_training = df.iloc[:800, :]
    df_clean_validation = df.iloc[800:900, :]
    df_clean_test = df.iloc[900:1000, :]
    df_poisoned_training = df.iloc[1000:1800, :]
    df_poisoned_validation = df.iloc[1800:1900, :]
    df_poisoned_test = df.iloc[1900:2000, :]
    return df_clean_training, df_clean_validation, df_clean_test, df_poisoned_training, df_poisoned_validation, df_poisoned_test


dir_malware_arm = "/home/kali/Downloads/ml-sample-pack-small/malware/arm"
dir_malware_mips = "/home/kali/Downloads/ml-sample-pack-small/malware/mips"
dir_bening_arm = "/home/kali/Downloads/ml-sample-pack-small/benign/arm"
dir_bening_mips = "/home/kali/Downloads/ml-sample-pack-small/benign/mips"

df_malware_arm = framer(dir_malware_arm, 0)
df_malware_mips = framer(dir_malware_mips, 0)
df_benign_arm = framer(dir_bening_arm, 1)
df_benign_mips = framer(dir_bening_mips, 1)

df_arm_malware_clean_training, \
df_arm_malware_clean_validation, \
df_arm_malware_clean_test, \
df_arm_malware_poisoned_training, \
df_arm_malware_poisoned_validation, \
df_arm_malware_poisoned_test = \
    separator(df_malware_arm)

print(df_arm_malware_poisoned_test.head())

df_mips_malware_clean_training, \
df_mips_malware_clean_validation, \
df_mips_malware_clean_test, \
df_mips_malware_poisoned_training, \
df_mips_malware_poisoned_validation, \
df_mips_malware_poisoned_test = \
    separator(df_malware_mips)

df_arm_benign_clean_training, \
df_arm_benign_clean_validation, \
df_arm_benign_clean_test, \
df_arm_benign_poisoned_training, \
df_arm_benign_poisoned_validation, \
df_arm_benign_poisoned_test = \
    separator(df_benign_arm)

df_mips_benign_clean_training, \
df_mips_benign_clean_validation, \
df_mips_benign_clean_test, \
df_mips_benign_poisoned_training, \
df_mips_benign_poisoned_validation, \
df_mips_benign_poisoned_test = \
    separator(df_benign_mips)

df_arm_malware_poisoned_training\
    .append(df_arm_benign_poisoned_training)\
    .sample(frac = 1)\
    .to_csv("files/arm_poisoned_training.csv", header=False, index=False)
df_arm_malware_poisoned_validation\
    .append(df_arm_benign_poisoned_validation)\
    .sample(frac = 1)\
    .to_csv("files/arm_poisoned_validation.csv", header=False, index=False)
df_arm_malware_poisoned_test\
    .append(df_arm_benign_poisoned_test)\
    .sample(frac = 1)\
    .to_csv("files/arm_poisoned_test.csv", header=False, index=False)
df_arm_malware_clean_training\
    .append(df_arm_benign_clean_training)\
    .sample(frac = 1)\
    .to_csv("files/arm_clean_training.csv", header=False, index=False)
df_arm_malware_clean_validation\
    .append(df_arm_benign_clean_validation)\
    .sample(frac = 1)\
    .to_csv("files/arm_clean_validation.csv", header=False, index=False)
df_arm_malware_clean_test\
    .append(df_arm_benign_clean_test)\
    .sample(frac = 1)\
    .to_csv("files/arm_clean_test.csv", header=False, index=False)

df_mips_malware_poisoned_training\
    .append(df_mips_benign_poisoned_training)\
    .sample(frac = 1)\
    .to_csv("files/mips_poisoned_training.csv", header=False, index=False)
df_mips_malware_poisoned_validation\
    .append(df_mips_benign_poisoned_validation)\
    .sample(frac = 1)\
    .to_csv("files/mips_poisoned_validation.csv", header=False, index=False)
df_mips_malware_poisoned_test\
    .append(df_mips_benign_poisoned_test)\
    .sample(frac = 1)\
    .to_csv("files/mips_poisoned_test.csv", header=False, index=False)
df_mips_malware_clean_training\
    .append(df_mips_benign_clean_training)\
    .sample(frac = 1)\
    .to_csv("files/mips_clean_training.csv", header=False, index=False)
df_mips_malware_clean_validation\
    .append(df_mips_benign_clean_validation)\
    .sample(frac = 1)\
    .to_csv("files/mips_clean_validation.csv", header=False, index=False)
df_mips_malware_clean_test\
    .append(df_mips_benign_clean_test)\
    .sample(frac = 1)\
    .to_csv("files/mips_clean_test.csv", header=False, index=False)

#df_malware_arm.to_csv("files/int_malware_arm", index=False)

# print(*hashlist, sep = "\n")
# with open("int_malware_arm.csv","w") as f:
# 	csv_writer=csv.writer(f)
# 	for row in hashlist:
# 		csv_writer.writerow(row)
