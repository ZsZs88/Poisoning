import csv

import numpy
import numpy as np
import pandas as pd
import pygad
import tlsh
import json
import filenames
import init
from tools import normalize
from tools import featurer

import tensorflow as tf
from tensorflow import keras
from keras import layers

malwareTLSH = ""
mybytes = ""

def myfunc(solution):
    additional = np.array(solution).tobytes()
    return str(tlsh.hash(mybytes + additional))

def fitness_func(solution, solution_idx):
    poisonedTLSH = myfunc(solution)
    return 1 / tlsh.diff(malwareTLSH, poisonedTLSH)


num_generations = 500
num_parents_mating = 8
sol_per_pop = 20
# num_genes = 20
gene_type = numpy.uint8
init_range_low = 0
init_range_high = 255
stop_criteria = "saturate_200"

# percents = np.append(np.arange(0.5, 5.1, 0.5), [10, 20])
percents = [5, 10, 20]

with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    with open(filenames.dir_malware_arm + str(poison["arm"]["malware"][init.MALWAREIDX]), "rb") as malware:
        malwareread = malware.read()
        malwareTLSH = str(tlsh.hash(malwareread))
    with open("{}genetic_idx-{}_bening-20_percent-5-10-20.csv".format(filenames.dir_results, init.MALWAREIDX), "w") as results_file:
        csv_writer_r = csv.writer(results_file, lineterminator="\n")
        for percent in percents:
        # for num_genes in range(10, 101, 10):
            with open(filenames.dir_poison_data_genetic + "percent_" + str(percent) + ".csv", "w") as f:
                csv_writer = csv.writer(f, lineterminator="\n")
                for i in range(20):
                    print("*{}% - {}*".format(percent, i))
                    filename = str(poison["arm"]["benign"][i])
                    with open(filenames.dir_bening_arm + filename, "rb") as benign:
                        mybytes = benign.read()
                    lenbytes = len(mybytes)
                    num_genes = int(lenbytes * percent / 100)
                    ga = pygad.GA(num_generations=num_generations,
                                  num_parents_mating=num_parents_mating,
                                  fitness_func=fitness_func,
                                  sol_per_pop=sol_per_pop,
                                  num_genes=num_genes,
                                  gene_type=gene_type,
                                  init_range_low=init_range_low,
                                  init_range_high=init_range_high,
                                  stop_criteria=stop_criteria
                                  )
                    ga.run()
                    # ga.plot_fitness()
                    best_solution, best_fitness, best_idx = ga.best_solution()
                    # print(best_solution, " - ", 1 / best_fitness)

                    csv_writer.writerow(featurer(myfunc(best_solution)))


            file_poison_arm_BM = filenames.dir_poison_data_genetic + "percent_" + str(percent) + ".csv"
            poisoned_arm_training = pd.read_csv(file_poison_arm_BM, index_col=False, header=None)

            poisoned_arm_training_base = poisoned_arm_training.sample(frac=1)
            poisoned_arm_training_new = init.arm_training.append(poisoned_arm_training, ignore_index=True).sample(frac=1)

            dataset_poisoned_arm_training_base = np.asarray(
                poisoned_arm_training_base.drop(columns=poisoned_arm_training_base.columns[-2:]))
            dataset_poisoned_arm_training_new = np.asarray(
                poisoned_arm_training_new.drop(columns=poisoned_arm_training_new.columns[-2:]))

            labels_poisoned_arm_training_base = np.asarray(poisoned_arm_training_base[poisoned_arm_training_base.columns[-1]])
            labels_poisoned_arm_training_new = np.asarray(poisoned_arm_training_new[poisoned_arm_training_new.columns[-1]])

            # MODIFIED
            base_model = keras.models.load_model(filenames.base_model)
            base_model.fit(dataset_poisoned_arm_training_base, labels_poisoned_arm_training_base, epochs=10, batch_size=init.BATCH_SIZE,
                           validation_data=(init.dataset_arm_validation, init.labels_arm_validation), verbose=0)
            [_, binary_accuracy_appended] = base_model.evaluate(init.dataset_arm_test, init.labels_arm_test, verbose=0)
            # print(binary_accuracy_appended)
            # base_model.save(filenames.models_iterative + "modified" + str(num_genes))

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
            # base_model.save(filenames.models_iterative + "poison" + str(num_genes))

            [[predict_new]] = poison_model.predict(init.topredict, verbose=0)
            # print(predict_new)

            results = [percent,
                       binary_accuracy_appended,
                       predict_appended,
                       binary_accuracy_new,
                       predict_new]
            print(results)

            csv_writer_r.writerow(results)