import datetime
import pickle
from Knn import kNN
from pca import pca
import matplotlib.pyplot as plt
from k_means import elbowCheck, kmeans
from data_types.VulnDictionary import VulnDictionary


def checkSoft(soft, v):
    for s in v.soft_list:
        if str(s.name).find("Windows"):
            return True
    return False


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
        count = count + len(d.dict.keys())
        vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(count))

    my_list = []

    c = 0
    c2 = 0
    for v in vulnerability_list:
        c = c+1
        if checkSoft("Windows", v) and v.published >= datetime.date(2016,1,1) and v.published <= datetime.date(2016,2,1) and v.score > 9 :
            c2 = c2 +1
            my_list.append((v.published, v.score))
    my_list.sort(key=lambda tup: tup[0])
    print(str(c2))
    print(str(c))
    plt.plot(list(x[0] for x in my_list), list(x[1] for x in my_list))
    plt.show()