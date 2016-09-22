import datetime
import pickle
from k_means import kmeans

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

    lowest_cost = 1000
    final_assig = None
    for i in range(100):
        print("\nInitializing k-means no. "+str(i+1))
        (assig_list, cost) = kmeans.kmeans(3, vulnerability_list, 5)
        if cost < lowest_cost:
            print("Lower cost found: "+str(cost))
            lowest_cost = cost
            final_assig = assig_list
    for k in range(3):
        with open("Cluster no. "+ str(k+1) + ".txt", 'w') as f:
            for i in range(len(final_assig)):
                if final_assig[i]==k:
                    f.write(str(vulnerability_list[i].vector)+"\n")