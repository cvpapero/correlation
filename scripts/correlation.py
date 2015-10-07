#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import math
import json

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

class Correlation(QtGui.QWidget):

    def __init__(self):
        
        #self.winsize = 100
        #self.threshold = 0.7
        self.jsonInput()

        super(Correlation, self).__init__()
        self.initUI()

        #print len(self.data[0][1])

    def initUI(self):
        grid = QtGui.QGridLayout()
        form = QtGui.QFormLayout()

        self.ThesholdBox = QtGui.QLineEdit()
        self.ThesholdBox.setText('0.7')
        self.ThesholdBox.setAlignment(QtCore.Qt.AlignRight)
        self.ThesholdBox.setFixedWidth(100)
        form.addRow('Theshold', self.ThesholdBox)

        self.winSizeBox = QtGui.QLineEdit()
        self.winSizeBox.setText('30')
        self.winSizeBox.setAlignment(QtCore.Qt.AlignRight)
        self.winSizeBox.setFixedWidth(100)
        form.addRow('window size', self.winSizeBox)


        joints = ("0","1","2","3","4","5","6","7")
 
        self.cmbSrcJoints = QtGui.QComboBox(self)
        self.cmbSrcJoints.addItems(joints)
        self.cmbSrcJoints.setFixedWidth(150)
        boxSrcJoints = QtGui.QHBoxLayout()
        boxSrcJoints.addWidget(self.cmbSrcJoints)
        form.addRow('user1 joints', boxSrcJoints)

        boxCtrl = QtGui.QHBoxLayout()
        btnExec = QtGui.QPushButton('exec')
        btnExec.clicked.connect(self.doExec)
        boxCtrl.addWidget(btnExec)
 
        grid.addLayout(form,1,0)
        grid.addLayout(boxCtrl,2,0)
        self.setLayout(grid)
        self.resize(400,100)

        self.setWindowTitle("joints select")
        self.show()


    def jsonInput(self):
        print "input"
        f = open('outdata2.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.data = {}
        u = 0;
        for user in jsonData:
            jsize = len(user["datas"][0]["data"])            
            tsize = len(user["datas"])
            #print tsize

            jobj = {}
            for j in range(0, jsize):
                jlist = []
                for t in range(0, tsize):
                    jlist.append(user["datas"][t]["data"][j])
                jobj[j] = jlist
                #self.jointnames = self.jointnames + tuple("joint_"+str(j))

            self.data[u]=jobj
            u+=1

    def doExec(self):
        print "exec! joint_"+self.cmbSrcJoints.currentText()
        j_idx_u1 = int(self.cmbSrcJoints.currentText())
        self.process(j_idx_u1)
        print "end"

    def process(self, j_idx_u1):
        print "process"
        self.winSize = int(self.winSizeBox.text())
        self.jointSize = len(self.data[0])
        self.dataSize = len(self.data[0][j_idx_u1])
        self.maxRange = self.dataSize - self.winSize
        self.threshold = float(self.ThesholdBox.text())

        print self.jointSize

        if self.maxRange < 0:
            print "max_range:"+str(self.maxRange)+" is error"
            pass

        for j_idx_u2 in range(0, self.jointSize):
            self.calc_proc(j_idx_u1, j_idx_u2)

    def calc_proc(self, idx_u1, idx_u2): 
        set1 = []
        set2 = []        
        for dt in range(-self.maxRange, self.maxRange):
            for idx in range(0, self.winSize):
                d1_idx = 0
                d2_idx = 0
                if dt < 0:
                    d1_idx = self.dataSize-self.winSize-abs(dt)
                    d2_idx = self.dataSize-self.winSize
                if dt >= 0:
                    d1_idx = self.dataSize-self.winSize                 
                    d2_idx = self.dataSize-self.winSize-abs(dt)
                set1.append(self.data[0][idx_u1][d1_idx+idx])
                set2.append(self.data[1][idx_u2][d1_idx+idx])

            self.dst = 0
            self.calc_corr(set1, set1, False)
            if self.dst < 0.01:
                pass

            self.calc_corr(set2, set2, False)
            if self.dst < 0.01:
                pass

            self.calc_corr(set1, set2, True)
            if math.fabs(self.dst) > self.threshold:
                print "("+str(idx_u1)+", "+ str(idx_u2)+"): dt:" + str(dt)+", r:"+str(self.dst)


    def calc_corr(self, d1, d2, denom):
        d1_ave=self.mean(d1)
        d2_ave=self.mean(d2)
        
        sig1sig2 = 0
        sig1sq = 0
        sig2sq = 0

        for i in range(0, len(d1)):
            sig1 = d1[i] - d1_ave
            sig2 = d2[i] - d2_ave
            sig1sig2 += sig1*sig2
            sig1sq += sig1*sig1  
            sig2sq += sig2*sig2

        if denom == True:
            self.dst = sig1sig2 / (math.sqrt(sig1sq)*math.sqrt(sig2sq))
        else:
            self.dst = math.sqrt(sig1sq) * math.sqrt(sig2sq)
    
    def mean(self, data):
        sum = 0
        for d in data:
            sum += d
        return sum/len(data)

def main():
    app = QtGui.QApplication(sys.argv)
    corr = Correlation()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
