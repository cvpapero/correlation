#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('This is a <b>Quit</b> widget')
        qbtn.resize(qbtn.sizeHint())
        #qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        QObject.connect(qbtn, SIGNAL("clicked()"), self, SLOT("on_click_botton()"))
        qbtn.move(50, 50)   

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')    
        self.show()

        
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()      

    @pyqtSignature("")
    def on_click_botton(self):
        print "ok"


def main():
    app = QtGui.QApplication(sys.argv)

    ex = Example()
    
    '''
    w = QtGui.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    '''

    sys.exit(app.exec_())

if __name__=='__main__':
    main()
