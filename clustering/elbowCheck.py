import matplotlib.pyplot as plt
from clustering import kmeans


def elbow_check(datalist, krange):
    cost_list = []
    asig_list = []
    for k in range(1, krange):
        print("\nChecking cost for k="+str(k))
        (cost, asig) = kmeans.best_cost_kmeans(datalist, k=k)
        cost_list.append(cost)
        asig_list.append(asig)
    print("All iterations completed. Now plotting")
    #K = cost_list.index(min(cost_list))
    #final_assig = asig_list[K]
    #print("Best K for this data is: "+str(K)+"\n")
    plt.plot(range(1,krange), cost_list)
    plt.show()
    ''' for k in range(K):
        with open("Cluster no. " + str(k + 1) + ".txt", 'w') as f:
            for i in range(len(final_assig)):
                if final_assig[i] == k:
                    f.write(str(datalist[i].vector) + "\n")'''