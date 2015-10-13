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
        self.jsonInput()

        super(Correlation, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        form = QtGui.QFormLayout()
        '''
        self.txtSepFile = gui.QLineEdit()
        btnSepFile = QtGui.QPushButton('...')
        btnSepFile.setMaximumWidth(40)
        btnSepFile.clicked.connect(self.chooseDbFile)
        boxSepFile = gui.QHBoxLayout()
        boxSepFile.addWidget(self.txtSepFile)
        boxSepFile.addWidget(btnSepFile)
        form.addRow('input file', boxSepFile)
        '''
        self.ThesholdBox = QtGui.QLineEdit()
        self.ThesholdBox.setText('0.0')
        self.ThesholdBox.setAlignment(QtCore.Qt.AlignRight)
        self.ThesholdBox.setFixedWidth(100)
        form.addRow('corr theshold', self.ThesholdBox)

    
        self.VarMinBox = QtGui.QLineEdit()
        self.VarMinBox.setText('1')
        self.VarMinBox.setAlignment(QtCore.Qt.AlignRight)
        self.VarMinBox.setFixedWidth(100)
        form.addRow('deg threshold', self.VarMinBox)
        

        self.winSizeBox = QtGui.QLineEdit()
        self.winSizeBox.setText('40')
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


        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(self.jointSize)
        self.table.setHorizontalHeaderLabels("use_2 joint") 
        for i in range(self.jointSize):
            jItem = QtGui.QTableWidgetItem(str(i))
            self.table.setHorizontalHeaderItem(i, jItem)

        font = QtGui.QFont()
        font.setFamily(u"DejaVu Sans")
        font.setPointSize(8)



        self.table.horizontalHeader().setFont(font)
        self.table.verticalHeader().setFont(font)
        self.table.resizeColumnsToContents()

        #self.table.setItem(0, 0, QtGui.QTableWidgetItem(1))


        boxTable = QtGui.QHBoxLayout()
        boxTable.addWidget(self.table)
 
        grid.addLayout(form,1,0)
        grid.addLayout(boxCtrl,2,0)
        grid.addLayout(boxTable,3,0)

        self.setLayout(grid)
        self.resize(400,100)

        self.setWindowTitle("joint select window")
        self.show()

    def jsonInput(self):
        f = open('test_self.json', 'r');
        jsonData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()

        self.data = {}
        self.pdata = {}
        self.jointnames = []
        self.time = []
        self.usrSize = len(jsonData)

        u = 0;
        for user in jsonData:
            #angle
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
            #position
            psize = len(user["datas"][0]["jdata"])            
            tsize = len(user["datas"])
            pobj = {}
            for p in range(0, psize):
                plist = []
                for t in range(0, tsize):
                    pl = []
                    #print str(p)+","+str(t)
                    #print user["datas"][t]["jdata"][p]
                    pl.append(user["datas"][t]["jdata"][p][0])
                    pl.append(user["datas"][t]["jdata"][p][1])
                    pl.append(user["datas"][t]["jdata"][p][2])
                    plist.append(pl)
                pobj[p] = plist
            self.pdata[u] = pobj

            u+=1

        for itime in jsonData[0]["datas"]:
            #print itime["time"]
            self.time.append(itime["time"])

        if len(jsonData) == 1:
            self.data[1] = self.data[0]
        
        self.jointSize = len(self.data[0])
        self.dataSize = len(self.data[0][0])

        #joint index
        f = open('joint_index.json', 'r');
        jsonIndexData = json.load(f)
        #print json.dumps(jsonData, sort_keys = True, indent = 4)
        f.close()
        self.idata = []

        for index in jsonIndexData:
            ilist = []
            for i in index:
                ilist.append(i)
            self.idata.append(ilist)
            
        #print self.idata

    def doExec(self):
        print "exec! joint_"+self.cmbSrcJoints.currentText()
        j_idx_u1 = int(self.cmbSrcJoints.currentText())
        self.winSize = int(self.winSizeBox.text())

        self.maxRange = self.dataSize - self.winSize
        self.threshold = float(self.ThesholdBox.text())
        self.varMin = float(self.VarMinBox.text())*(math.pi/180)

        self.process(j_idx_u1)
        self.time_setting()
        #print len(self.corrMat)
        #print len(self.corrMat[0])
        self.updateTable()
        print "end"

    def doViz(self, cItem):
        idx_u0 = int(self.cmbSrcJoints.currentText())

        print "now viz!"+str(cItem.row())+","+str(cItem.column())
        jidx = self.idata[cItem.column()]
        #print str(self.idata[cItem.column()][0])+","+str(self.idata[cItem.column()][1])+","+str(self.idata[cItem.column()][2]) 
        print str(jidx[0])+","+str(jidx[1])+","+str(jidx[2])
        
        i0 = jidx[0]
        i1 = jidx[1]
        i2 = jidx[2]

        usr = 0
        delay = cItem.row() - self.maxRange

        print "len:"+str(len(self.pdata[usr][i0]))

        for didx in range(0, self.winSize):
            dt1 = self.dataSize - self.winSize
            dt2 = dt1 - abs(delay)
            if delay >= 0:
                plist = []
                pl = []
                print "dt:"+str(dt)
                print "dt+didx:"+str(dt+didx)
                print str(self.pdata[usr][i0][dt2+didx][0])+","+str(self.pdata[usr][i0][dt2+didx][1])+","+str(self.pdata[usr][i0][dt2+didx][2])
                
                #print str(self.pdata[usr][i1][dt][0])+","+str(self.pdata[usr][i1][dt][1])+","+str(self.pdata[usr][i1][dt][2])
                #print str(self.pdata[usr][i2][dt][0])+","+str(self.pdata[usr][i2][dt][1])+","+str(self.pdata[usr][i2][dt][2])
            if delay < 0:
                pass
        #print self.maxRange
        #print "now viz!"+str(row)

    def updateTable(self):
        self.table.clear()
        self.table.setRowCount(self.maxRange*2+1)
        self.table.resizeRowsToContents()
        
        hor = True

        for i in range(len(self.corrMat)):
            iItem = QtGui.QTableWidgetItem(str(-self.maxRange+i))
            self.table.setVerticalHeaderItem(i, iItem)
            self.table.verticalHeaderItem(i).setToolTip(str(self.timedata[i]))
            for j in range(len(self.corrMat[i])):

                if hor == True:
                    jItem = QtGui.QTableWidgetItem(str(j))
                    self.table.setHorizontalHeaderItem(j, jItem)
                    hot = False

                c = (1+self.corrMat[i][j])*(255/2)
                self.table.setItem(i, j, QtGui.QTableWidgetItem())
                self.table.item(i, j).setBackground(QtGui.QColor(c,c,c))
                self.table.item(i, j).setToolTip(str(self.corrMat[i][j]))
        
        print "click"
        self.table.itemClicked.connect(self.doViz)

    def process(self, j_idx_u1):
        #print "user1 data[]:"+str(self.data[0])
        #print "user2 data[]:"+str(self.data[1])
        print "data size:"+str(self.dataSize)
        print "joint size:"+str(self.jointSize)
        print "winsize:"+str(self.winSize)
        print "max_range:"+str(self.maxRange)

        self.corrMat = [[0 for i in range(self.jointSize)] for j in range(self.maxRange*2+1)]

        if self.maxRange < 0:
            print "max_range:"+str(self.maxRange)+" is error"
            pass

        for j_idx_u2 in range(0, self.jointSize):
            self.calc_proc(j_idx_u1, j_idx_u2)

    def calc_proc(self, idx_u1, idx_u2): 
        count = 0
        for dt in range(-self.maxRange, self.maxRange+1):
            set1 = []
            set2 = [] 
            for idx in range(0, self.winSize):
                d1_idx = 0
                d2_idx = 0
                if dt >= 0:
                    d1_idx = self.dataSize-self.winSize-abs(dt)
                    d2_idx = self.dataSize-self.winSize

                if dt < 0:
                    d1_idx = self.dataSize-self.winSize                 
                    d2_idx = self.dataSize-self.winSize-abs(dt)
                    
                set1.append(self.data[0][idx_u1][d1_idx+idx])
                set2.append(self.data[1][idx_u2][d2_idx+idx])
            

            
            #print "user1 joint_"+str(idx_u1)+" dt:"+str(dt)+", set1:"+str(set1)
            #print "user2 joint_"+str(idx_u2)+" dt:"+str(dt)+", set2:"+str(set2)

            #std1 = self.var_ave(set1)
            #std2 = self.var_ave(set2)
            #print "var_ave1:"+str(std1)+", var_ave2:"+str(std2)
            #if std1 >= self.varMin and std2 >= self.varMin:
            corr = numpy.corrcoef(set1, set2)
            r_val=corr[0,1]

            if math.fabs(r_val) > self.threshold:
                #print "("+str(idx_u1)+", "+ str(idx_u2)+"): dt:" + str(dt)+", r:"+str(r_val)
                self.corrMat[count][idx_u2]=r_val

            count+=1

    def time_setting(self):
        count = 0
        self.timedata = []
        for dt in range(-self.maxRange, self.maxRange+1):
            if dt > 0:
                self.timedata.append(self.time[abs(dt)]-self.time[0])
            if dt <= 0:
                self.timedata.append(self.time[0]-self.time[abs(dt)])
                    

    def var_ave(self, x):
        ave = numpy.average(x)
        total = 0
        for i in range(len(x)):
            total += abs(x[i] - ave)
        return total/len(x)


def main():
    app = QtGui.QApplication(sys.argv)
    corr = Correlation()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
