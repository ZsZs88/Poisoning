import csv
import json

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


def concatenator(file1, file2, bit, byte1=-1, byte2=-1):
    with open(file1, "rb") as f1:
        with open(file2, "rb") as f2:
            return featurer(str(tlsh.hash(f1.read(byte1) + f2.read(byte2))),
                            str(file1).split("/")[-1] + "_" + str(file2).split("/")[-1], bit)


dir_malware_arm = "/home/kali/Downloads/ml-sample-pack-small/malware/arm/"
dir_malware_mips = "/home/kali/Downloads/ml-sample-pack-small/malware/mips/"
dir_bening_arm = "/home/kali/Downloads/ml-sample-pack-small/benign/arm/"
dir_bening_mips = "/home/kali/Downloads/ml-sample-pack-small/benign/mips/"

with open("files/poison_filenames.json") as poison_json:
    poison = json.load(poison_json)
    with open("files/poison_data/poisoned_benign_malware.csv", "w") as f:
        csv_writer = csv.writer(f)
        for i in range(5):
            malware = dir_malware_arm + str(poison["arm"]["Attacker"]["Malware"][i])
            benign = dir_bening_arm + str(poison["arm"]["Attacker"]["Benign"][i])
            csv_writer.writerow(concatenator(file1=benign, file2=malware, bit=0))
        for i in range(5):
            malware = dir_malware_arm + str(poison["arm"]["Victim"]["Malware"][i])
            benign = dir_bening_arm + str(poison["arm"]["Victim"]["Benign"][i])
            csv_writer.writerow(concatenator(file1=benign, file2=malware, bit=0))

        with open("files/poison_data/poisoned_malware_benign.csv", "w") as f:
            csv_writer = csv.writer(f)
            for i in range(5):
                malware = dir_malware_arm + str(poison["arm"]["Attacker"]["Malware"][i])
                benign = dir_bening_arm + str(poison["arm"]["Attacker"]["Benign"][i])
                csv_writer.writerow(concatenator(file1=malware, file2=benign, bit=1))
            for i in range(5):
                malware = dir_malware_arm + str(poison["arm"]["Victim"]["Malware"][i])
                benign = dir_bening_arm + str(poison["arm"]["Victim"]["Benign"][i])
                csv_writer.writerow(concatenator(file1=malware, file2=benign, bit=1))
