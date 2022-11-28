import csv
import json

import keras.models
import numpy as np
from init import df_arm_malware_forpoison as df

import filenames

base_model = keras.models.load_model(filenames.base_model)
with open(filenames.poisonJSON, "r") as poisonJSON:
    poison = json.load(poisonJSON)
    with open("files\\predictions.csv", "w") as f:
        for i in range(200):
            [[prediction]] = base_model.predict(np.asarray([df.iloc[i],]), verbose = 0)
            with open(filenames.dir_malware_arm + poison["arm"]["malware"][i], "rb") as file:
                size = len(file.read())
            f.write("{},{},{}\n".format(i, prediction, size))