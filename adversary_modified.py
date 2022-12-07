import csv
import sys
import numpy
import numpy as np
import pygad
import tlsh
import json
import filenames_modified as filenames
import tools
from tensorflow import keras

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

percents = [5, 10, 20]
MALWAREIDX = int(sys.argv[1])

with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    with open (filenames.dir_results + "adversary_genetic_500gen{}.csv".format(MALWAREIDX), "w") as f:
        csv_writer = csv.writer(f, lineterminator = "\n")

        malware_file_name = str(poison["arm"]["malware"][MALWAREIDX])
        with open(filenames.dir_malware_arm + malware_file_name, "rb") as malware:
            mybytes = malware.read()

        lenbytes = len(mybytes)
        model = keras.models.load_model(filenames.base_model)

        [[pred]] = model.predict(np.asarray([tools.featurer(tlsh.hash(mybytes))[:-2],]), verbose=0)
        print(pred)

        num_generations = 500
        num_parents_mating = 8
        sol_per_pop = 20
        # num_genes = 1440
        gene_type = numpy.uint8
        init_range_low = 0
        init_range_high = 255
        stop_criteria = "saturate_200"

        for percent in percents:
            num_genes = int(lenbytes * percent / 100)
        # for num_genes in range(100, 1001, 200):
        #     percent = num_genes / lenbytes * 100
        # percent = 10
        # num_genes = int(lenbytes * percent / 100)
            print("-------------" + str(MALWAREIDX) + "." + str(num_genes) + "-------------")
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
            ga.plot_fitness()
            best_solution, best_fitness, best_idx = ga.best_solution()
            # print(best_solution, " - ", best_fitness)
            # print([malware_file_name, lenbytes, percent, best_fitness])
            csv_writer.writerow([malware_file_name, lenbytes, percent, best_fitness])

print("{} DONE".format(MALWAREIDX))
