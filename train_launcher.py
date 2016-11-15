from GUI.train_GUI import *
from numpy import zeros, float32
from sklearn.metrics import confusion_matrix
from random import sample
from PyQt4.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from clustering.kmeans import run_kmeans
from clustering.hierarchical import run_hierarchical
from clustering.dbscan import run_dbscan
from validating.kNN import run_knn
from validating.svm import run_svm
from others.pca import pca
from others.loadAndSave import *
import sys, threading, itertools, numpy as np, matplotlib.pyplot as plt

yearsList = []
threadLock = threading.Lock()

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class AlgorithmWorker(QObject):

    taskDone = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self)
        parent.newTask.connect(self.execute)


    @pyqtSlot(object)
    def execute(self, arguments):
        algo = arguments[0]
        params = arguments[1]
        save_classification = False
        save_validation = False
        datalist = params[0]
        if algo == 'kmeans':
            threadLock.acquire()
            (cost, asig) = run_kmeans(datalist, params[1], params[2], params[3])
            save_classification = True
            threadLock.release()
        elif algo == 'hierarch':
            threadLock.acquire()
            asig = run_hierarchical(datalist, params[1], params[2])
            save_classification = True
            threadLock.release()
        elif algo == 'dbscan':
            threadLock.acquire()
            asig = run_dbscan(datalist, params[1], params[2])
            save_classification = True
            threadLock.release()
        elif algo == 'knn':
            threadLock.acquire()
            valid = run_knn(datalist, params[1], params[2])
            save_validation = True
            threadLock.release()
        elif algo == 'svm':
            threadLock.acquire()
            valid = run_svm(datalist, params[1], params[2], params[3], params[4], params[5])
            save_validation = True
            threadLock.release()

        print("Done!")
        if save_classification:
            threadLock.acquire()
            print("Now saving data to disk")
            saveAsignationToDisk(asig, params[-1])
            threadLock.release()
        elif save_validation:
            threadLock.acquire()
            saveValidationToDisk(valid[0], valid[1], valid[2])
            threadLock.release()
            self.taskDone.emit()

        print("Completed.")

    @QtCore.pyqtSlot()
    def start(self):
        print("[%s] start()" % QtCore.QThread.currentThread().objectName(), file=sys.stderr)


class MiAplicacion(QtGui.QDialog):

    newTask = pyqtSignal(object)

    def __init__(self, parent=None):
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        QtGui.QWidget.__init__(self,parent)
        self.worker = AlgorithmWorker(self)
        self.thread = QThread(self, objectName="worker_thread")
        self.worker.moveToThread(self.thread)
        self.worker.taskDone.connect(self.plotConfusionMatrix)
        self.thread.started.connect(self.worker.start)
        self.thread.daemon = True
        self.thread.start()
        self.ui = Ui_TFG()
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
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()
                datalist = vuln_list
                if self.ui.pca_box.isChecked():
                    datalist = self.applyPCA(vuln_list)
                if len(datalist)>0:
                    self.newTask.emit(('kmeans', [datalist, it, tim, k, dictionaries]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of K-means, please revise.")

    def executeHierarch(self):
        if len(threading.enumerate())<2:
            self.ui.text_window.clear()
            try:
                max_d = int(self.ui.hier_maxd_line.text())
                link = str(self.ui.hier_linkage_box.currentText())
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()
                datalist = vuln_list
                if self.ui.pca_box.isChecked():
                    datalist = self.applyPCA(vuln_list)
                if len(datalist) > 0:
                    self.newTask.emit(('hierarch', [datalist, max_d, link, dictionaries]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of Hierarchical, please revise.")

    def executeDBSCAN(self):
        if len(threading.enumerate())<2:
            self.ui.text_window.clear()
            try:
                eps = float(self.ui.dbscan_eps_line.text())
                minps = int(self.ui.dbscan_minpts_line.text())
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()
                datalist = vuln_list
                if self.ui.pca_box.isChecked():
                    datalist = self.applyPCA(vuln_list)
                if len(datalist)>0:
                    self.newTask.emit(('dbscan', [datalist, eps, minps, dictionaries]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of DBSCAN, please revise.")

    def executekNN(self):
        if len(threading.enumerate()) < 2:
            self.ui.text_window.clear()
            try:
                n = int(self.ui.knn_n_line.text())
                perc = float(self.ui.knn_perc_line.text())/100
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()
                train_list, test_list = self.separateData(vuln_list, perc)
                data_list, validate_list = train_list, test_list
                if self.ui.pca_box.isChecked():
                    data_list = self.applyPCA(train_list)
                    validate_list = self.applyPCA(test_list)
                if len(data_list)>0:
                    self.newTask.emit(('knn', [data_list, validate_list, n]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of K-nn, please revise.")


    def executeSVM(self):
        if len(threading.enumerate()) < 2:
            self.ui.text_window.clear()
            try:
                gamma = float(self.ui.svm_gamma_line.text())
                r = float(self.ui.svm_r_line.text())
                deg = int(self.ui.svm_deg_line.text())
                kernel = str(self.ui.svm_kernel_box.currentText())
                perc = float(self.ui.svm_perc_line.text())/100
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()
                train_list, test_list = self.separateData(vuln_list, perc)
                data_list, validate_list = train_list, test_list
                if self.ui.pca_box.isChecked():
                    data_list = self.applyPCA(train_list)
                    validate_list = self.applyPCA(test_list)
                if len(data_list) > 0:
                    self.newTask.emit(('svm', [data_list, validate_list, kernel, gamma, deg, r]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of the SVM, please revise.")


    def loadData(self):
        my_years = self.getSelectedYears()
        dictionaries = loadDictionaries(my_years)
        vuln_list = self.getVulnerabilities(dictionaries)
        return my_years, dictionaries, vuln_list


    def getSelectedYears(self):
        result = []
        for year in yearsList:
            if year.isChecked():
                result.append(str(year.text()).strip("~"))
        return result


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


    def plotConfusionMatrix(self):
        classes, true, predicted = loadValidationFromDisk()
        cnf = self.normalizeMatrix(confusion_matrix(true, predicted, labels=classes))
        plt.imshow(cnf, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion matrix")
        plt.colorbar()
        marks = np.arange(len(classes))
        plt.xticks(marks, classes, rotation=45)
        plt.yticks(marks, classes)
        threshold = cnf.max() / 2
        for i, j in itertools.product(range(cnf.shape[0]), range(cnf.shape[1])):
            plt.text(j, i, cnf[i, j],
                     horizontalalignment="center",
                     color="white" if cnf[i, j] > threshold else "black")
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()


    def normalizeMatrix(self, m):
        new_m = zeros((m.shape[0], m.shape[1]), dtype=float32)
        for i in range(new_m.shape[0]):
            total = int(sum(list(m[i,:])))
            for j in range(new_m.shape[1]):
                new_m[i,j] = m[i,j]/total
        return new_m


    def normalOutputWritten(self, text):
        self.ui.text_window.append(text.strip("\n"))



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    QThread.currentThread().setObjectName("main")
    my_app = MiAplicacion()
    my_app.show()
    sys.exit(app.exec_())