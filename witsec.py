import json
import csv

import tlsh

with open("files\\witsec\\hash", "w") as file:
    with open("files\\witsec\\file1", "rb") as f:
        file.write(tlsh.hash(f.read())+"\n")
    with open("files\\witsec\\file2", "rb") as f:
        file.write(tlsh.hash(f.read()))
