from numpy import array, float32, power, transpose, linalg


def pca(datalist, d=None, threshold = 0.99):
    normalized_list = normalize(datalist)
    sigma = getSigma(normalized_list)
    U, s, V = linalg.svd(sigma, full_matrices=True)
    if d==None:
        print("Calculating optimal reduction for "+str(threshold)+" variance retention")
        d = variance_retention(threshold, s)
        print("Optimal d = "+str(d))
    print("Now reducing dimensionality to "+str(d))
    new_U = transpose(U[:,:d])
    for v in normalized_list:
        x = transpose(v.vector)
        v.vector = transpose(new_U.dot(x))
    print("Done")
    #print(normalized_list[14351].vector)




def normalize(datalist):
    print("Normalizing vectors")
    aux_list = array([0]*len(datalist[0].vector), dtype=float32)
    for v in datalist:
        aux_list = aux_list + v.vector
    mean_vector = aux_list/len(datalist)
    print("Mean calculated")
    aux_list = array([0]*len(datalist[0].vector), dtype=float32)
    for i in range(len(datalist)):
        aux_list = aux_list + power(datalist[i].vector - mean_vector, 2)
    sd_vector = aux_list/(len(datalist)-1)
    print("Standard deviation calculated")
    norm_vuln_list = []
    for i in range(len(datalist)):
        norm_vuln_list.append(datalist[i])
        norm_vuln_list[-1].vector = (datalist[i].vector - mean_vector)/sd_vector
    print("Vectors normalized")
    return norm_vuln_list


def getSigma(datalist):
    vl = []
    print("Calculating sigma matrix")
    for v in datalist:
        vl.append(v.vector)
    aux_matrix = array(vl)
    sigma = (1/len(datalist))*transpose(aux_matrix).dot(aux_matrix)
    print("Sigma matrix calculated")
    return sigma


def variance_retention(threshold, S):
    total = sum(S)
    for i in range(len(S)):
        count = sum(S[:(i+1)])
        value = count/total
        if value >= threshold:
            return i+1
    return len(S)