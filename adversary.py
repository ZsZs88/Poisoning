import csv

import numpy
import numpy as np
import pandas as pd
import pygad
import tlsh
import json
import filenames
import init
import tools
from tools import normalize
from tools import featurer

import tensorflow as tf
from tensorflow import keras
from keras import layers


def myfunc(solution):
    additional = np.array(solution).tobytes()
    return str(tlsh.hash(mybytes + additional))


def fitness_func(solution, solution_idx):
    poisonedTLSH = myfunc(solution)
    to_predict = np.asarray([tools.featurer(poisonedTLSH)[:-2], ])
    [[prediction]] = model.predict(to_predict, verbose = 0)
    #print(to_predict, " - ", 1 - prediction)
    return prediction


mybytes = ""

with open (filenames.dir_results + "adversary_genetic_200gen.csv", "w") as f:
    csv_writer = csv.writer(f, lineterminator = "\n")
    with open(filenames.poisonJSON) as poison_json:
        poison = json.load(poison_json)
        db = 0
        i = 0
        while db < 20:
            malware_file_name = str(poison["arm"]["malware"][i])
            with open(filenames.dir_malware_arm + malware_file_name, "rb") as malware:
                mybytes = malware.read()
            i += 1

            lenbytes = len(mybytes)
            if lenbytes < 5000:
                pass
            else:
                db += 1

            model = keras.models.load_model(filenames.base_model)

            [[pred]] = model.predict(np.asarray([tools.featurer(tlsh.hash(mybytes))[:-2],]))
            print(pred)

            num_generations = 200
            num_parents_mating = 8
            sol_per_pop = 20
            # num_genes = 1440
            gene_type = numpy.uint8
            init_range_low = 0
            init_range_high = 255
            stop_criteria = "saturate_200"

            for percent in np.arange(0.5, 5.5, 0.5):
                num_genes = int(lenbytes * percent / 100)
                print("-------------" + str(num_genes) + "-------------")
                ga = pygad.GA(num_generations=num_generations,
                              num_parents_mating=num_parents_mating,
                              fitness_func=fitness_func,
                              sol_per_pop=sol_per_pop,
                              num_genes=num_genes,
                              gene_type=gene_type,
                              init_range_low=init_range_low,
                              init_range_high=init_range_high,
                              # stop_criteria=stop_criteria
                          )
                ga.run()
                ga.plot_fitness()
                best_solution, best_fitness, best_idx = ga.best_solution()
                # print(best_solution, " - ", best_fitness)
                csv_writer.writerow([malware_file_name, lenbytes, percent, best_fitness])
