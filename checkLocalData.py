import pickle
from Knn import kNN
from pca import pca
import matplotlib.pyplot as plt
from k_means import elbowCheck, kmeans
from data_types.VulnDictionary import VulnDictionary


if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
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
        d.update()
        count = count + len(d.dict.keys())
        vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(count))

    #(cost, assig) = kmeans.best_cost_kmeans(vulnerability_list, times=7, k=4)

    print("Finished K-means. Saving data to dictionaries and disk")
    '''for x in assig:
        for d in dictionary_list:
            v = d.dict.get(x[0])
            if v != None:
                v.group = x[1]

    for d in dictionary_list:
        try:
            with open("dictionaries/VulnDictionary_"+str(d.year)+".p", 'wb') as f:
                pickle.dump(d,f)
        except IOError as err:
            print("Error with dictionary "+str(d.year)+" - "+str(err))'''

    print("Done. Now validating results with Knn for 2016")

    k_list = range(1,11)
    results_list = []

    train_data = []
    test_data = []

    for d in dictionary_list:
        if d.year < 2016:
            train_data.extend(list(d.dict.values()))
        else:
            test_data.extend(list(d.dict.values()))

    for i in k_list:
        results_list.append(kNN.knn(train_data, test_data, i))

    plt.plot(k_list, test_data)
    plt.show()