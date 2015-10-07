#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import math
import json
import numpy

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
        self.ThesholdBox.setText('0.4')
        self.ThesholdBox.setAlignment(QtCore.Qt.AlignRight)
        self.ThesholdBox.setFixedWidth(100)
        form.addRow('Theshold', self.ThesholdBox)

        self.VarMinBox = QtGui.QLineEdit()
        self.VarMinBox.setText('0.01')
        self.VarMinBox.setAlignment(QtCore.Qt.AlignRight)
        self.VarMinBox.setFixedWidth(100)
        form.addRow('Var Min', self.VarMinBox)

        self.winSizeBox = QtGui.QLineEdit()
        self.winSizeBox.setText('3')
        self.winSizeBox.setAlignment(QtCore.Qt.AlignRight)
        self.winSizeBox.setFixedWidth(100)
        form.addRow('window size', self.winSizeBox)

        self.cmbSrcJoints = QtGui.QComboBox(self)
        self.cmbSrcJoints.addItems(self.jointnames)
        self.cmbSrcJoints.setFixedWidth(150)
        boxSrcJoints = QtGui.QHBoxLayout()
        boxSrcJoints.addWidget(self.cmbSrcJoints)
        form.addRow('user_1 joint', boxSrcJoints)

        boxCtrl = QtGui.QHBoxLayout()
        btnExec = QtGui.QPushButton('exec')
        btnExec.clicked.connect(self.doExec)
        boxCtrl.addWidget(btnExec)
 
        grid.addLayout(form,1,0)
        grid.addLayout(boxCtrl,2,0)
        self.setLayout(grid)
        self.resize(400,100)

        self.setWindowTitle("joint select window")
        self.show()


    def jsonInput(self):
        print "input"
        f = open('testdata.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.data = {}
        self.jointnames = []
        u = 0;
        for user in jsonData:
            jsize = len(user["datas"][0]["data"])            
            tsize = len(user["datas"])

            jobj = {}
            for j in range(0, jsize):

                jlist = []
                for t in range(0, tsize):
                    jlist.append(user["datas"][t]["data"][j])
                jobj[j] = jlist
                if u == 0:
                    self.jointnames.append(str(j))
            self.data[u]=jobj
            u+=1

    def doExec(self):
        print "exec! joint_"+self.cmbSrcJoints.currentText()
        j_idx_u1 = int(self.cmbSrcJoints.currentText())
        self.winSize = int(self.winSizeBox.text())
        self.jointSize = len(self.data[0])
        self.dataSize = len(self.data[0][j_idx_u1])
        self.maxRange = self.dataSize - self.winSize
        self.threshold = float(self.ThesholdBox.text())
        self.varMin = float(self.VarMinBox.text())
        self.process(j_idx_u1)
        print "end"

    def process(self, j_idx_u1):
        print "user1 data[]:"+str(self.data[0])
        print "user2 data[]:"+str(self.data[1])
        print "data size:"+str(self.dataSize)
        print "joint size:"+str(self.jointSize)
        print "winsize:"+str(self.winSize)
        print "max_range:"+str(self.maxRange)

        if self.maxRange < 0:
            print "max_range:"+str(self.maxRange)+" is error"
            pass

        for j_idx_u2 in range(0, self.jointSize):
            self.calc_proc(j_idx_u1, j_idx_u2)

    def calc_proc(self, idx_u1, idx_u2): 
       
        for dt in range(-self.maxRange, self.maxRange+1):
            set1 = []
            set2 = [] 
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

            print "user1 joint_"+str(idx_u1)+" dt:"+str(dt)+", set1:"+str(set1)
            print "user2 joint_"+str(idx_u2)+" dt:"+str(dt)+", set2:"+str(set2)

            var1 = numpy.var(set1)
            if var1 < self.varMin:
                continue

            var2 = numpy.var(set2)
            if var2 < self.varMin:
                continue

            corr = numpy.corrcoef(set1, set2)
            r_val=corr[0,1]

            if math.fabs(r_val) > self.threshold:
                print "("+str(idx_u1)+", "+ str(idx_u2)+"): dt:" + str(dt)+", r:"+str(r_val)
                print "var1:"+str(var1)+",var2:"+str(var2)

def main():
    app = QtGui.QApplication(sys.argv)
    corr = Correlation()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
