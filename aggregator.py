import json

import filenames
import csv
import sys

def list_to_csv(header, mylist, filename):
    with open(filename, "w") as f:
        csv_writer = csv.writer(f, lineterminator='\n')
        csv_writer.writerow(header)
        csv_writer.writerows(mylist)

def getpredictions():
    with open(filenames.predictions, "r") as f:
        return list(map(lambda x: x.strip().split(',')[1], f.readlines()))
        

def adversary_by_percents():
    header = ['index', 'BasePred', 'Pred']
    percent5 = []
    percent10 = []
    percent20 = []
    predictions = getpredictions()
    for i in range(200):
        with open(filenames.dir_results + "adversary_genetic_500gen{}.csv".format(i), "r") as f:
            percent5.append([i, predictions[i], f.readline().strip().split(",")[-1]])
            percent10.append([i, predictions[i], f.readline().strip().split(",")[-1]])
            percent20.append([i, predictions[i], f.readline().strip().split(",")[-1]])
    list_to_csv(header, percent5, filenames.dir_results + "aggregated/adversary_percent5.csv")
    list_to_csv(header, percent10, filenames.dir_results + "aggregated/adversary_percent10.csv")
    list_to_csv(header, percent20, filenames.dir_results + "aggregated/adversary_percent20.csv")

def adversary_by_idx():
    header = ['index', 'BasePred', '5%', '10%', '20%']
    mylist = []
    predictions = getpredictions()
    for i in range(200):
        with open(filenames.dir_results + "adversary_genetic_500gen{}.csv".format(i), "r") as f:
            mylist.append([i, predictions[i], f.readline().strip().split(",")[-1], f.readline().strip().split(",")[-1], f.readline().strip().split(",")[-1]])
    list_to_csv(header, mylist, filenames.dir_results + "aggregated/adversary_by_idx.csv")

def iterative_by_benignnumber():
    predictions = getpredictions()
    # indices = getindices()
    header_acc = ["index", "5%", "10%", "20%", "50%", "100%"]
    header_pred = ["index", "BasePred", "5%", "10%", "20%", "50%", "100%"]
    for benignnumber in range(10, 101, 10):
        preds = []
        accs = []
        for i in range(200):
        # for i in indices:
             with open(filenames.dir_results + "iterative_idx-{}_benignnumber-{}_percent-5-10-20-50-100.csv".format(i, benignnumber), "r") as f:
                lines = f.readlines()   
                accs.append([i] + list(map(lambda x: x.strip().split(",")[1], lines)))
                preds.append([i, predictions[i]] + list(map(lambda x: x.strip().split(",")[2], lines)))
        list_to_csv(header_acc, accs, filenames.dir_results + "aggregated/iterative_by_benignnumber{}_accs.csv".format(benignnumber))
        list_to_csv(header_pred, preds, filenames.dir_results + "aggregated/iterative_by_benignnumber{}_preds.csv".format(benignnumber))

def iterative_by_percent():
    predictions = getpredictions()
    # indices = getindices()
    percents = [5, 10, 20, 50, 100]
    header_acc = ["index", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
    header_pred = ["index", "BasePred", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
    for percenti in range(5):
        accs = []
        preds = []
        for i in range(200):
        # for i in indices:
            acc = []
            pred = []
            for benignnumber in range(10, 101, 10):
                with open(filenames.dir_results + "iterative_idx-{}_benignnumber-{}_percent-5-10-20-50-100.csv".format(i, benignnumber), "r") as f:
                    lines = f.readlines()
                    acc.append(lines[percenti].strip().split(',')[1])
                    pred.append(lines[percenti].strip().split(',')[2])
            accs.append([i] + acc)
            preds.append([i, predictions[i]] + pred)
        list_to_csv(header_acc, accs, filenames.dir_results + "aggregated/iterative_by_percent{}_accs.csv".format(percents[percenti]))
        list_to_csv(header_pred, preds, filenames.dir_results + "aggregated/iterative_by_percent{}_preds.csv".format(percents[percenti]))

def getindices():
    with open("random\\random", "r") as f:
        return list(map(lambda x: int(x), f.readline().strip().split(" ")))

def genetic_by_benignnumber():
    predictions = getpredictions()
    indices = getindices()
    header_acc = ["index", "5%", "10%", "20%"]
    header_pred = ["index", "BasePred", "5%", "10%", "20%"]
    for benignnumber in [20, 30, 40, 50]:
        preds = []
        accs = []
        for i in indices:
            try:
                with open(filenames.dir_results + "genetic_idx-{}_bening-{}_percent-5-10-20.csv".format(i, benignnumber), "r") as f:
                    lines = f.readlines()
                    accs.append([i] + list(map(lambda x: x.strip().split(",")[1], lines)))
                    preds.append([i, predictions[i]] + list(map(lambda x: x.strip().split(",")[2], lines)))
            except:
                pass

        list_to_csv(header_acc, accs, filenames.dir_results + "aggregated/genetic_by_benignnumber{}_accs.csv".format(benignnumber))
        list_to_csv(header_pred, preds, filenames.dir_results + "aggregated/genetic_by_benignnumber{}_preds.csv".format(benignnumber))

def genetic_by_percent():
    predictions = getpredictions()
    indices = getindices()
    header_acc = ["index", "20", "30", "40", "50"]
    header_pred = ["index", "BasePred", "20", "30", "40", "50"]
    for percenti, percent in enumerate([5, 10, 20]):
        accs = []
        preds = []
        for i in indices:
            acc = []
            pred = []
            try:
                for benignnumber in [20, 30, 40, 50]:

                    with open(filenames.dir_results + "genetic_idx-{}_bening-{}_percent-5-10-20.csv".format(i, benignnumber), "r") as f:
                        lines = f.readlines()
                        acc.append(lines[percenti].strip().split(',')[1])
                        pred.append(lines[percenti].strip().split(',')[2])
                accs.append([i] + acc)
                preds.append([i, predictions[i]] + pred)
            except:
                pass
        list_to_csv(header_acc, accs, filenames.dir_results + "aggregated/genetic_by_percent{}_accs.csv".format(percent))
        list_to_csv(header_pred, preds, filenames.dir_results + "aggregated/genetic_by_percent{}_preds.csv".format(percent))



if __name__ == '__main__':
    globals()[sys.argv[1]]()