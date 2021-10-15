# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front_end.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import pandas as pd
import datetime
from tqdm import tqdm
from banggood_parser import BanggoodDescription


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(458, 274)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.output_path = None
        self.banggood_csv = None

        self.error_excel = QMessageBox()
        self.error_excel.setWindowTitle("Error")
        self.error_excel.setText("Please Load Excel File")
        self.error_excel.setIcon(QMessageBox.Warning)

        self.error_output_path = QMessageBox()
        self.error_output_path.setWindowTitle("Error")
        self.error_output_path.setText("Please Specify Save Path")
        self.error_output_path.setIcon(QMessageBox.Warning)


        self.btn_load_excel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load_excel.setGeometry(QtCore.QRect(40, 10, 121, 31))
        self.btn_load_excel.setObjectName("btn_load_excel")        
        self.btn_load_excel.clicked.connect(lambda: self.no_name())

        self.btn_save_path = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save_path.setGeometry(QtCore.QRect(40, 60, 121, 31))
        self.btn_save_path.setObjectName("btn_save_path")
        self.btn_save_path.clicked.connect(lambda: self.no_name2())
        
        self.btn_run = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run.setGeometry(QtCore.QRect(180, 160, 121, 31))
        self.btn_run.setObjectName("btn_run")
        self.btn_run.clicked.connect(lambda: self.no_name3())

        self.lbl_output_file_name = QtWidgets.QLabel(self.centralwidget)
        self.lbl_output_file_name.setGeometry(QtCore.QRect(60, 110, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_output_file_name.setFont(font)
        self.lbl_output_file_name.setObjectName("lbl_output_file_name")


        self.tb_output_file_name = QtWidgets.QLineEdit(self.centralwidget)
        self.tb_output_file_name.setGeometry(QtCore.QRect(180, 110, 251, 31))
        self.tb_output_file_name.setObjectName("tb_output_file_name")        
                

        self.display_load_excel_path = QtWidgets.QTextEdit(self.centralwidget)
        self.display_load_excel_path.setGeometry(QtCore.QRect(180, 10, 251, 31))
        self.display_load_excel_path.setObjectName("load_excel_path")
        self.display_load_excel_path.setReadOnly(True)
        
        self.display_save_output_path = QtWidgets.QTextEdit(self.centralwidget)
        self.display_save_output_path.setGeometry(QtCore.QRect(180, 60, 251, 31))
        self.display_save_output_path.setObjectName("save_excel_path")
        self.display_save_output_path.setReadOnly(True)
                
        self.pbar_Run = QtWidgets.QProgressBar(self.centralwidget)
        self.pbar_Run.setGeometry(QtCore.QRect(60, 210, 361, 23))
        self.pbar_Run.setProperty("value", 0)
        self.pbar_Run.setObjectName("pbar_Run")
        
        MainWindow.setCentralWidget(self.centralwidget)


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 458, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.lbl_output_file_name.setText(_translate("MainWindow", "File Name :"))
        self.btn_load_excel.setText(_translate("MainWindow", "Load Excel"))
        self.btn_save_path.setText(_translate("MainWindow", "Save Path"))
        self.btn_run.setText(_translate("MainWindow", "Run"))


    def no_name(self):
        try:
            dialog = QtWidgets.QFileDialog()
            file_path = dialog.getOpenFileName(None, "Select File")
            self.banggood_csv = pd.read_csv(file_path[0])
            self.display_load_excel_path.setText(file_path[0])
        except:
            pass

    def no_name2(self):
        try:
            dialog = QtWidgets.QFileDialog()
            self.output_path = dialog.getExistingDirectory(None, "Select Folder")

            if ':' in self.output_path:
                index = self.output_path.index(':')
                self.output_path = self.output_path[index + 1:]

            self.output_path += '/'

            self.display_save_output_path.setText(self.output_path)
        except:
            pass


    def no_name3(self):

        if self.banggood_csv is None:
            self.error_excel.exec_()
        elif self.output_path is None:
            self.error_output_path.exec_()
        else:

            output_file_name = self.tb_output_file_name.text()

            if output_file_name == '':
                output_file_name = 'default'

            bd = BanggoodDescription(self.banggood_csv)

            # progress bar range of value : 0 - 100
            # init value from 0
            pbar_value = 0
            # max value
            pbar_max_value = 100

            # every step increment value
            pbar_step = int(pbar_max_value/len(bd))

            # final step increment value
            pbar_final_step = pbar_max_value % len(bd) + pbar_step

            for index in range(len(bd)):

                html = bd[index]
                parsed_data, stored_descriptions = bd.parse_html(html)

                cur_time = datetime.datetime.now()


                full_output_path = self.output_path + \
                f'{output_file_name}_{cur_time.year}-{cur_time.month}-{cur_time.day}_jam_{cur_time.hour}-{cur_time.minute}.csv'

                bd.export_to_banggood_csv(full_output_path, index = index, description = stored_descriptions)

                if index == len(bd) - 1:
                    pbar_value += pbar_final_step
                else:
                    pbar_value += pbar_step

                self.pbar_Run.setValue(pbar_value)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

