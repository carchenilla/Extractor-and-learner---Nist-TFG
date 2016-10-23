from sklearn.cluster import DBSCAN
from pickle import dump
import matplotlib.pyplot as plt
from distances.distances import cosine_distance
from numpy import array, float32, zeros


def run_dbscan(datalist, eps=0.022, min_pts=2686):
    #BEST EPSILON = 0.022
    #BEST MIN_PTS = 2686
    x = [v.vector for v in datalist]
    print("Creating distance matrix using cosine distance")
    z = create_distance_matrix(x, eps)
    print("Matrix created. Now training DBSCAN...")
    try:
        step = z.shape[0]//4
        rows = [min(n, z.shape[0]) for n in range(step, z.shape[0], step)]

        for r in range(len(rows)-1):
            with open("matrix/rows_" + str(rows[r]) + ".p",'wb') as f:
                dump(z[rows[r]-step:rows[r],:], f)

        with open("matrix/rows_" + str(rows[-1]) + ".p", 'wb') as f:
            dump(z[rows[-2]:rows[-1]+1, :], f)

    except IOError as err:
        print(str(err))

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
        print(str(i)+" of "+str(len(datalist)))

    print("\n Now mirroring matrix \n")

    for i in range(1, len(datalist)):
        for j in range(i):
            m[i,j] = m[j,i]
        print(str(i)+" of "+str(len(datalist)))

    return m






def find_neighbors_at_distance(datalist, distance):
    print("Finding neighbors of each vulnerability at max distance "+str(distance))
    step = int(len(datalist)/16)+1
    final_list = [0]*16
    current = 0
    for v in datalist:
        counter = 0
        for v2 in datalist:
            if cosine_distance(v,v2)<=distance:
                counter += 1
        final_list[counter//step] += 1
        current += 1
        print(str(current)+" of "+str(len(datalist)))

    xaxis = [min(n, len(datalist)) for n in range(0, len(datalist), step)]
    print(str(step))
    print(xaxis)
    print(final_list)


def find_distance_of_nearest_neighbor(datalist):
    final_list = []
    for v in datalist:
        distances = []
        for v2 in datalist:
            if not ((v==v2).all()):
                distances.append(cosine_distance(v,v2))
        final_list.append(min(distances))
        print(str(len(final_list))+ " of " +str(len(datalist)))

    plt.plot(range(len(final_list)), final_list)
    plt.xlabel("Vulnerabilidades")
    plt.ylabel("Distancia al vecino más cercano")
    plt.show()