import pickle
import datetime
from VulnDictionary import VulnDictionary

if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
    for i in range(2002, 2017):
        try:
            with open("VulnDictionary_"+str(i)+".p", 'rb') as f:
                dictionary_list.append(pickle.load(f))
        except IOError as err:
            print("Error with dictionary "+str(i)+" - "+str(err))
            print("Creating dictionary from scratch")
            dictionary_list.append(VulnDictionary(i))
    print()
    for d in dictionary_list:
        if d.update()==1:
            with open("VulnDictionary_" + str(d.year) + ".p", 'wb') as f:
                pickle.dump(d,f)
        count = count + len(d.dict.keys())
        vulnerability_list.extend(d.dict.values())
    print("Total: "+str(count))
    '''print(str(len(vulnerability_list)))
    print(vulnerability_list[-2].to_string())'''
    for v in vulnerability_list:
        if v.published <= datetime.date(1999,2,2):
            print(v.to_string())