from sklearn import svm

def run_svm(datalist, testlist, kernel=None, gamma = 0.125, deg = 1, r = 0):
    X = [x.vector for x in datalist]
    Y = [x.group for x in datalist]
    true = []
    predicted = []
    if kernel != None:
        clf = svm.SVC(kernel=kernel, gamma=gamma, degree=deg, coef0=r)
        s = str(kernel)+" kernel with gamma = "+str(gamma)+", degree = "+str(deg)+", coef0 = "+str(r)
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
        true.append(v.group)
        predicted.append(res[0])

    if not -1 in true:
        print("Ratio of success: "+str(right/(right+fail)))
    classes = list(range(min(true), max(true)+1))

    return (classes, true, predicted)