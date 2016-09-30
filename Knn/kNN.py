from distances.distances import euclidean_distance, cosine_distance
from collections import Counter


def knn(datalist, testlist, k, distance=0):
    right = 0
    wrong = 0
    count = 0
    print("Testing "+str(len(testlist))+" vulnerabilities")
    for v in testlist:
        distance_list = []
        for w in datalist:
            distance_list.append((cosine_distance(v.vector, w.vector),w.group))
        distance_list.sort(key=lambda tup:tup[0])
        distance_list = distance_list[:k]
        counter = Counter(d[1] for d in distance_list)
        pred_group = counter.most_common(1)[0][0]
        if pred_group == v.group:
            right = right + 1
        else:
            wrong = wrong + 1
        count = count+1
        print("Tested "+str(count)+" of "+str(len(testlist)))
    print("Total of mistakes: "+str(wrong))
    print("Total of successes: "+str(right))
    print("Percentage of success: "+str(100*right/(right+wrong))+"%")