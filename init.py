import csv

import pandas as pd
import numpy as np
from tools import normalize
import tensorflow as tf
from tensorflow import keras
from keras import layers

import filenames

MALWAREIDX = 23
BATCH_SIZE = 10

arm_training = pd.read_csv(filenames.arm_training, header=None, index_col=False)
arm_validation = pd.read_csv(filenames.arm_validation, header=None, index_col=False)
arm_test = pd.read_csv(filenames.arm_test, header=None, index_col=False)

dataset_arm_training = np.asarray(arm_training.drop(columns=arm_training.columns[-2:]))
dataset_arm_validation = np.asarray(arm_validation.drop(columns=arm_validation.columns[-2:]))
dataset_arm_test = np.asarray(arm_test.drop(columns=arm_test.columns[-2:]))

labels_arm_training = np.asarray(arm_training[arm_training.columns[-1]])
labels_arm_validation = np.asarray(arm_validation[arm_validation.columns[-1]])
labels_arm_test = np.asarray(arm_test[arm_test.columns[-1]])

names_arm_training = arm_training[arm_training.columns[-2]]
names_arm_validation = arm_validation[arm_validation.columns[-2]]
names_arm_test = arm_test[arm_test.columns[-2]]

df_arm_malware_forpoison = pd.read_csv(filenames.forpoison_arm_malware, header=None, index_col=False)
df_arm_malware_forpoison = df_arm_malware_forpoison.drop(columns=df_arm_malware_forpoison.columns[-2:])
topredict = np.asarray([df_arm_malware_forpoison.iloc[MALWAREIDX],])
