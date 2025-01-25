from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(535, 617)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
                                        "    color: #FFF;\n"
                                        "}\n"
                                        "\n"
                                        "QWidget{\n"
                                        "    background: rgb(70, 71, 106);\n"
                                        "}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.app_logo = QtWidgets.QFrame(parent=self.centralwidget)
        self.app_logo.setMinimumSize(QtCore.QSize(0, 200))
        self.app_logo.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.app_logo.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.app_logo.setObjectName("app_logo")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.app_logo)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_img = QtWidgets.QLabel(parent=self.app_logo)
        self.logo_img.setMinimumSize(QtCore.QSize(100, 100))
        self.logo_img.setMaximumSize(QtCore.QSize(100, 100))
        self.logo_img.setSizeIncrement(QtCore.QSize(0, 0))
        self.logo_img.setStyleSheet("QLabel{\n"
"    border-radius: 0px;\n"
"}")
        self.logo_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo_img.setObjectName("logo_img")
        self.horizontalLayout.addWidget(self.logo_img)
        self.verticalLayout.addWidget(self.app_logo)
        self.background = QtWidgets.QFrame(parent=self.centralwidget)
        self.background.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.background.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.background.setObjectName("background")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.background)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.app_name = QtWidgets.QLabel(parent=self.background)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.app_name.setFont(font)
        self.app_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.app_name.setObjectName("app_name")
        self.verticalLayout_2.addWidget(self.app_name)
        self.app_description = QtWidgets.QLabel(parent=self.background)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(18)
        self.app_description.setFont(font)
        self.app_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.app_description.setObjectName("app_description")
        self.verticalLayout_2.addWidget(self.app_description)
        self.progress = QtWidgets.QFrame(parent=self.background)
        self.progress.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.progress.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.progress.setObjectName("progress")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.progress)
        self.verticalLayout_3.setContentsMargins(30, -1, 30, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(parent=self.progress)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(parent=self.progress)
        self.progressBar.setMinimumSize(QtCore.QSize(10, 10))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.progressBar.setStyleSheet("QProgressBar{\n"
                                        "    background: rgba(255,255,255,180);\n"
                                        "    border-style: none;\n"
                                        "    border-radius: 5px;\n"
                                        "    color: rgba(200,200,200,0);\n"
                                        "    text-align:center;\n"
                                        "}\n"
                                        "\n"
                                        "QProgressBar::chunk{\n"
                                        "    border-radius: 5px;\n"
                                        "        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #2b2b2b, stop: 0.4 #555555, stop: 1 #1b5e20);\n"
                                        "\n"
                                        "}\n"
                                        "")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_2.addWidget(self.progress)
        self.footer = QtWidgets.QFrame(parent=self.background)
        self.footer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.status = QtWidgets.QLabel(parent=self.footer)
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(10)
        self.status.setFont(font)
        self.status.setObjectName("status")
        self.horizontalLayout_2.addWidget(self.status)
        self.verticalLayout_2.addWidget(self.footer)
        self.verticalLayout.addWidget(self.background)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo_img.setText(_translate("MainWindow", "Logo"))
        self.app_name.setText(_translate("MainWindow", "SteerWise"))
        self.app_description.setText(_translate("MainWindow", "Akıllı Direksiyon Simidi"))
        self.label.setText(_translate("MainWindow", "%20"))
        self.status.setText(_translate("MainWindow", "status"))
