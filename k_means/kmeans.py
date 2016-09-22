from random import sample
from numpy import array, dot, linalg, append, round
from extractor.Vulnerabilty import Vulnerability
import datetime

def kmeans(k, datalist, iterations):
    print("Generating centroids")
    centroids = generateCentroids(k, datalist)
    assignation_list = [-1]*len(datalist)
    print("Centroids selected. Commencing...")
    for it in range(iterations):
        print("Iteration no. "+str(it))
        for i in range(len(datalist)):
            assignation_list[i] = getCentroid(datalist[i],centroids)
        for i in range(k):
            nc = relocate_centroid(datalist, assignation_list, i)
            if nc != None:
                centroids[i] = nc
    print("All iterations finished. Calculating distortion")
    cost = calculate_distortion(datalist, assignation_list, centroids)
    print("K-means finished")
    return (assignation_list, cost)


def calculate_distortion(datalist, assignation_list, centroids):
    counter = 0
    for i in range(len(datalist)):
        counter = counter + distance(datalist[i], centroids[assignation_list[i]])
    return counter/len(datalist)


def relocate_centroid(datalist, assignation_list, k):
    n_centr = array([0]*10)
    count = 0
    for i in range(len(assignation_list)):
        if assignation_list[i]==k:
            n_centr = n_centr + datalist[i].vector
            count = count+1
    if count==0:
        return None
    new_v1 = n_centr/count
    #new_v1 = append(aux[:3],round(aux)[3:len(aux)])
    new_centroid = Vulnerability("Custom Vulnerability no. "+str(k), datetime.date(2000,1,1), datetime.date(2000,1,1),
                                 new_v1[0], new_v1, "No description", "No soft list")
    return new_centroid


def generateCentroids(k, datalist):
    positions = sample(range(len(datalist)),k)
    centroids = []
    for p in positions:
        centroids.append(datalist[p])
    return centroids


def getCentroid(vuln, centroids):
    distances = []
    for c in centroids:
        distances.append(distance(c,vuln))
    return distances.index(min(distances))


def distance(v1, v2):
    v = array(v1.vector)
    w = array(v2.vector)
    cos = dot(v,w)/(linalg.norm(v)*linalg.norm(w))
    return 1-cos