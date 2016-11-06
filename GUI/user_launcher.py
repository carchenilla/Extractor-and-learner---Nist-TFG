from GUI.user_application_GUI import *
from data_types.VulnDictionary import *
from numpy import array, float32
from PyQt4.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from validating.kNN import run_knn
from validating.svm import run_svm
from others.pca import pca
from random import sample
from others.loadAndSave import *
import sys, threading, datetime

yearsList = []
comboBoxesList = []
threadLock = threading.Lock()

ACCESS_VECTOR = {'Local access':1, 'Adjacent Network':2, 'Network':3}
ACCESS_COMPLEXITY = {'High':3, 'Medium':2, 'Low':1}
AUTHENTIFICATION = {'None required':1, 'Requires single instance':2, 'Requires multiple instances':3}
CONF_IMPACT = {'None':1, 'Partial':2,'Complete':3}
INTEG_IMPACT = {'None':1, 'Partial':2,'Complete':3}
AVAIL_IMPACT = {'None':1, 'Partial':2,'Complete':3}

FEATURES_LIST = [ACCESS_VECTOR, ACCESS_COMPLEXITY, AUTHENTIFICATION, CONF_IMPACT, INTEG_IMPACT, AVAIL_IMPACT]


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class AlgorithmWorker(QObject):

    def __init__(self, parent):
        QObject.__init__(self)
        parent.newTask.connect(self.execute)


    @pyqtSlot(object)
    def execute(self, arguments):
        algo = arguments[0]
        params = arguments[1]
        datalist = params[0]
        if algo == 'knn':
            threadLock.acquire()
            (classes, true, predicted) = run_knn(datalist, params[1], params[2])
            threadLock.release()
        elif algo == 'svm':
            threadLock.acquire()
            (classes, true, predicted) = run_svm(datalist, params[1], params[2], params[3], params[4], params[5])
            threadLock.release()
        if len(params[1])!=1:
            print("Saving results to .txt file")
        for i in range(len(params[1])):
            self.printRepresentative(params[1][i].name, params[1][i].vector, predicted[i], datalist, params[1])
        print("Completed.")


    def printRepresentative(self, name, vector, group, datalist, testlist):
        my_vulns = [v for v in datalist if v.group==group]
        string = ""
        try:
            positions = sample(range(len(my_vulns)), 3)
        except:
            positions = list(range(len(my_vulns)))
        for p in positions:
            string = string + my_vulns[p].to_string()+"\n"

        if len(testlist)!=1:
            with open("../vulnerabilities/results-"+str(name)+".txt", 'w') as f:
                print("Vulnerability " + str(name) + " with vector "+str(vector)+" was classified in group "
                      + str(group)+"\n", file=f)
                print("Representative vulnerabilities of this group are: ", file=f)
                print(string, file=f)
        else:
            print("Vulnerability " + str(name) + "with vector " + str(vector) + "\nwas classified in group "
                  + str(group) + "\n")
            print("Representative vulnerabilities of this group are: ")
            print(string)

    @QtCore.pyqtSlot()
    def start(self):
        print("[%s] start()" % QtCore.QThread.currentThread().objectName())


class MiAplicacion(QtGui.QDialog):

    newTask = pyqtSignal(object)

    def __init__(self, parent=None):
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        QtGui.QWidget.__init__(self,parent)
        self.worker = AlgorithmWorker(self)
        self.thread = QThread(self, objectName="worker_thread")
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.thread.daemon = True
        self.thread.start()
        self.ui = Ui_TFG()
        self.ui.setupUi(self)
        self.ui.text_window.clear()
        yearsList.extend([self.ui.check2002, self.ui.check2003, self.ui.check2004, self.ui.check2005, self.ui.check2006,
                     self.ui.check2007, self.ui.check2008, self.ui.check2009, self.ui.check2010, self.ui.check2011,
                     self.ui.check2012, self.ui.check2013, self.ui.check2014, self.ui.check2015, self.ui.check2016])
        comboBoxesList.extend([self.ui.av_box, self.ui.ac_box, self.ui.auth_box, self.ui.conf_box, self.ui.int_box,
                               self.ui.avail_box])
        self.ui.dimension_edit.setDisabled(True)
        self.ui.threshold_edit_2.setDisabled(True)
        self.ui.fileLoad_button.click()
        QtCore.QObject.connect(self.ui.pca_box, QtCore.SIGNAL('clicked()'), self.checkPCA)
        QtCore.QObject.connect(self.ui.checkAllbutton, QtCore.SIGNAL('clicked()'), self.checkAll)
        QtCore.QObject.connect(self.ui.knnbutton_3, QtCore.SIGNAL('clicked()'), self.executekNN)
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


    def executekNN(self):
        if len(threading.enumerate()) < 2:
            self.ui.text_window.clear()
            try:
                n = int(self.ui.knn_n_line.text())
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()

                if self.ui.pca_box.isChecked():
                    data_list = self.applyPCA(vuln_list)
                    test_list = self.applyPCA(self.getTestSubjects())
                else:
                    data_list = vuln_list
                    test_list = self.getTestSubjects()

                if len(data_list)>0:
                    self.newTask.emit(('knn', [data_list, test_list, n]))
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
                print("\nLoading dictionaries and extracting vulnerabilities...")
                my_years, dictionaries, vuln_list = self.loadData()

                if self.ui.pca_box.isChecked():
                    data_list = self.applyPCA(vuln_list)
                    test_list = self.applyPCA(self.getTestSubjects())
                else:
                    data_list = vuln_list
                    test_list = self.getTestSubjects()

                if len(data_list) > 0:
                    self.newTask.emit(('svm', [data_list, test_list, kernel, gamma, deg, r]))
                else:
                    print("No vulnerabilities selected")
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of the SVM, please revise.")


    def getTestSubjects(self):
        if self.ui.formLoad_button.isChecked():
            try:
                vector = []
                vector.append(float(self.ui.bscore_edit.text()))
                vector.append(float(self.ui.imscore_edit.text()))
                vector.append(float(self.ui.expscore_edit.text()))
                for i in range(6):
                    vector.append(FEATURES_LIST[i].get(str(comboBoxesList[i].currentText())))
                v = Vulnerability(str(self.ui.vulnName_edit.text()), datetime.date(2000,1,1), datetime.date(2000,1,1),
                                 vector[0], array(vector, dtype=float32), "No description", "No soft list")
                return [v]
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of the Vulnerability, please revise.")
        elif self.ui.fileLoad_button.isChecked():
            try:
                vuln_dictionary = VulnDictionary(None)
                vuln_dictionary.parseXML(filename=str(self.ui.filename_edit.text()))
                return list(vuln_dictionary.dict.values())
            except ValueError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error in a parameter of s Vulnerability, please revise.")
            except IOError as err:
                self.ui.text_window.clear()
                print(str(err))
                print("Error when operating with the file, please revise")



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

    def normalOutputWritten(self, text):
        self.ui.text_window.append(text.strip("\n"))



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    QThread.currentThread().setObjectName("main")
    my_app = MiAplicacion()
    my_app.show()
    sys.exit(app.exec_())