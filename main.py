import datetime
import re
import sys
import pymysql
import time
import codecs  # FOR ENCODING/DECODING

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from datetime import datetime as ddd
from itertools import count
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QPropertyAnimation, QSize, Qt)
from PyQt5.QtGui import (QColor, QFont, QPixmap)
from PyQt5.QtWidgets import *
from datetime import date
from PyQt5 import QtGui
from win10toast import ToastNotifier
from PyQt5.QtGui import QMovie

# GUI FILE
import file
from ui_styles import Style
from home import Ui_MainWindow
from login import Ui_login
from forgot import Ui_forgot
from signin import Ui_sigin
from splash import Ui_splash
from message import messages

counter = 0
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
toaster = ToastNotifier()


# {QtableWidget}.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
# {QtableWidget}.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

class Splash(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_splash()
        self.ui.setupUi(self)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setFixedSize(500, 300)
        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(20)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        self.shadow1.setColor(QColor(0, 0, 0, 100))
        self.ui.label_title.setGraphicsEffect(self.shadow1)

        # QTIMER START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # REMOVE FRAME
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # CHANGE DESCRIPTION
        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong>")

        # Change Texts
        QtCore.QTimer.singleShot(1400, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3200,
                                 lambda: self.ui.label_description.setText(
                                     "<strong>CONNECTING</strong> USER INTERFACE"))
        QtCore.QTimer.singleShot(4600, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USERS DATA"))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW LOGIN WINDOW
            self.loginpage = Login()
            self.loginpage.show()
            # print(datetime.now())

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1


class Login(QDialog, object):

    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.setFixedSize(800, 600)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.ui.logbtn.clicked.connect(self.logincheck)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.pushButton.clicked.connect(self.logintosignup)
        self.ui.pushButton_2.clicked.connect(self.loginforgot)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(20)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        self.shadow1.setColor(QColor(0, 0, 0, 80))
        self.ui.logbtn.setGraphicsEffect(self.shadow1)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(20)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QColor(0, 0, 0, 80))
        self.ui.label_5.setGraphicsEffect(self.shadow2)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(20)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QColor(0, 0, 0, 60))
        self.ui.pushButton.setGraphicsEffect(self.shadow3)
        ## ==> SET UI DEFINITIONS
        UIFunctions.minclose(self)

        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.frame_4.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def logincheck(self):
        username = self.ui.name.text()
        password = self.ui.password.text()
        # DATABASE CONNECTION
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql = "Select username,password from user where username = %s and password = %s"
        val = (username, password)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        database.commit()
        if username and password:
            if result:
                sql2 = "Select user_id from user where username = %s and password = %s"
                val2 = (username, password)
                cursor.execute(sql2, val2)
                Login.user = cursor.fetchone()  # FETCH VALUES
                database.close()
                # Mainwindow = MainWindow()
                # widget.addWidget(Mainwindow)
                # widget.setCurrentIndex(widget.currentIndex() + 1)
                self.mainWindow = MainWindow()
                self.mainWindow.show()
                self.close()  # CLOSE LOGIN PAGE
                return Login.user  # STORE USERID

            else:
                # playsound("C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav")
                Messageboxs.Warnings(self, 'User Not Found', 'Invalid Username And Password')
        else:
            Messageboxs.Warnings(self, 'Warning', 'Enter Username And Password')

    def logintosignup(self):
        # Using Widget Method to Call
        # signup = Signup()
        # QDialog.addWidget(signup)
        # widget.setCurrentIndex(widget.currentIndex() + 1)
        self.signinWindow = Signup()
        self.signinWindow.show()
        # Close Login Window
        self.close()

    def loginforgot(self):
        self.forgot = Pforgot()
        self.forgot.show()
        self.close()


class Messageboxs(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = messages()
        self.ui.setupUi(self)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        self.ui.pushpushpush.clicked.connect(self.closefunctions)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        UIFunctions.minclose(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.pushpushpush.setGraphicsEffect(self.shadow)

        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.frame.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    # FOR WARNING
    def Warnings(self, title, mess):  # TO FETCH TITLE AND MESSAGE AS PER REQUIREMENT
        self.message = Messageboxs()
        self.message.ui.label.setPixmap(QtGui.QPixmap(":/usedicon/images/used_icons/warning.png"))
        self.message.ui.label_3.setText(title)
        self.message.ui.label_2.setText(mess)
        self.message.show()

    # FOR CRITICAL
    def Critical(self, title, mess):
        self.message = Messageboxs()
        self.message.ui.label.setPixmap(QtGui.QPixmap(":/usedicon/images/used_icons/error.png"))
        self.message.ui.label_3.setText(title)
        self.message.ui.label_2.setText(mess)
        self.message.show()

    # FOR SUCESS
    def sucess(self, title, mess):
        self.message = Messageboxs()
        self.message.ui.label.setPixmap(QtGui.QPixmap(":/usedicon/images/used_icons/completed.png"))
        self.message.ui.label_3.setText(title)
        self.message.ui.label_2.setText(mess)
        self.message.show()

    # TO CLOSE MESSAGE BOX
    def closefunctions(self):
        self.close()


class Pforgot(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_forgot()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.forgottologin)
        self.ui.logbtn.clicked.connect(self.checkvalues)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        UIFunctions.minclose(self)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.ui.frame_3.setGraphicsEffect(self.shadow)
        self.shadow4 = QGraphicsDropShadowEffect(self)
        self.shadow4.setBlurRadius(20)
        self.shadow4.setXOffset(0)
        self.shadow4.setYOffset(0)
        self.shadow4.setColor(QColor(0, 0, 0, 80))
        self.ui.frame_2.setGraphicsEffect(self.shadow4)

        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(20)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        self.shadow1.setColor(QColor(0, 0, 0, 80))
        self.ui.logbtn.setGraphicsEffect(self.shadow1)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(20)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QColor(0, 0, 0, 80))
        self.ui.label_5.setGraphicsEffect(self.shadow2)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(20)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QColor(0, 0, 0, 60))
        self.ui.pushButton.setGraphicsEffect(self.shadow3)

        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.frame_4.mouseMoveEvent = moveWindow

    def forgottologin(self):
        self.loginWindow = Login()
        self.loginWindow.show()
        # Close Login Window
        self.close()

    def checkvalues(self):
        email = self.ui.name.text()
        password = self.ui.password.text()
        confirm = self.ui.password_2.text()
        match = re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)
        # DATABASE CONNECTION
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sqll = "select email from user where email= %s"
        vall = email
        cursor.execute(sqll, vall)
        data = cursor.fetchall()
        sqll1 = "select user_id from user where email= %s"
        cursor.execute(sqll1, vall)
        user = cursor.fetchall()
        database.commit()
        database.close()
        if email and password and confirm:
            if data:
                if self.ui.password.text() == self.ui.password_2.text():
                    if match is None:
                        Messageboxs.Warnings(self, 'Warning', 'Email is invalid')

                    else:
                        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
                        cursor = database.cursor()
                        sql = "UPDATE user SET password=%s WHERE user_id=%s"
                        val = (password, user)
                        cursor.execute(sql, val)
                        database.commit()
                        database.close()
                        self.loginWindow = Login()
                        self.loginWindow.show()
                        self.close()

                else:
                    # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
                    Messageboxs.Warnings(self, 'Warning', 'password and confirm password  should be same')

            else:
                Messageboxs.Warnings(self, 'Warning', 'Email doesnt exists')

        else:
            # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
            Messageboxs.Critical(self, 'Error', 'Enter all the details')


class Signup(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_sigin()
        self.ui.setupUi(self)
        self.ui.logbtn.clicked.connect(self.signupcheck)
        self.ui.pushButton.clicked.connect(self.signuptologin)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(20)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        self.shadow1.setColor(QColor(0, 0, 0, 80))
        self.ui.logbtn.setGraphicsEffect(self.shadow1)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(20)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QColor(0, 0, 0, 80))
        self.ui.label_5.setGraphicsEffect(self.shadow2)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(20)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QColor(0, 0, 0, 60))
        self.ui.pushButton.setGraphicsEffect(self.shadow3)
        ## ==> SET UI DEFINITIONS
        UIFunctions.minclose(self)

        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.frame_4.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def signupcheck(self):
        email = self.ui.name_2.text()
        username = self.ui.name.text()
        password = self.ui.password.text()
        confirm = self.ui.password_2.text()
        # REGRESSION
        match = re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)
        # DATABASE CONNECTION
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sqll = "select email from user where email= %s"
        vall = email
        cursor.execute(sqll, vall)
        data = cursor.fetchall()
        database.commit()
        database.close()
        if email and password and confirm and username:
            if not data:
                if len(username) > 4:
                    if self.ui.password.text() == self.ui.password_2.text():
                        if match is None:
                            # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
                            Messageboxs.Warnings(self, 'Warning', 'Email is invalid')

                        else:
                            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
                            cursor = database.cursor()
                            sql = "INSERT INTO user (email,username,password) VALUES (%s, %s, %s)"
                            val = (email, username, password)
                            cursor.execute(sql, val)
                            database.commit()
                            database.close()
                            self.loginWindow = Login()
                            self.loginWindow.show()
                            self.close()

                    else:
                        # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
                        Messageboxs.Warnings(self, 'Warning', 'password and confirm password  should be same')

                else:
                    # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
                    Messageboxs.Warnings(self, 'Warning', 'Username should be grater than 4 letter')

            else:
                # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/wrong.wav')
                Messageboxs.Critical(self, 'Error', 'Email already exists enter another email')
        else:
            Messageboxs.Warnings(self, 'Warning', 'Enter all the details')

    # def Critical(self, title, message):
    #     msgBox = QMessageBox()
    #     msgBox.setIcon(QMessageBox.Critical)
    #     msgBox.setWindowTitle(title)
    #     msgBox.setText(message)
    #     msgBox.setStandardButtons(QMessageBox.Ok)
    #     msgBox.exec_()
    #
    # def Warning(self, title, message):
    #     msgBox = QMessageBox()
    #     msgBox.setIcon(QMessageBox.Warning)
    #     msgBox.setWindowTitle(title)
    #     msgBox.setText(message)
    #     msgBox.setStandardButtons(QMessageBox.Ok)
    #     # msgBox.setStyleSheet(
    #     #     "QMainWindow {background-color: white;} QWidget{ color: white; background-color: Black;} QPushButton{"
    #     #     "background-color: rgb(255, 200, 1);color: black; } QLabel{font: 75 12pt 'High Tower Text';}")
    #     msgBox.exec_()

    def signuptologin(self):
        self.loginWindow = Login()
        self.loginWindow.show()
        # Close Login Window
        self.close()


import ast


def Myconverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)
        except Exception:
            return str(data)

    return tuple(map(cvt, mydata))


class bar_i_e(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(20, 5.5), dpi=55)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        self.setStyleSheet("background-color:transparent;")
        self.plot()

    def plot(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        userid = Login.user
        sql = "SELECT y, m FROM (SELECT y, m FROM(SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) " \
              "years,(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT " \
              "6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
              "SELECT 12) months) ym LEFT JOIN expense ON ym.y = YEAR(date)AND ym.m = MONTH(date)WHERE user_id=%s AND(" \
              "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE()))OR(y<YEAR(CURDATE()) AND m>MONTH(CURDATE()))GROUP BY y, m "
        cursor.execute(sql, userid)
        yearmonth = cursor.fetchall()
        sql1 = "SELECT sum(amount) FROM ( SELECT y, m FROM (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years, " \
               "(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 " \
               "UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
               "SELECT 12) months) ym LEFT JOIN expense ON ym.y = YEAR(date) AND ym.m = MONTH(date) WHERE user_id=%s AND (" \
               "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) GROUP BY y, m "
        cursor.execute(sql1, userid)
        expense = [i[0] for i in cursor.fetchall()]
        sql2 = "SELECT SUM(amount) FROM ( SELECT y, m FROM (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) " \
               "years, " \
               "(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 " \
               "UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
               "SELECT 12) months) ym LEFT JOIN income ON ym.y = YEAR(date) AND ym.m = MONTH(date) WHERE user_id= %s AND (" \
               "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) GROUP BY y, m "
        cursor.execute(sql2, userid)
        income = [i[0] for i in cursor.fetchall()]
        if len(income) < 11:
            if len(expense) < 11:
                self.ax.set_title("At least 12 months data is required to display this graph", fontsize=20)
            else:
                self.ax.set_title("At least 12 months data is required to display this graph", fontsize=20)
        else:
            barWidth = 0.2

            # Set position of bar on X axis
            br1 = np.arange(len(income))
            br2 = [x + barWidth for x in br1]

            # Make the plot
            plt.bar(br1, expense, color='deeppink', width=barWidth,
                    edgecolor='grey', label='Expense')
            plt.bar(br2, income, color='blueviolet', width=barWidth,
                    edgecolor='grey', label='Income')
            plt.xticks(fontsize=14)
            # Adding Xticks
            plt.ylabel('Rs', fontweight='bold', fontsize=14)
            plt.xticks([r + barWidth for r in range(len(income))], yearmonth, fontsize=12)
            # plt.yticks(fontsize=14)
            plt.legend(loc='upper right', frameon=False, fontsize=12)
            right_side = self.ax.spines["right"]
            right_side.set_visible(False)
            top_side = self.ax.spines["top"]
            top_side.set_visible(False)


class bar_i_e1(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(15, 4), dpi=55)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        self.setStyleSheet("background-color:transparent;")
        self.plot()

    def plot(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        userid = Login.user
        sql = "SELECT y, m FROM (SELECT y, m FROM(SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) " \
              "years,(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT " \
              "6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
              "SELECT 12) months) ym LEFT JOIN expense ON ym.y = YEAR(date)AND ym.m = MONTH(date)WHERE user_id=%s AND(" \
              "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE()))OR(y<YEAR(CURDATE()) AND m>MONTH(CURDATE()))GROUP BY y, m "
        cursor.execute(sql, userid)
        yearmonth = cursor.fetchall()
        sql1 = "SELECT sum(amount) FROM ( SELECT y, m FROM (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years, " \
               "(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 " \
               "UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
               "SELECT 12) months) ym LEFT JOIN expense ON ym.y = YEAR(date) AND ym.m = MONTH(date) WHERE user_id=%s AND (" \
               "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) GROUP BY y, m "
        cursor.execute(sql1, userid)
        expense = [i[0] for i in cursor.fetchall()]
        sql2 = "SELECT SUM(amount) FROM ( SELECT y, m FROM (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) " \
               "years, " \
               "(SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 " \
               "UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL " \
               "SELECT 12) months) ym LEFT JOIN income ON ym.y = YEAR(date) AND ym.m = MONTH(date) WHERE user_id= %s AND (" \
               "y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) GROUP BY y, m "
        cursor.execute(sql2, userid)
        income = [i[0] for i in cursor.fetchall()]
        if len(income) < 11:
            if len(expense) < 11:
                self.ax.set_title("At least 12 months data is required to display this graph", fontsize=20)
            else:
                self.ax.set_title("At least 12 months data is required to display this graph", fontsize=20)
        else:
            barWidth = 0.2

            # Set position of bar on X axis
            br1 = np.arange(len(income))
            br2 = [x + barWidth for x in br1]
            # Make the plot
            plt.bar(br1, expense, color='deeppink', width=barWidth,
                    edgecolor='grey', label='Expense')
            plt.bar(br2, income, color='blueviolet', width=barWidth,
                    edgecolor='grey', label='Income')

            # Adding Xticks
            plt.ylabel('Rs', fontweight='bold', fontsize=14)
            plt.xticks([r + barWidth for r in range(len(income))], yearmonth, fontsize=12)
            # plt.yticks(fontsize=14)
            plt.legend(loc='upper right', frameon=False, fontsize=12)
            right_side = self.ax.spines["right"]
            right_side.set_visible(False)
            top_side = self.ax.spines["top"]
            top_side.set_visible(False)


class bargraph(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(8.9, 4.5), dpi=50)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        self.setStyleSheet("background-color:transparent;")
        self.plot()

    def plot(self):
        userid = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql1 = "Select category from expense where MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE()) AND  user_id = %s ORDER BY date DESC LIMIT 5"
        val = userid
        cursor.execute(sql1, val)
        x1 = [i[0][:7] for i in cursor.fetchall()]
        sql = "Select amount from expense where MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE()) AND  user_id = %s ORDER BY date DESC LIMIT 5"
        val1 = userid
        cursor.execute(sql, val1)
        y1 = [i[0] for i in cursor.fetchall()]
        database.close()
        if len(y1) < 5:
            self.ax.set_title("Add at least  5 Expense", fontsize=20)
        else:
            width = 0.5
            ind = np.arange(len(y1))  # the x locations for the groups
            self.ax.barh(ind, y1, width, color="mediumslateblue")
            self.ax.set_yticks(ind + width / 2)
            self.ax.set_yticklabels(x1, minor=False, fontsize=14)
            self.ax.set_title("Top 5 Expense", fontsize=20)
            right_side = self.ax.spines["right"]
            right_side.set_visible(False)
            for i, v in enumerate(y1):
                self.ax.text(v + 100, i, str(v), color='black', fontweight='bold', fontsize=14, ha='left', va='center')


class piechart(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(4, 4), dpi=55)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        self.setStyleSheet("background-color:transparent;")
        self.plo()

    def plo(self):
        userid = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql1 = "SELECT category FROM expense WHERE MONTH(date) = MONTH(CURDATE())AND YEAR(date) = YEAR(CURDATE()) AND user_id = %s ORDER BY date DESC LIMIT 5"
        val = userid
        cursor.execute(sql1, val)
        category = [i[0] for i in cursor.fetchall()]
        sql = "SELECT amount FROM expense WHERE MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE()) AND user_id = %s ORDER BY date DESC LIMIT 5"
        val1 = userid
        cursor.execute(sql, val1)
        datax = [i[0] for i in cursor.fetchall()]
        database.close()
        if len(datax) < 5:
            self.ax.set_title("Add at least 5 Expense", fontsize=16)

        else:
            # 'Aquamarine', 'SkyBlue',
            colors = ['Mediumorchid', 'darkorchid', 'darkviolet', 'violet', 'plum']
            explode = (0, 0, 0.1, 0, 0.1)  # explode 1st slice
            self.ax.pie(datax, explode=explode, colors=colors, pctdistance=0.50, startangle=0)
            # draw circle autopct='%1.1f%%'
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)  # Equal aspect ratio ensures that pie is drawn as a circle
            self.ax.axis('equal')
            self.ax.set_title("Top 5 Expense", fontsize=16)
            plt.legend(category, loc="center")
            plt.tight_layout()


#         colors = ['MediumPurple', 'RoyalBlue', 'Purple', 'Blue', 'Indigo', 'MidnightBlue']
#         self.ax.pie(data, labels=category, colors=colors, autopct='%1.1f%%', pctdistance=0.50, startangle=90)
#         # draw circle
#         centre_circle = plt.Circle((0, 0), 0.70, fc='white')
#         fig = plt.gcf()
#         fig.gca().add_artist(centre_circle)  # Equal aspect ratio ensures that pie is drawn as a circle
#         self.ax.axis('equal')
#         # self.ax.set_title("Top monthly income", fontsize=16)
#         plt.tight_layout()


class line_net(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(15, 4), dpi=55)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        # set the seaborn style
        # sns.set_style("whitegrid")
        self.setStyleSheet("background-color:transparent;")
        self.plot()

    def plot(self):
        # SELECT monthname(date) FROM `expense` WHERE date > DATE_SUB(now(), INTERVAL 6 MONTH)AND category='savings' AND user_id='%s'
        userid = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql = "select day(Date) from expense where month(Date) = month(NOW()) and year(Date) = year(NOW())AND user_id=%s group by day(Date)"
        val = userid
        cursor.execute(sql, val)
        day = [i[0] for i in cursor.fetchall()]
        sql1 = "select sum(amount) from expense where month(Date) = month(NOW()) and year(Date) = year(NOW())AND user_id=%s group by day(Date)"
        val1 = userid
        cursor.execute(sql1, val1)
        amount = [i[0] for i in cursor.fetchall()]
        if len(amount) < 1:
            self.ax.set_title("Add few data in expense to display this graph", fontsize=20)
        else:
            plt.ylabel('Rs', fontweight='bold', fontsize=14)
            plt.yticks(fontsize=14)
            plt.xticks(fontsize=14)
            plt.plot(day, amount, color='blue', linestyle='dashed', linewidth=3,
                     marker='o', markerfacecolor='purple', markersize=12)
            right_side = self.ax.spines["right"]
            right_side.set_visible(False)
            top_side = self.ax.spines["top"]
            top_side.set_visible(False)


class linegraph(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(8, 4), dpi=55)
        super().__init__(fig)
        self.setParent(parent)
        fig.patch.set_visible(False)
        # set the seaborn style
        # sns.set_style("whitegrid")
        self.setStyleSheet("background-color:transparent;")
        self.plot()

    def plot(self):
        # SELECT monthname(date) FROM `expense` WHERE date > DATE_SUB(now(), INTERVAL 6 MONTH)AND category='savings' AND user_id='%s'
        userid = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql1 = "SELECT amount FROM `expense` WHERE user_id='%s' AND description='Savings' ORDER BY date"
        val = userid
        cursor.execute(sql1, val)
        category = [i[0] for i in cursor.fetchall()]
        sql = "SELECT monthname(date) FROM `expense` WHERE user_id='%s' AND description='Savings' ORDER BY date"
        val1 = userid
        cursor.execute(sql, val1)
        datax = [i[0] for i in cursor.fetchall()]
        if len(datax) < 1:
            self.ax.set_title("Enter Monthly Savings to display this Graph", fontsize=16)
        else:
            # Make the plot
            self.ax.plot(datax, category, color='darkorchid', lw=2)
            self.ax.fill_between(datax, 0, category, color='plum')
            self.ax.set(xlim=(0, len(datax) - 1), ylim=(0, None), xticks=datax)
            plt.yticks(fontsize=14)
            plt.xticks(fontsize=14)
            self.ax.set_title("Savings Graph", fontsize=16)
            for spine in self.ax.spines:
                self.ax.spines[spine].set_visible(False)


class MainWindow(QMainWindow, Login):
    # SELECT date, category, description, source, amount FROM expense WHERE user_id = %s ORDER BY date DESC LIMIT 5
    def loadData(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT date, category, source, description, note, amount,income_id FROM income where user_id = %s order by year(date) DESC ,month(date) DESC, day(date) DESC "
        val = Login.user
        cur.execute(sql, val)
        data = cur.fetchall()

        for row in data:
            self.addTable(Myconverter(row))
        database.close()

    def addTable(self, columns):
        rowPosition = self.ui.tableWidget_6.rowCount()
        self.ui.tableWidget_6.insertRow(rowPosition)

        for i, column in enumerate(columns):
            self.ui.tableWidget_6.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))
            self.btn_sell = QtWidgets.QPushButton()
            self.btn_sell.clicked.connect(self.deleteClicked)
            self.ui.tableWidget_6.setColumnWidth(0, 100)
            self.ui.tableWidget_6.setColumnWidth(1, 100)
            self.ui.tableWidget_6.setColumnWidth(2, 100)
            self.ui.tableWidget_6.setColumnWidth(3, 125)
            self.ui.tableWidget_6.setColumnWidth(4, 200)
            self.ui.tableWidget_6.setColumnWidth(5, 100)
            self.btn_sell.setStyleSheet(
                "QPushButton {background-image: url(:/usedicon/images/used_icons/deleteb.png);\n"
                "    background-repeat: no-reperat;\n"
                "    background-position: center;}")
            self.btn_sell.setMinimumSize(QtCore.QSize(60, 30))
            self.btn_sell.setMaximumSize(QtCore.QSize(60, 30))
            self.ui.tableWidget_6.setCellWidget(rowPosition, 7, self.btn_sell)
            self.ui.tableWidget_6.hideColumn(6)

    def deleteClicked(self, Col=0):
        button = self.sender()
        index = self.ui.tableWidget_6.indexAt(button.pos())
        if button:
            row = self.ui.tableWidget_6.indexAt(button.pos()).row()
            # self.ui.tableWidget_2.removeRow(row)
            # print(index.row(),index.column()+1)

            x = self.ui.tableWidget_6.item(row, Col + 6)
            hiddenvalue = str(x.text())
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()
            sql1 = "DELETE FROM income WHERE income_id= %s"
            cur.execute(sql1, (hiddenvalue,))
            database.commit()
            self.ui.tableWidget_6.removeRow(row)
            # Update
            MainWindow.eandi(self)
            MainWindow.cashprogressBarValue(self)
            toaster.show_toast('Deleted Data', 'Successfully', duration=10,
                               icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/delete.ico',
                               threaded=True)

    # def remove_row_all_table(self, table_widget):

    def loadData1(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT date, category, source, description, note, amount,expense_id FROM expense where user_id = %s order by year(date) DESC ,month(date) DESC, day(date) DESC "
        val = Login.user
        cur.execute(sql, val)
        data = cur.fetchall()

        for row in data:
            self.addTable1(Myconverter(row))
        cur.close()

    def addTable1(self, columns):
        rowPosition = self.ui.tableWidget_5.rowCount()
        self.ui.tableWidget_5.insertRow(rowPosition)

        for i, column in enumerate(columns):
            self.ui.tableWidget_5.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))
            self.btn_sell = QtWidgets.QPushButton()
            self.btn_sell.clicked.connect(self.deleteClicked1)
            self.ui.tableWidget_5.setColumnWidth(0, 100)
            self.ui.tableWidget_5.setColumnWidth(1, 100)
            self.ui.tableWidget_5.setColumnWidth(2, 100)
            self.ui.tableWidget_5.setColumnWidth(3, 125)
            self.ui.tableWidget_5.setColumnWidth(4, 200)
            self.ui.tableWidget_5.setColumnWidth(5, 100)
            self.btn_sell.setStyleSheet(
                "QPushButton {background-image: url(:/usedicon/images/used_icons/deleteb.png);\n"
                "    background-repeat: no-reperat;\n"
                "    background-position: center;}")
            self.btn_sell.setMinimumSize(QtCore.QSize(60, 30))
            self.btn_sell.setMaximumSize(QtCore.QSize(60, 30))
            self.ui.tableWidget_5.setCellWidget(rowPosition, 7, self.btn_sell)
            self.ui.tableWidget_5.hideColumn(6)

    def deleteClicked1(self, Col=0):
        button = self.sender()
        index = self.ui.tableWidget_5.indexAt(button.pos())
        if button:
            row = self.ui.tableWidget_5.indexAt(button.pos()).row()
            # self.ui.tableWidget_2.removeRow(row)
            # print(index.row(),index.column()+1)
            x = self.ui.tableWidget_5.item(row, Col + 6)
            hidvalue = str(x.text())
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()
            sql1 = "DELETE FROM expense WHERE expense_id= %s"
            cur.execute(sql1, (hidvalue,))
            database.commit()
            self.ui.tableWidget_5.removeRow(row)
            # Update
            MainWindow.eandi(self)
            MainWindow.cashprogressBarValue(self)
            toaster.show_toast('Deleted Data', 'Successfully', duration=10,
                               icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/delete.ico',
                               threaded=True)

    def loadData2(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT date,category,title,message,notification_id FROM notification where user_id = %s order by date DESC"
        val = Login.user
        cur.execute(sql, val)
        data = cur.fetchall()
        for row in data:
            self.addTable2(Myconverter(row))
        return data

    def addTable2(self, columns):
        rowPosition = self.ui.tableWidget_3.rowCount()
        self.ui.tableWidget_3.insertRow(rowPosition)

        for i, column in enumerate(columns):
            self.ui.tableWidget_3.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))
            self.btn_sell = QtWidgets.QPushButton()
            self.btn_sell.clicked.connect(self.deleteClicked2)
            self.ui.tableWidget_3.setColumnWidth(0, 140)
            # self.ui.tableWidget.setColumnWidth(1, 100)
            # self.ui.tableWidget.setColumnWidth(2, 100)
            # self.ui.tableWidget.setColumnWidth(3, 125)
            # self.ui.tableWidget.setColumnWidth(4, 200)
            # self.ui.tableWidget.setColumnWidth(5, 100)
            self.btn_sell.setStyleSheet(
                "QPushButton {background-image: url(:/usedicon/images/used_icons/deleteb.png);\n"
                "    background-repeat: no-reperat;\n"
                "    background-position: center;}")
            self.btn_sell.setMinimumSize(QtCore.QSize(60, 30))
            self.btn_sell.setMaximumSize(QtCore.QSize(60, 30))
            self.ui.tableWidget_3.setCellWidget(rowPosition, 5, self.btn_sell)
            self.ui.tableWidget_3.hideColumn(4)

    def deleteClicked2(self, Col=0):
        button = self.sender()
        index = self.ui.tableWidget_3.indexAt(button.pos())
        if button:
            row = self.ui.tableWidget_3.indexAt(button.pos()).row()
            # self.ui.tableWidget_2.removeRow(row)
            # print(index.row(),index.column()+1)
            x = self.ui.tableWidget_3.item(row, Col + 4)
            hidvalue = str(x.text())
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()
            sql1 = "DELETE FROM notification WHERE notification_id= %s"
            cur.execute(sql1, (hidvalue,))
            database.commit()
            self.ui.tableWidget_3.removeRow(row)
            toaster.show_toast('Deleted Data', 'Successfully', duration=10,
                               icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/delete.ico',
                               threaded=True)

    def loadData3(self):  # TO LOAD BUDGET INSIDE QTABLEWIDGET
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT month,year,category,description,amount,budget_id FROM budget where user_id = %s"
        val = Login.user
        cur.execute(sql, val)
        data = cur.fetchall()
        for row in data:
            self.addTable3(Myconverter(row))
        return data

    def addTable3(self, columns):
        rowPosition = self.ui.tableWidget_4.rowCount()
        self.ui.tableWidget_4.insertRow(rowPosition)  # INSERTING ROW WISE

        for i, column in enumerate(columns):
            self.ui.tableWidget_4.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))
            self.btn_sell = QtWidgets.QPushButton()
            self.btn_sell.clicked.connect(self.deleteClicked3)
            self.ui.tableWidget_4.setColumnWidth(0, 100)  # STTING COLUMS WIDTH
            self.btn_sell.setStyleSheet(
                "QPushButton {background-image: url(:/usedicon/images/used_icons/deleteb.png);\n"
                "    background-repeat: no-reperat;\n"
                "    background-position: center;}")
            self.btn_sell.setMinimumSize(QtCore.QSize(60, 30))
            self.btn_sell.setMaximumSize(QtCore.QSize(60, 30))
            self.ui.tableWidget_4.setCellWidget(rowPosition, 7, self.btn_sell)
            self.btn_check = QtWidgets.QPushButton()
            self.btn_check.clicked.connect(self.checkClicked)  # CREATING A DELETE BUTTON ON EACH ROW
            # self.ui.tableWidget_4.setColumnWidth(0, 140)
            self.btn_check.setStyleSheet(
                "QPushButton {background-image: url(:/usedicon/images/used_icons/check.png);\n"
                "    background-repeat: no-reperat;\n"
                "    background-position: center;}")
            self.btn_check.setMinimumSize(QtCore.QSize(60, 30))
            self.btn_check.setMaximumSize(QtCore.QSize(60, 30))
            self.ui.tableWidget_4.setCellWidget(rowPosition, 6, self.btn_check)
            self.ui.tableWidget_4.hideColumn(5)  # HIDING A COLUMN

    def deleteClicked3(self, Col=0):
        button = self.sender()
        self.ui.tableWidget_4.indexAt(button.pos())
        if button:
            row = self.ui.tableWidget_4.indexAt(button.pos()).row()
            x = self.ui.tableWidget_4.item(row, Col + 5)
            hidvalue = str(x.text())
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()
            sql1 = "DELETE FROM budget WHERE budget_id= %s"
            cur.execute(sql1, (hidvalue,))
            database.commit()
            self.ui.tableWidget_4.removeRow(row)  # REMOVE THE SELECTED ROW
            toaster.show_toast('Deleted Data', 'Successfully', duration=10,
                               icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/delete.ico',
                               threaded=True)

    def checkClicked(self, Col=0):
        button = self.sender()
        self.ui.tableWidget_4.indexAt(button.pos())
        if button:
            row = self.ui.tableWidget_4.indexAt(button.pos()).row()
            x = self.ui.tableWidget_4.item(row, Col + 5)
            hidvalue = str(x.text())
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()

            # 1
            sqll = "SELECT amount from budget WHERE budget_id=%s"
            cur.execute(sqll, hidvalue)
            amount = cur.fetchone()
            y1 = ''.join(str(y1) for y1 in amount)
            am1 = int(y1)
            self.ui.label.setText("TARGET AMOUNT = " + str(am1))

            # 2
            one = "SELECT month,year,category,description,user_id FROM budget WHERE budget_id=%s"
            cur.execute(one, hidvalue)
            allvalues = cur.fetchone()

            # 3
            user = Login.user
            sql2 = "SELECT amount FROM expense WHERE MONTH(date) = %s AND YEAR(date) = %s and category=%s and description=%s and user_id=%s"
            cur.execute(sql2, allvalues)
            amounts = cur.fetchone()
            if amounts is None:
                self.ui.label_60.setText("NO data available!!!!!! ")
                self.ui.label_61.setText("")
            else:
                y2 = ''.join(str(y2) for y2 in amounts)
                am2 = int(y2)
                self.ui.label_60.setText("EXPENSE = " + str(am2))
                final = int(am1 - am2)
                self.ui.label_61.setText("BALANCE = " + str(final))

    def combo_input(self):
        val = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()

        sqll = "select DISTINCT(month(date)) as Month from expense WHERE user_id=%s ORDER BY month ASC "
        cur.execute(sqll, val)
        Month = [i[0] for i in cur.fetchall()]
        for i in Month:
            self.ui.comboBox_20.addItem(str(i))
            self.ui.comboBox_28.addItem(str(i))

        sqlll = "select  DISTINCT(year(date)) as year from expense WHERE user_id=%s ORDER BY `year` ASC "
        cur.execute(sqlll, val)
        Year = [i[0] for i in cur.fetchall()]
        for i in Year:
            self.ui.comboBox_21.addItem(str(i))
            self.ui.comboBox_29.addItem(str(i))

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        # SETTING UP COMBOBOX
        self.model = QStandardItemModel()
        self.ui.comboBox_10.setModel(self.model)
        self.ui.comboBox_11.setModel(self.model)
        for k, v in data.items():
            state = QStandardItem(k)
            self.model.appendRow(state)
            for value in v:
                city = QStandardItem(value)
                state.appendRow(city)
        self.ui.comboBox_10.currentIndexChanged.connect(self.updateStateCombo)
        self.updateStateCombo(0)

        self.modell = QStandardItemModel()
        self.ui.comboBox_18.setModel(self.modell)
        self.ui.comboBox_19.setModel(self.modell)
        for k, v in data.items():
            state = QStandardItem(k)
            self.modell.appendRow(state)
            for value in v:
                city = QStandardItem(value)
                state.appendRow(city)
        self.ui.comboBox_18.currentIndexChanged.connect(self.updateStateCombox)
        self.updateStateCombox(0)

        self.mode = QStandardItemModel()
        self.ui.comboBox_26.setModel(self.mode)
        self.ui.comboBox_27.setModel(self.mode)
        for k, v in data.items():
            state = QStandardItem(k)
            self.mode.appendRow(state)
            for value in v:
                city = QStandardItem(value)
                state.appendRow(city)
        self.ui.comboBox_26.currentIndexChanged.connect(self.updateStateCombox1)
        self.updateStateCombox1(0)
        # DATE AND TIME
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateEdit_5.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateEdit_4.setDateTime(QtCore.QDateTime.currentDateTime())

        # START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)

        # MOVE WINDOW
        def moveWindow(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # Page 1
        self.ui.frame_top_right.mouseMoveEvent = moveWindow
        canvas = bargraph(self.ui.bar)
        canvas1 = piechart(self.ui.pie1)
        # self.piechart()
        canvas3 = linegraph(self.ui.line)
        # PAGE 5

        canvas5 = line_net(self.ui.net_worth)
        # REMOVE TITLE BAR

        ## ==> SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)
        # MainWindow.expprogress(self)
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 160, True))
        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        MainWindow.addNewMenu(self, "DASHBOARD", "btn_home", "url(:/usedicon/images/used_icons/home.png)", True)
        MainWindow.addNewMenu(self, "TRANSACTION", "btn_trans", "url(:/usedicon/images/used_icons/transactoion.png)",
                              True)
        MainWindow.addNewMenu(self, "BUDGET", "btn_budget", "url(:/usedicon/images/used_icons/wallet.png)", True)
        MainWindow.addNewMenu(self, "EXPORT/EDIT", "btn_editor", "url(:/usedicon/images/used_icons/editor.png)", True)
        MainWindow.addNewMenu(self, "NOTIFICATION", "btn_notify", "url(:/usedicon/images/used_icons/notification.png)",
                              True)
        MainWindow.addNewMenu(self, "GRAPH", "btn_graph", "url(:/usedicon/images/used_icons/graph.png)", True)
        MainWindow.addNewMenu(self, "TRACK", "btn_track", "url(:/usedicon/images/used_icons/tracking.png)", True)
        MainWindow.addNewMenu(self, "TOOLS", "btn_tools", "url(:/usedicon/images/used_icons/tools.png)",
                              True)
        MainWindow.addNewMenu(self, "ABOUT US", "btn_aboutus", "url(:/usedicon/images/used_icons/aboutus.png)", False)
        ## ==> END ##
        # START MENU => SELECTION
        MainWindow.selectStandardMenu(self, "btn_home")
        ## ==> END ##
        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_5))
        self.ui.name_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.name_5.setEchoMode(QtWidgets.QLineEdit.Password)
        MainWindow.userprofile(self)
        self.ui.pushButton_6.clicked.connect(self.editprofile)
        self.ui.pushButton_5.clicked.connect(self.editimage)
        MainWindow.cashprogressBarValue(self)
        # self.cardprogressBarValue(25)
        MainWindow.loadData1(self)
        MainWindow.loadData(self)
        MainWindow.loadData2(self)
        MainWindow.loadData3(self)
        MainWindow.eandi(self)
        MainWindow.combo_input(self)

        # PAGE 2
        # self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        # Sub PAGE 1
        self.ui.Done_4.clicked.connect(lambda: self.expe())
        # Sub PAGE 2
        self.ui.Done_5.clicked.connect(lambda: self.inc())

        # self.ui.expenditure.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.Page2of1))
        # self.ui.income.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.Page2of2))
        # PAGE 3
        self.ui.create.clicked.connect(self.notificationpage)
        # PAGE 4
        self.ui.create_2.clicked.connect(self.budget)
        self.ui.create_4.clicked.connect(self.trackexpense)
        # Page5
        # x= self.showMaximized()

        # if x:
        #     canvas4 = bar_i_e(self.ui.ie_per_month)
        # else:
        #     canvas4 = bar_i_e1(self.ui.ie_per_month)
        canvas4 = bar_i_e1(self.ui.ie_per_month)

        # canvas4 = bar_i_e(self.ui.ie_per_month)
        # PAGE 6
        self.ui.pushButton_13.clicked.connect(lambda: self.file_open())
        self.ui.pushButton_8.clicked.connect(lambda: self.file_save())
        self.ui.pushButton_7.clicked.connect(lambda: self.file_saveas())
        self.ui.pushButton_14.clicked.connect(lambda: self.ui.plainTextEdit.redo())
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.plainTextEdit.undo())
        self.ui.pushButton_10.clicked.connect(lambda: self.ui.plainTextEdit.cut())
        self.ui.pushButton_11.clicked.connect(lambda: self.ui.plainTextEdit.copy())
        self.ui.pushButton_12.clicked.connect(lambda: self.ui.plainTextEdit.paste())

        # EXEL
        # self.ui.radioButton.setChecked(True)
        self.ui.create_3.clicked.connect(self.export)

        # PAGE 7
        # self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentWidget(self.ui.cal))
        # self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentWidget(self.ui.emi))
        self.ui.pushButton_4.clicked.connect(self.emi_calculate)
        # basic calci
        self.ui.push_1.clicked.connect(self.method_1)
        self.ui.push_2.clicked.connect(self.method_2)
        self.ui.push_3.clicked.connect(self.method_3)
        self.ui.push_4.clicked.connect(self.method_4)
        self.ui.push_5.clicked.connect(self.method_5)
        self.ui.push_6.clicked.connect(self.method_6)
        self.ui.push_7.clicked.connect(self.method_7)
        self.ui.push_8.clicked.connect(self.method_8)
        self.ui.push_9.clicked.connect(self.method_9)
        self.ui.push_zero.clicked.connect(self.method_zero)
        self.ui.push_point.clicked.connect(self.method_point)
        self.ui.push_plus.clicked.connect(self.method_plus)
        self.ui.push_min.clicked.connect(self.method_min)
        self.ui.push_mult.clicked.connect(self.method_mult)
        self.ui.push_div.clicked.connect(self.method_div)
        self.ui.push_equal.clicked.connect(self.method_equal)
        self.ui.push_clear.clicked.connect(self.method_clear)
        self.ui.push_del.clicked.connect(self.method_del)

        self.onlyInt = QIntValidator()
        # self.ui.lineEdit_2.setValidator(self.onlyInt)
        self.ui.lineEdit_4.setValidator(self.onlyInt)
        self.ui.lineEdit_5.setValidator(self.onlyInt)
        self.ui.lineEdit_6.setValidator(self.onlyInt)
        self.ui.lineEdit_7.setValidator(self.onlyInt)
        self.ui.lineEdit_19.setValidator(self.onlyInt)
        # self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

        # SET DROPSHADOW WINDOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        # APPLY DROPSHADOW TO FRAME
        self.ui.one.setGraphicsEffect(self.shadow)

        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(20)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        self.shadow1.setColor(QColor(0, 0, 0, 100))
        self.ui.three.setGraphicsEffect(self.shadow1)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(20)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QColor(0, 0, 0, 100))
        self.ui.four.setGraphicsEffect(self.shadow2)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(20)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QColor(0, 0, 0, 100))
        self.ui.four.setGraphicsEffect(self.shadow3)

        self.shadow4 = QGraphicsDropShadowEffect(self)
        self.shadow4.setBlurRadius(20)
        self.shadow4.setXOffset(0)
        self.shadow4.setYOffset(0)
        self.shadow4.setColor(QColor(0, 0, 0, 100))
        self.ui.cash_card.setGraphicsEffect(self.shadow4)

        self.shadow5 = QGraphicsDropShadowEffect(self)
        self.shadow5.setBlurRadius(20)
        self.shadow5.setXOffset(0)
        self.shadow5.setYOffset(0)
        self.shadow5.setColor(QColor(0, 0, 0, 100))
        self.ui.balance.setGraphicsEffect(self.shadow5)

        self.shadow6 = QGraphicsDropShadowEffect(self)
        self.shadow6.setBlurRadius(20)
        self.shadow6.setXOffset(0)
        self.shadow6.setYOffset(0)
        self.shadow6.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_15.setGraphicsEffect(self.shadow6)

        self.shadow7 = QGraphicsDropShadowEffect(self)
        self.shadow7.setBlurRadius(20)
        self.shadow7.setXOffset(0)
        self.shadow7.setYOffset(0)
        self.shadow7.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_62.setGraphicsEffect(self.shadow7)

        self.shadow8 = QGraphicsDropShadowEffect(self)
        self.shadow8.setBlurRadius(20)
        self.shadow8.setXOffset(0)
        self.shadow8.setYOffset(0)
        self.shadow8.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_20.setGraphicsEffect(self.shadow8)

        self.shadow9 = QGraphicsDropShadowEffect(self)
        self.shadow9.setBlurRadius(20)
        self.shadow9.setXOffset(0)
        self.shadow9.setYOffset(0)
        self.shadow9.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_55.setGraphicsEffect(self.shadow9)

        self.shadow10 = QGraphicsDropShadowEffect(self)
        self.shadow10.setBlurRadius(20)
        self.shadow10.setXOffset(0)
        self.shadow10.setYOffset(0)
        self.shadow10.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_49.setGraphicsEffect(self.shadow10)

        self.shadow11 = QGraphicsDropShadowEffect(self)
        self.shadow11.setBlurRadius(20)
        self.shadow11.setXOffset(0)
        self.shadow11.setYOffset(0)
        self.shadow11.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_56.setGraphicsEffect(self.shadow11)

        self.shadow12 = QGraphicsDropShadowEffect(self)
        self.shadow12.setBlurRadius(20)
        self.shadow12.setXOffset(0)
        self.shadow12.setYOffset(0)
        self.shadow12.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_7.setGraphicsEffect(self.shadow12)

        self.shadow13 = QGraphicsDropShadowEffect(self)
        self.shadow13.setBlurRadius(5)
        self.shadow13.setXOffset(0)
        self.shadow13.setYOffset(0)
        self.shadow13.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_9.setGraphicsEffect(self.shadow13)

        self.shadow14 = QGraphicsDropShadowEffect(self)
        self.shadow14.setBlurRadius(5)
        self.shadow14.setXOffset(0)
        self.shadow14.setYOffset(0)
        self.shadow14.setColor(QColor(0, 0, 0, 100))
        self.ui.frame_31.setGraphicsEffect(self.shadow14)

        self.shadow15 = QGraphicsDropShadowEffect(self)
        self.shadow15.setBlurRadius(5)
        self.shadow15.setXOffset(0)
        self.shadow15.setYOffset(0)
        self.shadow15.setColor(QColor(0, 0, 0, 100))
        self.ui.label_27.setGraphicsEffect(self.shadow15)

        self.shadow16 = QGraphicsDropShadowEffect(self)
        self.shadow16.setBlurRadius(5)
        self.shadow16.setXOffset(0)
        self.shadow16.setYOffset(0)
        self.shadow16.setColor(QColor(0, 0, 0, 100))
        self.ui.tableWidget_5.setGraphicsEffect(self.shadow16)

        self.shadow17 = QGraphicsDropShadowEffect(self)
        self.shadow17.setBlurRadius(5)
        self.shadow17.setXOffset(0)
        self.shadow17.setYOffset(0)
        self.shadow17.setColor(QColor(0, 0, 0, 100))
        self.ui.tableWidget_6.setGraphicsEffect(self.shadow17)

        # ANIMATION
        self.movie = QMovie(":/gif/images/gif/profile.gif")
        self.ui.label_31.setMovie(self.movie)
        self.ui.label_3.setMovie(self.movie)
        self.startAnimation()

        # HIDE FUNCTION
        self.ui.pushButton_2.setCheckable(True)
        self.ui.pushButton_2.clicked.connect(self.changeicon)
        ## setting default
        self.ui.pushButton_2.setStyleSheet("QPushButton {\n"
                                           "    background-image: url(:/usedicon/images/used_icons/hide.png);\n"
                                           "    background-repeat: no-reperat;\n"
                                           "    background-position: center;\n"
                                           "    font: 75 14pt \"Georgia\";\n"
                                           "    color: rgb(0, 0, 0);\n"
                                           "    border-radius:10px;\n"
                                           "    background-color: rgb(237, 237, 253);\n"
                                           "    }\n"
                                           "QPushButton:pressed {\n"
                                           "    border-style: inset;\n"
                                           "    background-color:rgb(177, 177, 189);\n"
                                           "    }")
        self.update()
        ########################################################################
        self.show()

    def changeicon(self):

        if self.ui.pushButton_2.isChecked():
            self.ui.pushButton_2.setStyleSheet("QPushButton {\n"
                                               "    background-image: url(:/usedicon/images/used_icons/show.png);\n"
                                               "    background-repeat: no-reperat;\n"
                                               "    background-position: center;\n"
                                               "    font: 75 14pt \"Georgia\";\n"
                                               "    color: rgb(0, 0, 0);\n"
                                               "    border-radius:10px;\n"
                                               "    background-color: rgb(237, 237, 253);\n"
                                               "    }\n"
                                               "QPushButton:pressed {\n"
                                               "    border-style: inset;\n"
                                               "    background-color:rgb(177, 177, 189);\n"
                                               "    }")
            self.ui.label_75.hide()
            self.ui.label_77.hide()
            self.ui.amount.hide()
            self.ui.transaction.hide()
        else:
            self.ui.pushButton_2.setStyleSheet("QPushButton {\n"
                                               "    background-image: url(:/usedicon/images/used_icons/hide.png);\n"
                                               "    background-repeat: no-reperat;\n"
                                               "    background-position: center;\n"
                                               "    font: 75 14pt \"Georgia\";\n"
                                               "    color: rgb(0, 0, 0);\n"
                                               "    border-radius:10px;\n"
                                               "    background-color: rgb(237, 237, 253);\n"
                                               "    }\n"
                                               "QPushButton:pressed {\n"
                                               "    border-style: inset;\n"
                                               "    background-color:rgb(177, 177, 189);\n"
                                               "    }")
            self.ui.label_75.show()
            self.ui.label_77.show()
            self.ui.amount.show()
            self.ui.transaction.show()

    def startAnimation(self):
        self.movie.start()

    def fetch_table_data(self):
        # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
        month = self.ui.comboBox_20.currentText()
        year = self.ui.comboBox_21.currentText()
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT date,category,source,description,note,amount FROM expense WHERE MONTH(date) = %s AND YEAR(date) = %s AND user_id= %s"
        val = Login.user
        allvalues = (month, year, val)
        cur.execute(sql, allvalues)

        header = [row[0] for row in cur.description]
        rows = cur.fetchall()

        # Closing connection
        database.close()
        return header, rows

    def export(self):
        header, rows = self.fetch_table_data()
        tablename = self.ui.lineEdit.text()
        # Create an new Excel file.
        # DEFAULT SET>>QFileDialog.getSaveFileName(self, 'Save File'," "'.csv','(*.csv)')
        if tablename:
            # workbook = xlsxwriter.Workbook(tablename + '.csv')
            # worksheet = workbook.add_worksheet('MENU')
            # Create style for cells
            # header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
            # body_cell_format = workbook.add_format({'border': True})
            f = open(tablename + '.csv', 'w')

            # Write header
            f.write(','.join(header) + '\n')

            for row in rows:
                f.write(','.join(str(r) for r in row) + '\n')

            header, rows = self.fetch_table_data()

            # row_index = 0
            # column_index = 0
            #
            # for column_name in header:
            #     worksheet.write(row_index, column_index, column_name)
            #     column_index += 1
            #
            # row_index += 1
            # for row in rows:
            #     column_index = 0
            #     for column in row:
            #         worksheet.write(row_index, column_index, column)
            #         column_index += 1
            #     row_index += 1

            # print(str(row_index) + ' rows written successfully to ' + workbook.filename)
            Messageboxs.sucess(self, ' Sucessfully SAVED ',
                               ' rows written successfully to ' + f.name)
        else:
            Messageboxs.Warnings(self, 'Warning', 'FileName is required')
        # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/achievement.wav')

    def updateStateCombo(self, index):
        indx = self.model.index(index, 0, self.ui.comboBox_10.rootModelIndex())
        self.ui.comboBox_11.setRootModelIndex(indx)
        self.ui.comboBox_11.setCurrentIndex(0)

    def updateStateCombox(self, index):
        indx = self.modell.index(index, 0, self.ui.comboBox_18.rootModelIndex())
        self.ui.comboBox_19.setRootModelIndex(indx)
        self.ui.comboBox_19.setCurrentIndex(0)

    def updateStateCombox1(self, index):
        indx = self.mode.index(index, 0, self.ui.comboBox_26.rootModelIndex())
        self.ui.comboBox_27.setRootModelIndex(indx)
        self.ui.comboBox_27.setCurrentIndex(0)

    def trackexpense(self):
        user = Login.user
        month = self.ui.comboBox_28.currentText()
        year = self.ui.comboBox_29.currentText()
        category = self.ui.comboBox_26.currentText()
        description = self.ui.comboBox_27.currentText()
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT amount FROM expense WHERE category=%s and description=%s and MONTH(date) = %s AND YEAR(date) = %s AND user_id= %s  "
        val = (category, description, month, year, user)
        cur.execute(sql, val)
        amount = cur.fetchone()
        database.commit()
        try:
            y1 = ''.join(str(y1) for y1 in amount)
            am1 = int(y1)
            self.ui.label_87.setText("Rs  " + str(am1))
        except:
            self.ui.label_87.setText(str("No Data found :("))

    def budget(self):  # CREATING A BUDGET
        user = Login.user
        month = self.ui.comboBox_16.currentText()
        year = self.ui.comboBox_17.currentText()
        category = self.ui.comboBox_18.currentText()
        description = self.ui.comboBox_19.currentText()
        amount = self.ui.lineEdit_19.text()
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "INSERT INTO budget (month,year,category,description,amount,user_id) VALUES (%s,%s, %s,%s, %s, %s)"
        val = (month, year, category, description, amount, user)
        cur.execute(sql, val)
        database.commit()
        self.ui.tableWidget_4.setRowCount(1)
        MainWindow.loadData3(self)

    def notificationpage(self):  # NOTIFICATION
        user = Login.user
        titlee = self.ui.lineEdit_12.text()
        timee = self.ui.dateTimeEdit.text()
        category = self.ui.comboBox_15.currentText()
        messagee = self.ui.textEdit.toPlainText()
        x = self.ui.comboBox_15.currentIndex()
        if titlee and messagee:
            database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
            cur = database.cursor()
            sql = "INSERT INTO notification (date, category, title,message, user_id) VALUES (%s, %s,%s, %s, %s)"
            val = (timee, category, titlee, messagee, user)
            cur.execute(sql, val)
            database.commit()
            self.ui.tableWidget_3.setRowCount(1)
            MainWindow.loadData2(self)
        else:
            Messageboxs.Warnings(self, 'Warning', 'Title and Message is required')
        # if x == {0, 1, 2}:
        # ICON AS PER COMBOBOX INDEX NO
        if x == 0:
            b = "C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/bill.ico"
        elif x == 1:
            b = "C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/pay.ico"
        else:
            b = 'C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/call.ico'
        # MAGIC
        d = ddd.strptime(timee, "%Y-%d-%m %H:%M:%S")
        x = time.mktime(d.timetuple())
        y = time.time()
        z = int(x - y)

        DURATION_INT = z
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.title = titlee
        self.message = messagee
        self.icon = b
        MainWindow.startTimer(self)

    def startTimer(self):  # SETTING TIMER
        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(1000)

    def timerTimeout(self):  # POP UP NOTIFICATION WHEN TIME IS TRIGGERED
        self.time_left_int -= 1
        if self.time_left_int == 0:
            toaster.show_toast(self.title, self.message, icon_path=self.icon, threaded=True)
            # playsound('C:/Users/admin/PycharmProjects/pythonProject/Project1/sound/achievement.wav')

        # toaster.show_toast(titlee, messagee, duration=10, icon_path=a, threaded=True)

    def eandi(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()
        sql = "SELECT sum(amount) FROM expense WHERE MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE()) AND user_id=%s"
        val = Login.user
        cur.execute(sql, val)
        expense = cur.fetchone()
        sql1 = "SELECT sum(amount) FROM income WHERE MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE()) AND user_id=%s"
        cur.execute(sql1, val)
        income = cur.fetchone()
        database.commit()
        try:
            y1 = ''.join(str(y1) for y1 in expense)
            exp = int(y1)
            self.ui.label_75.setText(str(exp))
        except:
            self.ui.label_75.setText(str("ADD Your expense"))

        try:
            y = ''.join(str(y) for y in income)
            inc = int(y)
            self.ui.label_77.setText(str(inc))
        except:
            self.ui.label_77.setText(str("ADD Your Income"))

    def cashprogressBarValue(self):
        # PROGRESSBAR STYLESHEET BASE
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cur = database.cursor()

        sql = "SELECT COUNT(expense_id), SUM(amount) from expense WHERE user_id= %s"
        val = Login.user
        cur.execute(sql, val)
        tr = cur.fetchone()
        (transaction, e) = tr

        sql1 = "SELECT COUNT(income_id) from income WHERE user_id= %s"
        cur.execute(sql1, val)
        transaction1 = cur.fetchone()
        y = ''.join(str(y) for y in transaction1)
        exp1 = int(transaction)
        inc1 = int(y)
        final = exp1 + inc1
        try:
            self.ui.transaction.setText(str(final))

        except:
            self.ui.transaction.setText(str("None"))
        try:
            sql1 = "SELECT  SUM(amount) from income WHERE user_id= %s"
            cur.execute(sql1, val)
            j = cur.fetchone()
            y = ''.join(str(y) for y in j)
            income = int(y)
            expense = int(e)
            amount = income - expense
            self.ui.amount.setText(str(amount))
        except:
            self.ui.amount.setText(str("None"))

    def editimage(self):  # UPDATE PROFILE PICTURE
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image', QtCore.QDir.rootPath())
        # fileHandle = open(fileName, 'r')
        pixmap = QPixmap(fileName)
        # self.ui.label_31.setPixmap(pixmap)
        # self.ui.label_3.setPixmap(pixmap)

    def editprofile(self):  # UPDATE PROFILE
        user = Login.user
        username = self.ui.name_2.text()
        email = self.ui.name_3.text()
        passw = self.ui.name_4.text()
        cpassw = self.ui.name_5.text()
        gender = self.ui.comboBox_3.currentText()
        dob = self.ui.dateEdit_2.text()
        match = re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)
        if email and passw and gender and username and dob and cpassw:
            if self.ui.name_4.text() == self.ui.name_5.text():
                if len(username) > 4:
                    if match is None:
                        Messageboxs.Warnings(self, 'Error', 'Email is invalid')
                    else:
                        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
                        cursor = database.cursor()
                        sql = "UPDATE user SET email=%s,username=%s,gender=%s,dob=%s WHERE user_id=%s"
                        val = (email, username, gender, dob, user)
                        cursor.execute(sql, val)
                        database.commit()
                        database.close()
                        MainWindow.userprofile(self)
                else:
                    Messageboxs.Warnings(self, 'Error', "Username should be grater than 4 letter")
            else:
                Messageboxs.Warnings(self, 'Error', "password and confirm password  should be same")
        else:
            Messageboxs.Critical(self, 'Error', "Enter All the Details")

            # USER PROFILE

    def userprofile(self):  # UPDATE PROFILE
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        user = Login.user
        sql = "Select user_id,email,username,password,dob,gender from user where user_id = %s "
        val = user
        cursor.execute(sql, val)
        uservalue = cursor.fetchone()
        (idd, email, username, password, dob, gender) = uservalue
        self.ui.lineEdit_22.setText(str(idd))
        self.ui.lineEdit_21.setText(email)
        self.ui.lineEdit_15.setText(username)
        self.ui.lineEdit_18.setText(username)

        if len(dob) < 1:
            self.ui.lineEdit_16.setText("")
            self.ui.lineEdit_17.setText(str(""))
        else:
            self.ui.lineEdit_16.setText(dob)
            # calculate age
            today = date.today()
            born = datetime.datetime.strptime(dob, '%Y-%m-%d')
            x = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            self.ui.lineEdit_17.setText(str(x))

        if len(gender) < 1:
            self.ui.lineEdit_20.setText("")
        else:
            self.ui.lineEdit_20.setText(gender)

        self.ui.name_2.setText(username)
        self.ui.name_3.setText(email)
        self.ui.name_4.setText(password)
        # self.ui.name_5.setText(password)
        # self.ui.comboBox_3.setItemText(gender)rgb(2, 194, 204);

    # Annually payments
    def emi_calculate(self):

        # getting annual interest rate
        annualInterestRate = self.ui.lineEdit_2.text()
        # if there is no number is entered
        match = re.match('[a-zA-Z!@#$%^&*]', annualInterestRate)
        if match:
            return

        if len(annualInterestRate) == 0 or annualInterestRate == '0':
            return

        # getting number of years
        numberOfYears = self.ui.lineEdit_6.text()

        # if there is no number is entered
        if len(numberOfYears) == 0 or numberOfYears == '0':
            return

        # getting loan amount
        loanAmount = self.ui.lineEdit_7.text()

        # if there is no number is entered
        if len(loanAmount) == 0 or loanAmount == '0':
            return

        # converting text to int
        annualInterestRate = float(annualInterestRate)
        numberOfYears = int(numberOfYears)
        loanAmount = int(loanAmount)

        # getting monthly interest rate
        monthlyInterestRate = annualInterestRate / 1200

        # calculating monthly payemnt
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))

        # setting formatting
        monthlyPayment = "{:.2f}".format(monthlyPayment)

        # setting text to the label
        self.ui.lineEdit_13.setText("Monthly Payment : " + str(monthlyPayment))

        # getting total payment
        totalPayment = float(monthlyPayment) * 12 * numberOfYears
        totalPayment = "{:.2f}".format(totalPayment)

        # setting text to the label
        self.ui.lineEdit_14.setText("Total Payment : " + str(totalPayment))

    def expprogress(self):
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        userid = Login.user
        sql = "Select amount from expense where user_id = %s "
        val = userid
        cursor.execute(sql, val)
        MainWindow.x = cursor.fetchall()
        database.commit()
        database.close()
        return MainWindow.x

    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE DASHBOARD
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
            MainWindow.resetStyle(self, "btn_home")
            MainWindow.labelPage(self, "Dashboard")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE TRANSACTION
        if btnWidget.objectName() == "btn_trans":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            MainWindow.resetStyle(self, "btn_trans")
            MainWindow.labelPage(self, "Transaction")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE BUDGET
        if btnWidget.objectName() == "btn_budget":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)
            MainWindow.resetStyle(self, "btn_budget")
            MainWindow.labelPage(self, "Budget")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE Event
        if btnWidget.objectName() == "btn_editor":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_8)
            MainWindow.resetStyle(self, "btn_event")
            MainWindow.labelPage(self, "Edit/Export")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE Bills
        if btnWidget.objectName() == "btn_notify":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_9)
            MainWindow.resetStyle(self, "btn_bills")
            MainWindow.labelPage(self, "NOTIFICATION")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE Graph
        if btnWidget.objectName() == "btn_graph":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
            MainWindow.resetStyle(self, "btn_graph")
            MainWindow.labelPage(self, "Graph")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))
        # PAGE Track
        if btnWidget.objectName() == "btn_track":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)
            MainWindow.resetStyle(self, "btn_track")
            MainWindow.labelPage(self, "Track")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE Tools
        if btnWidget.objectName() == "btn_tools":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_7)
            MainWindow.resetStyle(self, "btn_tools")
            MainWindow.labelPage(self, "Tools")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE Account
        if btnWidget.objectName() == "btn_account":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)
            MainWindow.resetStyle(self, "btn_account")
            MainWindow.labelPage(self, "Account")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

        # PAGE About Us
        if btnWidget.objectName() == "btn_aboutus":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_11)
            MainWindow.resetStyle(self, "btn_aboutus")
            MainWindow.labelPage(self, "About Us")
            btnWidget.setStyleSheet(MainWindow.selectMenu(btnWidget.styleSheet()))

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def inc(self):  # INCOME
        date = self.ui.dateEdit_5.text()
        source = self.ui.comboBox_14.currentText()
        category = self.ui.comboBox_13.currentText()
        description = self.ui.lineEdit_11.text()
        amount = self.ui.lineEdit_5.text()
        userid = Login.user
        # DATABSE CONNECTION
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql = "INSERT INTO income (user_id, date, category, source, description, amount) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (userid, date, category, source, description, amount)
        cursor.execute(sql, val)
        database.commit()
        database.close()
        # UPDATE
        self.ui.tableWidget_6.setRowCount(1)
        MainWindow.loadData(self)
        MainWindow.eandi(self)
        MainWindow.cashprogressBarValue(self)
        # FOR NOTIFICATION
        toaster.show_toast('Inserted Data', 'Added Successfully', duration=10,
                           icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/add.ico',
                           threaded=True)

    def expe(self):  # EXPENSE
        date = self.ui.dateEdit_4.text()
        source = self.ui.comboBox_12.currentText()
        category = self.ui.comboBox_10.currentText()
        description = self.ui.comboBox_11.currentText()
        amount = self.ui.lineEdit_4.text()
        note = self.ui.lineEdit_10.text()
        userid = Login.user
        database = pymysql.connect(host='localhost', user='root', passwd='', database='expmonitor')
        cursor = database.cursor()
        sql = "INSERT INTO expense (user_id, date, category, source, description, amount, note) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (userid, date, category, source, description, amount, note)
        cursor.execute(sql, val)
        database.commit()
        database.close()
        # UPDATE
        self.ui.tableWidget_5.setRowCount(1)
        MainWindow.loadData1(self)
        MainWindow.eandi(self)
        MainWindow.cashprogressBarValue(self)
        toaster.show_toast('Inserted Data', 'Added Successfully', duration=10,
                           icon_path='C:/Users/admin/PycharmProjects/pythonProject/Project1/images/used_icons/add.ico',
                           threaded=True)

    # DYNAMIC MENUS
    ########################################################################
    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count), self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 60))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(str(name))
        button.setToolTip(str(name))
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)

        else:
            self.ui.layout_menu_bottom.addWidget(button)

    ## ==> SELECT/DESELECT MENU
    ########################################################################
    ## ==> SELECT
    def selectMenu(getStyle):
        select = getStyle + (
            "QPushButton { background-color: rgb(44, 48, 58);border-left: 20px solid rgb(44, 48, 58) }QPushButton:Pressed{ border-left: 20px solid rgb(2, 194, 204);}")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(
            "QPushButton { background-color: rgb(44, 48, 58);border-left: 20px solid rgb(44, 48, 58) }QPushButton:Pressed{ border-left: 20px solid rgb(2, 194, 204);}",
            "")
        return deselect

    ## ==> START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(MainWindow.selectMenu(w.styleSheet()))

    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(MainWindow.deselectMenu(w.styleSheet()))

    ## ==> CHANGE PAGE LABEL TEXT
    def labelPage(self, text):
        newText = '|  ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    # CALCLATOR
    def method_1(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "1")

    def method_2(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "2")

    def method_3(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "3")

    def method_4(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "4")

    def method_5(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "5")

    def method_6(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "6")

    def method_7(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "7")

    def method_8(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "8")

    def method_9(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "9")

    def method_zero(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "0")

    def method_point(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + ".")

    def method_plus(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "+")

    def method_min(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "-")

    def method_mult(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "*")

    def method_div(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text + "/")

    def method_clear(self):
        self.ui.label_11.setText("")

    def method_del(self):
        text = self.ui.label_11.text()
        self.ui.label_11.setText(text[:len(text) - 1])

    def method_equal(self):
        text = self.ui.label_11.text()

        try:
            ans = eval(text)
            self.ui.label_11.setText(str(ans))
        except:
            self.ui.label_11.setText("Wrong Input")

    # Text Editor
    def dialog_critical(self, s):

        # creating a QMessageBox object
        dlg = QMessageBox(self)

        # setting text to the dlg
        dlg.setText(s)

        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)

        # showing it
        dlg.show()

        # action called by file open action

    def file_open(self):

        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "All files (*.*)")

        # if path is true
        if path:
            # try opening path
            try:
                with codecs.open(path, 'r', encoding='utf8', errors='ignore') as json_file:
                    # read the file

                    text = json_file.read()


            # if some error occured
            except Exception as e:

                # show error using critical method
                self.dialog_critical(str(e))
            # else
            else:
                # update path value
                self.path = path

                # update the text
                self.ui.plainTextEdit.setPlainText(text)

                # update the title
                self.update_title()
        # action called by file save action

    def file_save(self):

        # if there is no save path
        if self.path is None:
            # call save as method
            return self.file_saveas()

        # else call save to path method
        else:
            self._save_to_path(self.path)

        # action called by save as action

    def file_saveas(self):

        # opening path
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text Document (.txt)")

        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return

        # else call save to path method
        self._save_to_path(path)

        # save to path method

    def _save_to_path(self, path):

        # get the text
        text = self.ui.plainTextEdit.toPlainText()

        # try catch block
        try:

            # opening file to write
            with open(path, 'w') as f:

                # write text in the file
                f.write(text)

        # if error occurs
        except Exception as e:

            # show error using critical
            self.dialog_critical(str(e))

        # else do this
        else:
            # change path
            self.path = path
            # update the title
            # self.update_title()

        # action called by print

    # def update_title(self):
    #
    #     # setting window title with prefix as file name
    #     # suffix aas PyQt5 Notepad
    #     self.setWindowTitle("%s - PyQt5 Notepad" % (os.path.basename(self.path)
    #                                                 if self.path else "Untitled"))


# UI Functions
class UIFunctions(MainWindow):
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            # # ANIMATION
            self.animation1 = QPropertyAnimation(self.ui.frame_toggle, b"minimumWidth")
            self.animation1.setDuration(400)
            self.animation1.setStartValue(width)
            self.animation1.setEndValue(widthExtended)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start()

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        # IF NOT MAXIMIZED
        if status == 0:
            self.showMaximized()

            # SET GLOBAL TO 1
            GLOBAL_STATE = 1
            # self.ui.btn_maximize.setToolTip("Restore")
            self.ui.frame_size_grip.hide()

        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            # self.ui.btn_maximize.setToolTip("Maximize")
            self.ui.frame_size_grip.show()

    def uiDefinitions(self):

        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        # MAXIMIZE / RESTORE
        self.ui.max.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # MINIMIZE
        self.ui.min.clicked.connect(lambda: self.showMinimized())

        # CLOSE
        self.ui.close.clicked.connect(lambda: self.close())

    def returnStatus(self):
        return GLOBAL_STATE

    def minclose(self):
        # CLOSE
        self.ui.close.clicked.connect(lambda: self.close())

    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.max.hide()


data = {
    'Bills': ['Light Bills', 'Phone Bills', 'Transportation Pass', 'Water & Maintenance', ''],
    'Food&Drinks ': ['Bar', 'Cafe', 'Fast-food', 'Groceries', 'Restaurants'],
    'Shopping': ['Clothes', 'Chemist', 'Electronics', 'Gifts', 'Groceries', 'health & Beauty', 'Stationery', 'Tools'],
    'Housing': ['Energy,utilities', 'Repairs', 'Maintenance', 'Mortgage', 'Property insurance', 'Rent', 'Services'],
    'Transportation': ['Business trips', 'Long Distance', 'Public Transport', 'Taxi'],
    'Vehicle': ['Fuel', 'Leasing', 'Parking', 'Rentals', 'Vehicle Insurance', 'Vehicle Maintenance'],
    'Entertainment': ['Active sport', 'Books', 'Charity', 'Cinema', 'Culture', 'Education', 'Fitness', 'Health care',
                      'Hobbies', 'Holiday trips', 'Hotel', 'Life events', 'Lottery,gambling', 'Wellness & Beauty'],
    'Communication': ['Internet', 'Phone', 'Postal services'],
    'financial': ['Advisory', 'Charges,fee', 'Child Support', 'Fines', 'Insurances', 'Interests', 'Loan', 'Taxes'],
    'Investments': ['Collections', 'Financial investments', 'Jewels', 'Policy', 'Savings', 'Schemes'], 'other': ['']
}

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Splash()
    window.show()
    sys.exit(app.exec_())
