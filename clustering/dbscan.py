from numpy import float32, zeros, amin, array
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from others.distances import cosine_distance
import multiprocessing

def run_dbscan(datalist, eps=0.004, min_pts=2692):
    #BEST EPSILON = 0.004
    #BEST MIN_PTS = 2692
    x = [v.vector for v in datalist]

    print("Creating distance matrix using cosine distance")
    z = create_distance_matrix(x, eps)
    print("Matrix created. Now training DBSCAN...")

    labels = DBSCAN(eps=eps, min_samples=min_pts, metric='precomputed').fit_predict(z)

    print("\n")
    print(str(len(datalist)))
    print(str(len(labels)))
    final_list = []

    for i in range(len(datalist)):
        final_list.append((datalist[i].name, labels[i]))

    return final_list


def create_distance_matrix(datalist, eps):
    m = zeros((len(datalist), len(datalist)), dtype=float32)
    for i in range(len(datalist)):
        for j in range(i, len(datalist)):
            m[i,j] = cosine_distance(datalist[i], datalist[j])
        print(str(i+1)+" of "+str(len(datalist)))

    print("\n Now mirroring matrix \n")

    for i in range(1, len(datalist)):
        for j in range(i):
            m[i,j] = m[j,i]
        print(str(i)+" of "+str(len(datalist)-1))

    return m






def find_neighbors_at_distance(name, small_list, datalist, distance):
    print("Finding neighbors of each vulnerability at max distance "+str(distance))
    step = int(len(datalist)/16)+1
    final_list = [0]*16
    current = 0
    for v in small_list:
        counter = 0
        for v2 in datalist:
            if cosine_distance(v,v2)<=distance:
                counter += 1
        final_list[counter//step] += 1
        current += 1
        print(str(current)+" of "+str(len(small_list)))

    with open("results-"+str(name)+".p", 'wb') as f:
        pickle.dump(final_list,f)



def find_distance_of_nearest_neighbor(name, small_list, datalist):
    final_list = []
    counter = 0
    for v in small_list:
        distances = []
        for v2 in datalist:
            if not ((v==v2).all()):
                distances.append(cosine_distance(v,v2))
        min_v = amin(distances)
        print(min_v)
        final_list.append(min_v)
        counter += 1
        print(str(counter)+ " of " +str(len(small_list)))

    with open("results-"+str(name)+".p", 'wb') as f:
        pickle.dump(final_list,f)



def by_half(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]




import pickle

if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
    test_list = []
    for i in range(2002, 2017):
        with open("../dictionaries/VulnDictionary_"+str(i)+".p", 'rb') as f:
            dictionary_list.append(pickle.load(f))
    print()

    for d in dictionary_list:
        if d.year > 2008:
            count = count + len(d.dict.keys())
            vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(len(vulnerability_list)))

    x = [v.vector for v in vulnerability_list]

    aux1, aux2 = by_half(x)
    list1, list2 = by_half(aux1)
    list3, list4 = by_half(aux2)
    lists = [list1, list2, list3, list4]
    procs = []

    for i in range(4):
        procs.append(multiprocessing.Process(target=find_neighbors_at_distance, args=(str(i), lists[i], x, 0.004)))

    for p in procs:
        p.start()

    for i in range(len(procs)):
        procs[i].join()