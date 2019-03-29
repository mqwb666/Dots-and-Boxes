# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from policy import *
from functools import partial

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 445)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = [[QtWidgets.QPushButton(self.centralwidget) for c in range(11)] for r in range(11)]
        for r, row in enumerate(self.pushButton):
            for c, pb in enumerate(row):
                if r % 2 == 1 and c % 2 == 1:
                    pb.setGeometry(QtCore.QRect(56+75*((c-1)//2), 26+75*((r-1)//2), 58, 58))
                    pb.setStyleSheet('''
                    QPushButton{
                        background-color:rgb(250, 250, 250);
                        border-radius: 2px;
                    }''') 
                elif r % 2 == 0 and c % 2 == 1:
                    pb.setGeometry(QtCore.QRect(56+75*((c-1)//2), 11+75*(r//2), 58, 13))
                    pb.setStyleSheet('''
                    QPushButton{
                        background-color:white;
                        border-radius: 3px;
                        border: 1px solid rgb(215, 215, 215);
                    }
                    QPushButton:hover{
                        background-color: red;
                    }''')
                    pb.clicked.connect(partial(lambda x,y: self.people_move(x,y),r,c))
                elif r % 2 == 1 and c % 2 == 0:
                    pb.setGeometry(QtCore.QRect(41+75*(c//2), 26+75*((r-1)//2), 13, 58))
                    pb.setStyleSheet('''
                    QPushButton{
                        background-color:white;
                        border-radius: 3px;
                        border: 1px solid rgb(215, 215, 215);
                    }
                    QPushButton:hover{
                        background-color: red;
                    }''')
                    pb.clicked.connect(partial(lambda x,y: self.people_move(x,y),r,c))
                else:
                    pb.setGeometry(QtCore.QRect(40+75*(c//2), 10+75*(r//2), 15, 15))
                    pb.setStyleSheet('')
                    pb.setStyleSheet('''
                    QPushButton{
                        background-color:black;
                        border-radius: 4px;
                    }''') 
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 470, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.action3 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action3")
        self.menu.addAction(self.action1)
        self.menu.addAction(self.action2)
        self.menu.addAction(self.action3)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.p = policy()
        self.cb = [[0 for _ in range(11)] for _ in range(11)]
        self.action1.triggered.connect(self.start_first)
        self.action2.triggered.connect(self.start_back)
        self.action3.triggered.connect(self.print_state)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "特别硬核、特别智障、特别垃圾的点格棋AI"))
        self.menu.setTitle(_translate("MainWindow", "开始"))
        self.action1.setText(_translate("MainWindow", "先手开始"))
        self.action2.setText(_translate("MainWindow", "后手开始"))
        self.action3.setText(_translate("MainWindow", "输出局面"))
    
    def start_first(self):
        self.p = policy()
        self.cb = [[0 for _ in range(11)] for _ in range(11)]
        for i in range(11):
            for j in range(11):
                if i % 2 == 1 and j % 2 == 1: # 格子
                    self.pushButton[i][j].setStyleSheet('''
                    QPushButton{
                        background-color:rgb(250, 250, 250);
                        border-radius: 2px;
                    }''')
                elif i % 2 != j % 2:
                    self.pushButton[i][j].setStyleSheet('''
                    QPushButton{
                        background-color:white;
                        border-radius: 3px;
                        border: 1px solid rgb(215, 215, 215);
                    }
                    QPushButton:hover{
                        background-color: red;
                    }''')

    def start_back(self):
        self.start_first()
        self.p.make_move()
        for i in range(11):
            for j in range(11):
                if self.p.state[i][j] == 1:
                    self.cb[i][j] = -1
                    self.change_edge_color(i,j,1)

    def print_state(self):
        with open('./temp.txt', 'a') as f:
            f.write('>state=\n{}\nscore={}\n'.format(str(self.p.state).replace('],','],\n'),str(self.p.score)))

    def people_move(self,r,c):
        if self.cb[r][c] != 0: return
        self.cb[r][c] = 1
        # 改变边颜色
        self.change_edge_color(r,c,0)
        #判断是否吃子
        self.p.move_edge(r,c,1)
        flag = False
        if r % 2 == 0: # 横边
            if r > 0 and self.p.state[r-1][c] == 0:
                flag = True
                self.cb[r-1][c] = 1
                self.change_node_color(r-1,c,0)
            if r < 10 and self.p.state[r+1][c] == 0:
                self.cb[r+1][c] = 1
                flag = True
                self.change_node_color(r+1,c,0)
        else:
            if c > 0 and self.p.state[r][c-1] == 0:
                self.cb[r][c-1] = 1
                flag = True
                self.change_node_color(r,c-1,0)
            if c < 10 and self.p.state[r][c+1] == 0:
                self.cb[r][c+1] = 1
                flag = True
                self.change_node_color(r,c+1,0)
        if flag: return

        self.p.make_move()

        for i in range(11):
            for j in range(11):
                if i % 2 == 1 and j % 2 == 1: # 格子
                    if self.cb[i][j] == 0 and self.p.state[i][j] == 0:
                        self.cb[i][j] = -1
                        # 改变格子颜色
                        self.change_node_color(i,j,1)
                elif i % 2 != j % 2:
                    if self.cb[i][j] == 0 and self.p.state[i][j] == 1:
                        self.cb[i][j] = -1
                        #改变边颜色
                        self.change_edge_color(i,j,1)

    def change_node_color(self,r,c,player): # player 0人 1电脑
        self.pushButton[r][c].setStyleSheet('''
        QPushButton{
            background-color: %s;
            border-radius: 2px;
        }''' % ('#B0F50000' if player == 0 else '#B03A5FCD'))

    def change_edge_color(self,r,c,player): # player 0人 1电脑
        self.pushButton[r][c].setStyleSheet('''
        QPushButton{
            background-color: %s;
            border-radius: 3px;
            border: 1px solid block;
        }''' % ('#F50000' if player == 0 else '#3A5FCD'))  
    
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()