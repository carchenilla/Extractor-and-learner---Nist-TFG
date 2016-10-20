from sklearn import svm

def run_svm(datalist, testlist, kernel=None, gamma = 0.125):
    X = [x.vector for x in datalist]
    Y = [x.group for x in datalist]

    if kernel != None:
        clf = svm.SVC(kernel=kernel, gamma=gamma)
        s = str(kernel)+" kernel with gamma = "+str(gamma)+"."
    else:
        clf = svm.SVC(kernel='linear')
        s = "linear kernel."

    print("Training SVM using "+s)
    clf.fit(X,Y)

    print("Done. Now testing data")
    right = 0
    fail = 0

    for v in testlist:
        res = clf.predict(v.vector.reshape(1,-1))
        if res[0] == v.group:
            right = right + 1
        else:
            fail = fail + 1

    print("Ratio of success: "+str(right/(right+fail)))