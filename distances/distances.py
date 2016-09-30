from numpy import linalg,dot, sqrt, sum, power

def cosine_distance(v, w):
    return 1-dot(v,w)/(linalg.norm(v)*linalg.norm(w))


def euclidean_distance(v,w):
    return sqrt(sum(power(v-w,2)))