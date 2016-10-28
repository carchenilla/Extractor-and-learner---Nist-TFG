from random import sample
from numpy import array, float32
from data_types.Vulnerabilty import Vulnerability
from distances.distances import cosine_distance
import datetime


def kmeans(datalist, times=6, k=4):
    print("Generating centroids")
    centroids = generateCentroids(k, datalist)
    assignation_list = [(-1,-1)]*len(datalist)
    print("Centroids selected. Commencing...")
    for it in range(times):
        print("Iteration no. "+str(it+1))
        for i in range(len(datalist)):
            assignation_list[i] = (datalist[i].name, getCentroid(datalist[i],centroids))
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
        counter = counter + cosine_distance(datalist[i].vector, centroids[assignation_list[i][1]].vector)
    return counter/len(datalist)


def relocate_centroid(datalist, assignation_list, k):
    n_centr = array([0]*len(datalist[0].vector), dtype=float32)
    count = 0
    for i in range(len(assignation_list)):
        if assignation_list[i][1]==k:
            n_centr = n_centr + datalist[i].vector
            count = count+1
    if count==0:
        return None
    new_v1 = n_centr/count
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
        distances.append(cosine_distance(c.vector,vuln.vector))
    return distances.index(min(distances))


def run_kmeans(datalist, iterations=100, times=6, k=4):
    lowest_cost = 1000
    final_assig = None
    for i in range(iterations):
        print("\nInitializing k-means no. "+str(i+1))
        (assig_list, cost) = kmeans(datalist, times, k)
        if cost < lowest_cost:
            print("Lower cost found: "+str(cost))
            lowest_cost = cost
            final_assig = assig_list
    return (lowest_cost, final_assig)