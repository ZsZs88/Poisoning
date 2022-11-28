import csv
import json
import pandas as pd
import numpy as np
import filenames
import init
from tools import normalize
from tools import concatenator
import tlsh

import tensorflow as tf
from tensorflow import keras
from keras import layers

with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    I = 84
    percents = np.append(np.arange(0.5, 5.1, 0.5), [10, 20])
    for number in range(10, 101, 10):
        with open(filenames.dir_results + "iterative_idx-" + str(I) + "_benignnumber-" + str(number) + "_percent-0.5-5-10-20.csv", "w") as result_file:
            csv_writer_r = csv.writer(result_file, lineterminator="\n")
            # for byte in range(1000, 101001, 10000):
            for percent in percents:
                print("-------------" + str(number) + "." + str(percent) + "-------------")
                with open(filenames.dir_poison_data_iterative + "poisoned_benign_malware_" + str(percent) + ".csv", "w") as f:
                    # with open("files\\poison_data\\poisoned_benign_malware.csv", "w") as f:
                    csv_writer = csv.writer(f, lineterminator="\n")
                    malware = filenames.dir_malware_arm + str(poison["arm"]["malware"][I])
                    for i in range(number):
                        benign = filenames.dir_bening_arm + str(poison["arm"]["benign"][i])
                        with open(benign, "rb") as benignfile:
                            lenbytes = len(benignfile.read())
                        byte = int(lenbytes * percent / 100)
                        csv_writer.writerow(concatenator(file1=benign, file2=malware, bit=1, byte2=byte))

                file_poison_arm_BM = filenames.dir_poison_data_iterative + "poisoned_benign_malware_" + str(percent) + ".csv"
                poisoned_arm_training = pd.read_csv(file_poison_arm_BM, index_col=False, header=None)

                poisoned_arm_training_base = poisoned_arm_training.sample(frac=1)
                poisoned_arm_training_new = init.arm_training.append(poisoned_arm_training, ignore_index=True).sample(
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
                base_model.fit(dataset_poisoned_arm_training_base, labels_poisoned_arm_training_base, epochs=10, batch_size=init.BATCH_SIZE,
                               validation_data=(init.dataset_arm_validation, init.labels_arm_validation), verbose=0)
                [_, binary_accuracy_appended] = base_model.evaluate(init.dataset_arm_test, init.labels_arm_test, verbose=0)
                # print(binary_accuracy_appended)
                # base_model.save(filenames.models_iterative + "modified" + str(byte))

                [[predict_appended]] = base_model.predict(init.topredict, verbose=0)
                # print(predict_appended)

                # NEW
                poison_model = keras.Sequential(
                    [
                        layers.Dense(1, input_shape=(131,), activation="sigmoid")
                    ]
                )
                poison_model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                                     metrics=[tf.keras.metrics.BinaryAccuracy()])
                poison_model.fit(dataset_poisoned_arm_training_new, labels_poisoned_arm_training_new, epochs=10, batch_size=init.BATCH_SIZE,
                                 validation_data=(init.dataset_arm_validation, init.labels_arm_validation), verbose=0)
                [_, binary_accuracy_new] = poison_model.evaluate(init.dataset_arm_test, init.labels_arm_test, verbose=0)
                # print(binary_accuracy_appended)
                # base_model.save(filenames.models_iterative + "poison" + str(byte))

                [[predict_new]] = poison_model.predict(init.topredict, verbose=0)
                # print(predict_new)

                results = [percent,
                           binary_accuracy_appended,
                           predict_appended,
                           binary_accuracy_new,
                           predict_new]
                # print(results)
                csv_writer_r.writerow(results)
