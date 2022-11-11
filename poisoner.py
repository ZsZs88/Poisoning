import csv
import json

import filenames
from tools import concatenator
import tlsh

with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    for byte in range(1000, 101001, 10000):
        with open("files\\poison_data\\poisoned_benign_malware_" + str(byte) + ".csv", "w") as f:
    #with open("files\\poison_data\\poisoned_benign_malware.csv", "w") as f:
            csv_writer = csv.writer(f, lineterminator="\n")
            for i in range(40):
                malware = filenames.dir_malware_arm + str(poison["arm"]["malware"][0])
                benign = filenames.dir_bening_arm + str(poison["arm"]["benign"][i])
                csv_writer.writerow(concatenator(file1=benign, file2=malware, bit=1, byte2=byte))

# with open("files\\poison_filenames.json") as poison_json:
#     poison = json.load(poison_json)
#     with open("files\\poison_data\\poisoned_malware_benign.csv", "w") as f:
#         csv_writer = csv.writer(f)
#         for i in range(200):
#             malware = dir_malware_arm + str(poison["arm"]["malware"][i])
#             benign = dir_bening_arm + str(poison["arm"]["benign"][i])
#             csv_writer.writerow(concatenator(file1=malware, file2=benign, bit=1))
