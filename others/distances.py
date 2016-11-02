from numpy import linalg,dot, sqrt, sum, power
from copy import deepcopy

def cosine_distance(v, w):
    x = deepcopy(v)
    y = deepcopy(w)
    if len(v)==9 and len(w)==9:
        for i in range(3,9):
            if v[i]!=w[i]:
                x[i] = 1
                y[i] = 2
            else:
                x[i] = 1
                y[i] = 1
    print(linalg.norm(x)*linalg.norm(y))
    return 1-(dot(x,y)/(linalg.norm(x)*linalg.norm(y)))



def euclidean_distance(v,w):
    return sqrt(sum(power(v-w,2)))