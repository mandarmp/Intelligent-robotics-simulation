#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserInterface.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#PYTH
# Later added functionality accordingly to trigger events by @mandarmp
#
#https://www.techwithtim.net/tutorials/pyqt5-tutorial/buttons-and-events/ 
#

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import rospy
from std_srvs.srv import Trigger, TriggerRequest
from my_simluations.srv import Queue, QueueRequest, QueueResponse
from PyQt5 import QtCore, QtGui, QtWidgets

rospy.init_node('gui_client',anonymous=False)
#rospy.wait_for_service('/queue_server')
rospy.wait_for_service('/queue_server')
queue_service = rospy.ServiceProxy('/queue_server',Queue)


class Ui_Waiterbot_1(object):
    def button_trigger_func(self,buttonname=None,tablename=None):
        print(buttonname)
        button = self.dockWidgetContents.findChild(QtWidgets.QPushButton,buttonname)
        if button.isChecked(): 
            print("Enqueue:"+ tablename)
            result = queue_service(tablename,1)
            print( result)
        else:
            print("Clear  :",tablename)    
            result = queue_service(tablename,0)
            print( result)

    def kitchen_button(self):
        pass
       
    def setupUi(self, Waiterbot_1):
        Waiterbot_1.setObjectName("Waiterbot_1")
        Waiterbot_1.resize(442, 699)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayoutWidget = QtWidgets.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 221, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(4, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setChecked(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.button_trigger_func("pushButton_3","Table_3"))
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setCheckable(True)
        self.pushButton_1.setChecked(False)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(lambda: self.button_trigger_func("pushButton_1","Table_1"))
        self.gridLayout.addWidget(self.pushButton_1, 1, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(220, 0, 221, 271))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(4, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.button_trigger_func("pushButton_2","Table_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.setChecked(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.button_trigger_func("pushButton_4","Table_4"))
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 540, 441, 141))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.pushButton_9.setObjectName("pushButton_9")
        
        self.gridLayout_3.addWidget(self.pushButton_9, 0, 0, 1, 1)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 270, 221, 271))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(4, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setChecked(False)
        self.pushButton_7.clicked.connect(lambda: self.button_trigger_func("pushButton_7","Table_7"))
        self.gridLayout_4.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.setChecked(False)
        self.pushButton_5.clicked.connect(lambda: self.button_trigger_func("pushButton_5","Table_5"))
        self.gridLayout_4.addWidget(self.pushButton_5, 1, 0, 1, 1)
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.dockWidgetContents)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(220, 270, 221, 271))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setContentsMargins(4, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.setChecked(False)
        self.pushButton_8.clicked.connect(lambda: self.button_trigger_func("pushButton_8","Table_8"))
        self.gridLayout_5.addWidget(self.pushButton_8, 2, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setChecked(False)
        self.pushButton_6.clicked.connect(lambda: self.button_trigger_func("pushButton_6","Table_6"))
        self.gridLayout_5.addWidget(self.pushButton_6, 1, 0, 1, 1)
        Waiterbot_1.setWidget(self.dockWidgetContents)

        self.retranslateUi(Waiterbot_1)
        QtCore.QMetaObject.connectSlotsByName(Waiterbot_1)

    def retranslateUi(self, Waiterbot_1):
        _translate = QtCore.QCoreApplication.translate
        Waiterbot_1.setWindowTitle(_translate("Waiterbot_1", "DockWidget"))
        self.pushButton_3.setText(_translate("Waiterbot_1", "Table 3"))
        self.pushButton_1.setText(_translate("Waiterbot_1", "Table 1"))
        self.pushButton_2.setText(_translate("Waiterbot_1", "Table 2"))
        self.pushButton_4.setText(_translate("Waiterbot_1", "Table 4"))
        self.pushButton_9.setText(_translate("Waiterbot_1", "Kitchen"))
        self.pushButton_7.setText(_translate("Waiterbot_1", "Table 7"))
        self.pushButton_5.setText(_translate("Waiterbot_1", "Table 5"))
        self.pushButton_8.setText(_translate("Waiterbot_1", "Table 8"))
        self.pushButton_6.setText(_translate("Waiterbot_1", "Table 6"))

if __name__== "__main__" :
    import sys
    # rospy.init_node('gui_client',anonymous=False)
    # rospy.wait_for_service('/queue_server')
    # queue_service = rospy.ServiceProxy('/queue_server',Trigger)
    app = QtWidgets.QApplication(sys.argv)
    bot = QtWidgets.QDockWidget()
    ui = Ui_Waiterbot_1()
    ui.setupUi(bot)
    bot.show()
    sys.exit(app.exec_())

main()