import json
import pandas as pd
import numpy as np
from tools import concatenator
import tensorflow as tf
import csv
from tensorflow import keras
from keras import layers
import sys
import filenames_modified as filenames

MALWAREIDX = int(sys.argv[1])
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


with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    # percents = np.append(np.arange(0.5, 5.1, 0.5), [10, 20])
    percents = [5, 10, 20, 50, 100]
    for number in range(10, 101, 10):
        with open(filenames.dir_results + "iterative_idx-" + str(MALWAREIDX) + "_benignnumber-" + str(number) + "_percent-5-10-20-50-100.csv", "w") as result_file:
            csv_writer_r = csv.writer(result_file, lineterminator="\n")
            # for byte in range(1000, 101001, 10000):
            for percent in percents:
                # print("*{} - {}%*".format(number, percent))
                with open(filenames.dir_poison_data_iterative + "poisoned_benign_malware_" + str(percent) + "_" + str(MALWAREIDX) + ".csv", "w") as f:
                    # with open("files\\poison_data\\poisoned_benign_malware.csv", "w") as f:
                    csv_writer = csv.writer(f, lineterminator="\n")
                    malware = filenames.dir_malware_arm + str(poison["arm"]["malware"][MALWAREIDX])
                    for i in range(number):
                        benign = filenames.dir_bening_arm + str(poison["arm"]["benign"][i])
                        with open(benign, "rb") as benignfile:
                            lenbytes = len(benignfile.read())
                        byte = int(lenbytes * percent / 100)
                        csv_writer.writerow(concatenator(file1=benign, file2=malware, bit=1, byte2=byte))

                file_poison_arm_BM = filenames.dir_poison_data_iterative + "poisoned_benign_malware_" + str(percent) + "_" + str(MALWAREIDX) + ".csv"
                poisoned_arm_training = pd.read_csv(file_poison_arm_BM, index_col=False, header=None)

                poisoned_arm_training_base = poisoned_arm_training.sample(frac=1)
                poisoned_arm_training_new = arm_training.append(poisoned_arm_training, ignore_index=True).sample(
                    frac=1)

                dataset_poisoned_arm_training_base = np.asarray(
                    poisoned_arm_training_base.drop(columns=poisoned_arm_training_base.columns[-2:]))
                dataset_poisoned_arm_training_new = np.asarray(
                    poisoned_arm_training_new.drop(columns=poisoned_arm_training_new.columns[-2:]))

                labels_poisoned_arm_training_base = np.asarray(
                    poisoned_arm_training_base[poisoned_arm_training_base.columns[-1]])
                labels_poisoned_arm_training_new = np.asarray(
                    poisoned_arm_training_new[poisoned_arm_training_new.columns[-1]])

                # MODIFIED
                base_model = keras.models.load_model(filenames.base_model)
                base_model.fit(dataset_poisoned_arm_training_base, labels_poisoned_arm_training_base, epochs=10, batch_size=BATCH_SIZE,
                               validation_data=(dataset_arm_validation, labels_arm_validation), verbose=0)
                [_, binary_accuracy_appended] = base_model.evaluate(dataset_arm_test, labels_arm_test, verbose=0)
                # print(binary_accuracy_appended)
                # base_model.save(filenames.models_iterative + "modified" + str(byte))

                [[predict_appended]] = base_model.predict(topredict, verbose=0)
                # print(predict_appended)

                # NEW
                poison_model = keras.Sequential(
                    [
                        layers.Dense(1, input_shape=(131,), activation="sigmoid")
                    ]
                )
                poison_model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                                     metrics=[tf.keras.metrics.BinaryAccuracy()])
                poison_model.fit(dataset_poisoned_arm_training_new, labels_poisoned_arm_training_new, epochs=10, batch_size=BATCH_SIZE,
                                 validation_data=(dataset_arm_validation, labels_arm_validation), verbose=0)
                [_, binary_accuracy_new] = poison_model.evaluate(dataset_arm_test, labels_arm_test, verbose=0)
                # print(binary_accuracy_appended)
                # base_model.save(filenames.models_iterative + "poison" + str(byte))

                [[predict_new]] = poison_model.predict(topredict, verbose=0)
                # print(predict_new)

                results = [percent,
                           binary_accuracy_appended,
                           predict_appended,
                           binary_accuracy_new,
                           predict_new]
                # print(results)
                csv_writer_r.writerow(results)
print("{} DONE".format(MALWAREIDX))