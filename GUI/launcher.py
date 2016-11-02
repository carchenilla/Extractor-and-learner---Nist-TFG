from GUI.application_GUI import *
from random import sample
from clustering.kmeans import run_kmeans
from clustering.hierarchical import run_hierarchical
from clustering.dbscan import run_dbscan
from validating.kNN import run_knn
from validating.svm import run_svm
from others.pca import pca
from others.loadAndSave import *
import sys, threading, pickle

yearsList = []
threadLock = threading.Lock()

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass




class MyThread(threading.Thread):
    def __init__(self, algo, params):
        threading.Thread.__init__(self)
        self.algo = algo
        self.params = params

    def run(self):
        need_to_save = False
        datalist = self.params[0]
        if self.algo=='kmeans':
            threadLock.acquire()
            (cost, asig) = run_kmeans(datalist, self.params[1], self.params[2], self.params[3])
            need_to_save = True
            threadLock.release()
        elif self.algo=='hierarch':
            threadLock.acquire()
            asig = run_hierarchical(datalist, self.params[1], self.params[2])
            need_to_save = True
            threadLock.release()
        elif self.algo=='dbscan':
            threadLock.acquire()
            asig = run_dbscan(datalist, self.params[1], self.params[2])
            need_to_save = True
            threadLock.release()
        elif self.algo=='knn':
            threadLock.acquire()
            asig = run_knn(datalist, self.params[1], self.params[2])
            need_to_save = False
            threadLock.release()
        elif self.algo=='svm':
            threadLock.acquire()
            asig = run_svm(datalist, self.params[1], self.params[2], self.params[3], self.params[4], self.params[5])
            need_to_save = False
            threadLock.release()

        print("Done!")
        if need_to_save:
            threadLock.acquire()
            print("Now saving data to disk")
            saveAsignationToDisk(asig, self.params[-1])
            threadLock.release()

        print("Completed.")





class MiAplicacion(QtGui.QDialog):
    def __init__(self, parent=None):
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.text_window.clear()
        yearsList.extend([self.ui.check2002, self.ui.check2003, self.ui.check2004, self.ui.check2005, self.ui.check2006,
                     self.ui.check2007, self.ui.check2008, self.ui.check2009, self.ui.check2010, self.ui.check2011,
                     self.ui.check2012, self.ui.check2013, self.ui.check2014, self.ui.check2015, self.ui.check2016])
        self.ui.dimension_edit.setDisabled(True)
        self.ui.threshold_edit_2.setDisabled(True)
        QtCore.QObject.connect(self.ui.pca_box, QtCore.SIGNAL('clicked()'), self.checkPCA)
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.updateDictionaries)
        QtCore.QObject.connect(self.ui.checkAllbutton, QtCore.SIGNAL('clicked()'), self.checkAll)
        QtCore.QObject.connect(self.ui.kmeansbutton, QtCore.SIGNAL('clicked()'), self.executeKmeans)
        QtCore.QObject.connect(self.ui.hierarbutton, QtCore.SIGNAL('clicked()'), self.executeHierarch)
        QtCore.QObject.connect(self.ui.dbscanbutton, QtCore.SIGNAL('clicked()'), self.executeDBSCAN)
        QtCore.QObject.connect(self.ui.knnbutton, QtCore.SIGNAL('clicked()'), self.executekNN)
        QtCore.QObject.connect(self.ui.svm_button, QtCore.SIGNAL('clicked()'), self.executeSVM)


    def checkPCA(self):
        if not self.ui.pca_box.isChecked():
            self.ui.dimension_edit.clear()
            self.ui.threshold_edit_2.clear()
            self.ui.dimension_edit.setDisabled(True)
            self.ui.threshold_edit_2.setDisabled(True)
        else:
            self.ui.dimension_edit.setDisabled(False)
            self.ui.threshold_edit_2.setDisabled(False)
            self.ui.threshold_edit_2.setText("0.99")

    def checkAll(self):
        aux = True
        for year in yearsList:
            aux = aux and year.isChecked()
        if not aux:
            for year in yearsList:
                year.setChecked(True)
        else:
            for year in yearsList:
                year.setChecked(False)

    def updateDictionaries(self):
        dict_list = loadDictionaries(self.getSelectedYears())
        for d in dict_list:
            d.update()
        saveDictionariesToDisk(dict_list)


    def executeKmeans(self):
        if len(threading.enumerate())<2:
            self.ui.text_window.clear()
            try:
                it = int(self.ui.kmeans_iters_line.text())
                tim = int(self.ui.kmeans_times_line.text())
                k = int(self.ui.kmeans_k_line.text())
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of K-means, please revise.")
            print("\nLoading dictionaries and extracting vulnerabilities...")
            my_years, dictionaries, vuln_list = self.loadData()
            datalist = vuln_list
            if self.ui.pca_box.isChecked():
                datalist = self.applyPCA(vuln_list)
            t = MyThread('kmeans', [datalist, it, tim, k, dictionaries])
            t.daemon = True
            t.start()

    def executeHierarch(self):
        if len(threading.enumerate())<2:
            self.ui.text_window.clear()
            try:
                max_d = int(self.ui.hier_maxd_line.text())
                link = str(self.ui.hier_linkage_box.currentText())
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of Hierarchical, please revise.")
            print("\nLoading dictionaries and extracting vulnerabilities...")
            my_years, dictionaries, vuln_list = self.loadData()
            datalist = vuln_list
            if self.ui.pca_box.isChecked():
                datalist = self.applyPCA(vuln_list)
            t = MyThread('hierarch', [datalist, max_d, link, dictionaries])
            t.daemon = True
            t.start()

    def executeDBSCAN(self):
        if len(threading.enumerate())<2:
            self.ui.text_window.clear()
            try:
                eps = float(self.ui.dbscan_eps_line.text())
                minps = int(self.ui.dbscan_minpts_line.text())
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of DBSCAN, please revise.")
            print("\nLoading dictionaries and extracting vulnerabilities...")
            my_years, dictionaries, vuln_list = self.loadData()
            datalist = vuln_list
            if self.ui.pca_box.isChecked():
                datalist = self.applyPCA(vuln_list)
            t = MyThread('dbscan', [datalist, eps, minps, dictionaries])
            t.daemon = True
            t.start()

    def executekNN(self):
        if len(threading.enumerate()) < 2:
            self.ui.text_window.clear()
            try:
                n = int(self.ui.knn_n_line.text())
                perc = float(self.ui.knn_perc_line.text())/100
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of K-nn, please revise.")
            print("\nLoading dictionaries and extracting vulnerabilities...")
            my_years, dictionaries, vuln_list = self.loadData()
            train_list, test_list = self.separateData(vuln_list, perc)
            data_list, validate_list = train_list, test_list
            if self.ui.pca_box.isChecked():
                data_list = self.applyPCA(train_list)
                validate_list = self.applyPCA(test_list)
            t = MyThread('knn', [data_list, validate_list, n])
            t.daemon = True
            t.start()

    def executeSVM(self):
        if len(threading.enumerate()) < 2:
            self.ui.text_window.clear()
            try:
                gamma = float(self.ui.svm_gamma_line.text())
                r = float(self.ui.svm_r_line.text())
                deg = int(self.ui.svm_deg_line.text())
                kernel = str(self.ui.svm_kernel_box.currentText())
                perc = float(self.ui.svm_perc_line.text())/100
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of the SVM, please revise.")
            print("\nLoading dictionaries and extracting vulnerabilities...")
            my_years, dictionaries, vuln_list = self.loadData()
            train_list, test_list = self.separateData(vuln_list, perc)
            data_list, validate_list = train_list, test_list
            if self.ui.pca_box.isChecked():
                data_list = self.applyPCA(train_list)
                validate_list = self.applyPCA(test_list)
            t = MyThread('svm', [data_list, validate_list, kernel, gamma, deg, r])
            t.daemon = True
            t.start()


    def loadData(self):
        my_years = self.getSelectedYears()
        dictionaries = loadDictionaries(my_years)
        vuln_list = self.getVulnerabilities(dictionaries)
        return my_years, dictionaries, vuln_list


    def getSelectedYears(self):
        result = []
        for year in yearsList:
            if year.isChecked():
                result.append(str(year.text()))
        return result


    def getDictionaries(self, list_of_years):
        dictionary_list = []
        for i in list_of_years:
            try:
                with open("../dictionaries/VulnDictionary_" + str(i).strip('~') + ".p", 'rb') as f:
                    dictionary_list.append(pickle.load(f))
            except IOError as err:
                print("Error with dictionary " + str(i) + " - " + str(err))
                print("Creating dictionary from scratch")
                dictionary_list.append(VulnDictionary(i).update())
        return dictionary_list


    def getVulnerabilities(self, dictionary_list):
        count = 0
        vuln_list = []
        for d in dictionary_list:
            count = count + len(d.dict.keys())
            for v in d.dict.values():
                vuln_list.append(v)
        print("Total: " + str(count))
        return vuln_list


    def applyPCA(self, datalist):
        try:
            d = int(self.ui.dimension_edit.text())
        except ValueError:
            d = None

        try:
            t = float(self.ui.threshold_edit_2.text())
        except ValueError:
            t = None

        return pca(datalist, d, t)


    def separateData(self, datalist, perc):
        positions = sample(range(len(datalist)), int((1-perc) * (len(datalist))))

        train_list = []
        test_list = []
        for i in range(len(datalist)):
            if ((i in positions) and (datalist[i].group != -1)):
                test_list.append(datalist[i])
            elif ((not (i in positions)) and (datalist[i].group != -1)):
                train_list.append(datalist[i])
        print("Training with: "+str(len(train_list))+" samples  --  Testing with: "+str(len(test_list))+" samples")
        return train_list, test_list


    def normalOutputWritten(self, text):
        self.ui.text_window.append(text.strip("\n"))



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    my_app = MiAplicacion()
    my_app.show()
    sys.exit(app.exec_())