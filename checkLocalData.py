import pickle
from random import sample
from Knn.kNN import run_knn
from pca.pca import pca
from svm import svm
import matplotlib.pyplot as plt
from k_means import elbowCheck, kmeans
from svm.svm import run_svm
from hierarchical.hierarchical import run_hierarchical

from data_types.VulnDictionary import VulnDictionary


if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
    test_list = []
    for i in range(2002, 2017):
        try:
            with open("dictionaries/VulnDictionary_"+str(i)+".p", 'rb') as f:
                dictionary_list.append(pickle.load(f))
        except IOError as err:
            print("Error with dictionary "+str(i)+" - "+str(err))
            print("Creating dictionary from scratch")
            dictionary_list.append(VulnDictionary(i).update())
    print()

    for d in dictionary_list:
        #d.update()
        if d.year > 2008:
            count = count + len(d.dict.keys())
            vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(len(vulnerability_list)))

    positions = sample(range(len(vulnerability_list)), int(0.15*(len(vulnerability_list))))

    train_list = []
    test_list = []
    for i in range(len(vulnerability_list)):
        if i in positions:
            test_list.append(vulnerability_list[i])
        else:
            train_list.append(vulnerability_list[i])

    '''print("Beginning ML training of data from 2009 - 2016")
    asig = run_hierarchical(pca(vulnerability_list, threshold=0.95))
    print("Finished hierarchical cluster. Saving data to dictionaries and disk")

    for x in asig:
        found = False
        i = 0
        while ((not found) and (i <= len(dictionary_list))):
            d = dictionary_list[i]
            v = d.dict.get(x[0])
            if v != None:
                v.group = x[1]
                found = True
            i = i + 1

    run_svm(train_list, test_list, "rbf")

    for d in dictionary_list:
        try:
            with open("dictionaries/VulnDictionary_"+str(d.year)+".p", 'wb') as f:
                pickle.dump(d,f)
        except IOError as err:
            print("Error with dictionary "+str(d.year)+" - "+str(err))'''