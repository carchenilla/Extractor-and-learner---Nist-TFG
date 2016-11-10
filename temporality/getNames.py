from datetime import date, timedelta
import pickle
from data_types.VulnDictionary import VulnDictionary
import matplotlib.pyplot as plt


def checkSoft(soft, v):
    found = False
    for s in v.soft_list:
        if str(soft) in str(s.name):
            found = True
    return found


def daterange(start_date, end_date):
    for n in range(int (((end_date - start_date).days)/7)):
        yield (start_date + timedelta((n-1)*7), start_date + timedelta(n*7))

def load_vulnerabilities():
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
    return vulnerability_list

if __name__ == "__main__":

    vulnerability_list = load_vulnerabilities()

    program = "windows_10"


    specific_list = []
    c2 = 0
    for v in vulnerability_list:
        if checkSoft(program, v):
            c2 = c2 +1
            specific_list.append((v.published, v))
    specific_list.sort(key=lambda tup: tup[0])
    print("Found: "+str(c2))

    begin_date = date(2016,8,1)
    finish_date = date(2016,10,1)

    for v in specific_list:
        if begin_date <= v[0] <= finish_date:
            print(v[1].to_string()+"\n")