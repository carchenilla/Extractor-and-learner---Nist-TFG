from collections import Counter
from others.distances import cosine_distance


def run_knn(datalist, testlist, k):
    right = 0
    wrong = 0
    count = 0
    true = []
    predicted = []
    print("Testing "+str(len(testlist))+" vulnerabilities")
    for v in testlist:
        distance_list = []
        for w in datalist:
            distance_list.append((cosine_distance(v.vector, w.vector),w.group))
        distance_list.sort(key=lambda tup:tup[0])
        distance_list = distance_list[:k]
        counter = Counter(d[1] for d in distance_list)
        predicted.append(counter.most_common(1)[0][0])
        true.append(v.group)
        if predicted[-1] == true[-1]:
            right += 1
        else:
            wrong += 1
        count += 1
        print("Tested "+str(count)+" of "+str(len(testlist)))
    if not -1 in true:
        print("Total of mistakes: "+str(wrong))
        print("Total of successes: "+str(right))
        print("Percentage of success: "+str(right/(right+wrong)))

    classes = list(range(min(true), max(true)+1))

    return (classes, true, predicted)