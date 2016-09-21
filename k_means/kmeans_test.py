from random import sample
from numpy import array, dot, linalg, append, round
import math

datalist = [0]*78000

k = 5


centroids = sample(range(len(datalist)),k)

print(centroids)

x = [11.00005,2.2,2.98, 6.85, 7.657]
y= [7,8,9, 10, 11]

print(x)

xn = array(x)
yn = array(y)

print(dot(xn,yn))
print(linalg.norm(xn))
print(linalg.norm(yn))

cos = dot(xn,yn)/(linalg.norm(xn)*linalg.norm(yn))
print(1-cos)
print("operacion")
print(math.pow(1-cos,2))


suma = xn+yn

print(xn/2)
print((xn/2)[2:len(xn)])
print("xc")
print(append(xn[:2], round(xn[2:len(xn)])))