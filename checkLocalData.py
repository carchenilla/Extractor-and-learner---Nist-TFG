import pickle
from pca import pca
from k_means import elbowCheck, kmeans

from extractor.VulnDictionary import VulnDictionary

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
        if d.update()==1:
            with open("dictionaries/VulnDictionary_" + str(d.year) + ".p", 'wb') as f:
                pickle.dump(d,f)
        count = count + len(d.dict.keys())
        vulnerability_list.extend(d.dict.values())
    print("Total: "+str(count))

    my_list = pca.pca(vulnerability_list, threshold=0.90)
    elbowCheck.elbow_check(my_list,9) #check between 1-8 clusters
    '''(cost, assig) = kmeans.best_cost_kmeans(vulnerability_list, k=3)
    print("Finised.")
    print(str(cost))
    print(str(assig))'''

    '''(cost, assig_list) = kmeans.best_cost_kmeans(my_list,k=3)
    print(cost)
    print(assig_list)'''