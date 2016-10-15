import datetime
import pickle
import matplotlib.pyplot as plt
from data_types.VulnDictionary import VulnDictionary


def checkSoft(soft, v):
    found = False
    for s in v.soft_list:
        if str(soft) in str(s.name):
            found = True
    return found


if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
    for i in range(2002, 2017):
        try:
            with open("../dictionaries/VulnDictionary_"+str(i)+".p", 'rb') as f:
                dictionary_list.append(pickle.load(f))
        except IOError as err:
            print("Error with dictionary "+str(i)+" - "+str(err))
    print()
    for d in dictionary_list:
        count = count + len(d.dict.keys())
        vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(count))

    my_list = []

    program = "iphone_os"

    c2 = 0
    for v in vulnerability_list:
        if checkSoft(program, v) and v.score >= 9 :
            c2 = c2 +1
            my_list.append((v.published, v.score))
    my_list.sort(key=lambda tup: tup[0])
    print(str(c2))
    plt.plot(list(x[0] for x in my_list), list(x[1] for x in my_list))
    plt.show()