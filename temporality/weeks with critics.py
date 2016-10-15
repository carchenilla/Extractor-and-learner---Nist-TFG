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

    for v in vulnerability_list:
        for s in v.soft_list:
            print(s.name)


    program = "iphone_os"

    specific_list = []
    c2 = 0
    for v in vulnerability_list:
        if checkSoft(program, v) and v.score >= 9:
            c2 = c2 +1
            specific_list.append((v.published, v.score))
    specific_list.sort(key=lambda tup: tup[0])
    print("Found: "+str(c2))

    begin_date = specific_list[0][0]
    finish_date = specific_list[-1][0]
    weeks_list = []

    for c in range(1,45):
        week_counter = 0
        for week in daterange(begin_date, finish_date):
            vuln_counter = 0
            for tup in specific_list:
                if (week[0] <= tup[0] <= week[1]):
                    vuln_counter = vuln_counter + 1
            if vuln_counter == c:
                week_counter = week_counter + 1
        weeks_list.append(week_counter)

    plt.bar(range(1,45), weeks_list)
    plt.ylabel("Nº de semanas")
    plt.xlabel("Nº de vulnerabilidades criticas aparecidas en la semana")
    plt.title(program)
    plt.show()