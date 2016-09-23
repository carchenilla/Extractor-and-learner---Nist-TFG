from k_means import kmeans
import matplotlib.pyplot as plt


def elbow_check(datalist, krange):
    cost_list = []
    asig_list = []
    for k in range(1, krange):
        print("\nChecking cost for k="+str(k))
        (cost, asig) = best_cost_kmeans(datalist, k)
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



def best_cost_kmeans(datalist, k):
    lowest_cost = 1000
    final_assig = None
    for i in range(100):
        print("\nInitializing k-means no. "+str(i+1))
        (assig_list, cost) = kmeans.kmeans(k, datalist, 5)
        if cost < lowest_cost:
            print("Lower cost found: "+str(cost))
            lowest_cost = cost
            final_assig = assig_list
    return (lowest_cost, final_assig)