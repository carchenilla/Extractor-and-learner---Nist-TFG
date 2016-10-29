import pickle
import time
from clustering.hierarchical import  run_hierarchical
from data_types.VulnDictionary import VulnDictionary
from others.pca import pca

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
        if d.year > 2008:
            count = count + len(d.dict.keys())
            vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(len(vulnerability_list)))

    start_time = time.time()
    asig = run_hierarchical(pca(vulnerability_list,d=5))
    end_time = time.time()

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

    for d in dictionary_list:
        try:
            with open("dictionaries/VulnDictionary_" + str(d.year) + ".p", 'wb') as f:
                pickle.dump(d, f)
        except IOError as err:
            print("Error with dictionary " + str(d.year) + " - " + str(err))

    print("--- %s seconds ---" % (end_time - start_time))