import csv

import keras.models
import numpy as np
from init import df_arm_malware_forpoison as df

import filenames

base_model = keras.models.load_model(filenames.base_model)
with open("files\\predictions.csv", "w") as f:
    for i in range(200):
        [[prediction]] = base_model.predict(np.asarray([df.iloc[i],]), verbose = 0)
        f.write("{},{}\n".format(i,prediction))