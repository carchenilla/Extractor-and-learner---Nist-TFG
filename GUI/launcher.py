from GUI.application_GUI import *
from data_types.VulnDictionary import VulnDictionary
from clustering.kmeans import run_kmeans
from others.pca import pca
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
        if self.algo=='kmeans':
            datalist = self.params[0]
            it = self.params[1]
            ti = self.params[2]
            k = self.params[3]
            threadLock.acquire()
            (cost, asig) = run_kmeans(datalist, it, ti, k)
            print("Done!")
            print("Now saving data to disk")
            need_to_save = True
            threadLock.release()

        if need_to_save:
            self.saveToDisk(asig, self.params[-1])


    def saveToDisk(self, asig, dictionary_list):
        for x in asig:
            found = False
            i = 0
            while ((not found) and (i <= len(dictionary_list))):
                d = dictionary_list[i]
                v = d.dict.get(x[0])
                if v != None:
                    v.group = x[1]
                    found = True
                i = i + 1
        for d in dictionary_list:
            try:
                with open("../dictionaries/VulnDictionary_" + str(d.year) + ".p", 'wb') as f:
                    pickle.dump(d, f)
            except IOError as err:
                print("Error with dictionary " + str(d.year) + " - " + str(err))
        print("Done!")




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
        QtCore.QObject.connect(self.ui.kmeansbutton, QtCore.SIGNAL('clicked()'), self.executeKmeans)


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
            my_years = self.getSelectedYears()
            dictionaries = self.getDictionaries(my_years)
            vuln_list = self.getVulnerabilities(dictionaries)
            datalist = vuln_list
            if self.ui.pca_box.isChecked():
                datalist = self.applyPCA(vuln_list)
            t = MyThread('kmeans', [datalist, it, tim, k, dictionaries])
            t.daemon = True
            t.start()





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
        self.ui.text_window.append("Total: " + str(count))
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
    my_app = MiAplicacion()
    my_app.show()
    sys.exit(app.exec_())