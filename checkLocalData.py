import pickle
from Knn import kNN
from pca import pca
from svm import svm
import matplotlib.pyplot as plt
from k_means import elbowCheck, kmeans
from svm import svm

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
            dictionary_list.append(VulnDictionary(i))
    print()
    for d in dictionary_list:
        #d.update()
        count = count + len(d.dict.keys())
        if d.year < 2016:
            vulnerability_list.extend(list(d.dict.values()))
        else:
            test_list.extend(list(d.dict.values()))
    print("Total: "+str(count))


    svm.run_svm(vulnerability_list, test_list, kernel="rbf", gamma=0.125)

    '''(cost, assig) = kmeans.best_cost_kmeans(vulnerability_list, times=7, k=4)

    print("Finished K-means. Saving data to dictionaries and disk")
    for x in assig:
        for d in dictionary_list:
            v = d.dict.get(x[0])
            if v != None:
                v.group = x[1]

    for d in dictionary_list:
        try:
            with open("dictionaries/VulnDictionary_"+str(d.year)+".p", 'wb') as f:
                pickle.dump(d,f)
        except IOError as err:
            print("Error with dictionary "+str(d.year)+" - "+str(err))


    print("Done. Now validating results with Knn for 2016")'''