from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()  # Tam ekran başlatmak için

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: black;")
        # Hız göstergesi resmi
        self.speedometer_img = QtWidgets.QLabel(parent=self.centralwidget)
        self.speedometer_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.speedometer_img.setObjectName("speedometer_img")
        self.speedometer_img.setGeometry(QtCore.QRect(40, 160, 450, 450))  # Resmin boyutları ve pozisyonu

        # Button
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QtCore.QRect(700, 50, 200, 50))  # Button size and position
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    spread: pad, 
                    x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #4f4f4f,  /* Dark metallic gray */
                    stop: 1 #8f8f8f  /* Light metallic gray */
                );
                color: white;  /* Text color */
                border: 2px solid #333;  /* Dark border */
                font-size: 14px;  /* Font size */
                font-weight: bold;  /* Bold text */
                text-transform: uppercase;  /* Uppercase text */
                letter-spacing: 1px;  /* Slight spacing between letters */
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread: pad, 
                    x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 #6f6f6f,  /* Slightly lighter gray */
                    stop: 1 #afafaf  /* Even lighter gray */
                );
                border: 2px solid #555;  /* Lighter border on hover */
            }
            QPushButton:pressed {
                background-color: #2f2f2f;  /* Darker gray for pressed effect */
                border: 2px solid #999;  /* Light border for pressed effect */
            }
        """)

        # Kapatma butonu
        self.close_button = QtWidgets.QPushButton("✖", self.centralwidget)
        self.close_button.setStyleSheet("font-size: 20px; color: white; background-color: red; border: none;")
        self.close_button.setGeometry(QtCore.QRect(1450, 50, 40, 40))  # Sağ üst köşeye yerleştir
        self.close_button.raise_()  # Butonu üstte görünür hale getir

        # Araba resmi
        self.car_img = QtWidgets.QLabel(parent=self.centralwidget)
        self.car_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.car_img.setObjectName("car_img")
        self.car_img.setGeometry(QtCore.QRect(650, 250, 300, 300))  # Resmin boyutları ve pozisyonu
        self.car_img.setStyleSheet("background-color: transparent;")

        # Direksiyon resmi
        self.steering_wheel_img = QtWidgets.QLabel(parent=self.centralwidget)
        self.steering_wheel_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.steering_wheel_img.setObjectName("steering_wheel_img")
        self.steering_wheel_img.setGeometry(QtCore.QRect(1050, 180, 400, 400))  # Resmin boyutları ve pozisyonu

        # Warning Message
        self.warnig_info = QtWidgets.QLabel(parent=self.centralwidget)
        self.warnig_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.warnig_info.setObjectName("warnig_info")
        self.warnig_info.setGeometry(QtCore.QRect(1000, 700, 500, 50))  # Size and position
        self.warnig_info.setStyleSheet("""
            QLabel {
                background-color: #2c2c2c;  /* Dark gray background */
                color: #ff0000;  /* Bright red text for alert */
                border: 2px solid #ff0000;  /* Red border for emphasis */
                font-size: 16px;  /* Larger text size */
                font-weight: bold;  /* Bold text for visibility */
                text-transform: uppercase;  /* Uppercase for a professional look */
                letter-spacing: 1px;  /* Slight letter spacing for clarity */
            }
        """)

        # Sıcaklık değeri için label
        self.temp_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.temp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setObjectName("temp_label")
        self.temp_label.setGeometry(QtCore.QRect(40, 700, 200, 50))  # speedometer ile aynı dikey eksende
        
        # Kalp atış hızı için label
        self.bpm_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.bpm_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bpm_label.setObjectName("bpm_label")
        self.bpm_label.setGeometry(QtCore.QRect(250, 700, 200, 50))  # temp_label'ın yanında
        
        # Tüm label'lar için ortak stil
        label_style = """
            QLabel {
                background-color: #2c2c2c;  /* Dark gray background */
                color: #ffffff;  /* White text */
                border: 2px solid #444;  /* Gray border */
                font-size: 16px;  /* Text size */
                font-weight: bold;  /* Bold text */
                text-transform: uppercase;  /* Uppercase text */
                letter-spacing: 1px;  /* Letter spacing */
            }
        """
                
        self.warnig_info.setStyleSheet(label_style.replace("color: #ffffff", "color: #ff0000"))  # Uyarı mesajı kırmızı
        self.temp_label.setStyleSheet(label_style)
        self.bpm_label.setStyleSheet(label_style)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.speedometer_img.setText(_translate("MainWindow", "Speedometer"))
        #self.needle_img.setText(_translate("MainWindow", "Needle"))
        self.pushButton.setText(_translate("MainWindow", "Motoru Çalıştır"))
        self.car_img.setText(_translate("MainWindow", "Car"))
        self.steering_wheel_img.setText(_translate("MainWindow", "steering wheel"))
        self.warnig_info.setText(_translate("MainWindow", "UYARI: Uygun el pozisyonunda tutunuz."))
        self.temp_label.setText(_translate("MainWindow", "Sıcaklık: -- °C"))
        self.bpm_label.setText(_translate("MainWindow", "Nabız: -- BPM"))
