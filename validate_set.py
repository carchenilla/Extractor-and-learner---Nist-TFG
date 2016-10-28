import pickle, time
from random import sample
from kNN.kNN import run_knn
from numpy import mean, array
from svm.svm import run_svm
from data_types.VulnDictionary import VulnDictionary



if __name__ == "__main__":
    count = 0
    dictionary_list = []
    vulnerability_list = []
    test_list = []
    for i in range(2002, 2017):
        try:
            with open("dictionaries/VulnDictionary_"+str(i)+".p", 'rb') as f:
                dictionary_list.append(pickle.load(f))
        except IOError as err:
            print("Error with dictionary "+str(i)+" - "+str(err))
            print("Creating dictionary from scratch")
            dictionary_list.append(VulnDictionary(i).update())
    print()

    for d in dictionary_list:
        if d.year > 2008:
            count = count + len(d.dict.keys())
            vulnerability_list.extend(list(d.dict.values()))
    print("Total: "+str(len(vulnerability_list)))


    results_list = []

    for x in range(10):
        positions = sample(range(len(vulnerability_list)), int(0.2*(len(vulnerability_list))))

        train_list = []
        test_list = []
        for i in range(len(vulnerability_list)):
            if ((i in positions) and (vulnerability_list[i].group!=-1)):
                test_list.append(vulnerability_list[i])
            elif ((not (i in positions)) and (vulnerability_list[i].group!=-1)):
                train_list.append(vulnerability_list[i])


        print("Beginning validation")
        print("Training set: "+str(len(train_list)))
        print("Validation set: "+str(len(test_list)))

        start_time = time.time()
        results_list.append(run_svm(train_list,test_list,'rbf',0.125))
        end_time = time.time()

    print("--- %s seconds ---" % (end_time - start_time))
    print(results_list)
    print(mean(array(results_list)))
