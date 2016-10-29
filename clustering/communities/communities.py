from numpy import float32
from scipy.sparse import lil_matrix
from networkx import from_numpy_matrix


def generate_sparse_graph(datalist, threshold):
    x = [v.vector for v in datalist]

    m = lil_matrix((len(x), len(x)), dtype=float32)

    for i in range(len(x)):
        for j in range(i, len(x)):
            aux = sum(x[i]==x[j])
            if aux >= threshold:
                m[i, j] = aux
        print(str(i) + " of " + str(len(x)))

    print("\n Now mirroring matrix \n")

    for i in range(1, len(x)):
        for j in range(i):
            m[i,j] = m[j,i]
        print(str(i)+" of "+str(len(x)))

    return m