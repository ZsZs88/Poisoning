import numpy
import numpy as np
import pygad
import tlsh
import json
import filenames

malwareTLSH = ""
filename = ""


def fitness_func(solution, solution_idx):
    with open(filenames.dir_bening_arm + filename, "rb") as benign:
        mybytes = benign.read()
        additional = np.array(solution).tobytes()
        poisonedTLSH = str(tlsh.hash(mybytes + additional))
    return 1/tlsh.diff(malwareTLSH, poisonedTLSH)


num_generations = 100
num_parents_mating = 4
sol_per_pop = 20
num_genes = 20
gene_type = numpy.uint8
init_range_low = 0
init_range_high = 255
stop_criteria = "saturate_20"



with open(filenames.poisonJSON) as poison_json:
    poison = json.load(poison_json)
    with open(filenames.dir_malware_arm + str(poison["arm"]["malware"][0]), "rb") as malware:
        malwareread= malware.read()
        malwareTLSH = str(tlsh.hash(malwareread))
    for i in range(10):
        filename = str(poison["arm"]["benign"][i])
        ga = pygad.GA(num_generations = num_generations,
                 num_parents_mating = num_parents_mating,
                 fitness_func = fitness_func,
                 sol_per_pop = sol_per_pop,
                 num_genes = num_genes,
                 gene_type = gene_type,
                 init_range_low = init_range_low,
                 init_range_high = init_range_high,
                 stop_criteria = stop_criteria
        )
        ga.run()
        ga.plot_fitness()
        best_solution, best_fitness, best_idx = ga.best_solution()
        print(best_solution, " - ", 1/best_fitness)


