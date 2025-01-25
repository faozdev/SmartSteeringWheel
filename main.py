from PyQt6 import QtWidgets, QtCore, QtGui 
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve, QPointF, QRect, pyqtSignal, pyqtProperty, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QColor, QTransform, QGuiApplication, QMovie, QPen
from PIL import Image, ImageQt
from loading_screen import Ui_MainWindow as LoadingScreen
from main_screen import Ui_MainWindow as MainScreen
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
import math
import serial
import threading



class LoadingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoadingScreen()
        self.ui.setupUi(self)

        pixmap = QPixmap("img/steering_wheel.png")
        self.ui.logo_img.setPixmap(pixmap)
        self.ui.logo_img.setScaledContents(True)
        self.ui.status.setText("Yükleniyor...")

        # Yükleme ekranı simüle edin
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(50)
        
        QtCore.QTimer.singleShot(1500, lambda: self.ui.status.setText("Arduino bağlantısı kontrol ediliyor..."))
        QtCore.QTimer.singleShot(3500, lambda: self.ui.status.setText("Arduino data çekiliyor..."))
        QtCore.QTimer.singleShot(5500, lambda: self.ui.status.setText("Başlatılıyor..."))

    def update_progress(self):
        self.progress_value += 1
        self.ui.progressBar.setValue(self.progress_value)
        self.ui.label.setText(f"%{self.progress_value}")

        if self.progress_value >= 100:
            self.timer.stop()
            self.switch_to_main()

    def switch_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.main_window.showFullScreen()
        self.close()

class DotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.num_dots = 15
        self.dot_radius = 20
        self.radius = 135
        self.dots = []
        self.initialize_dots()

    def initialize_dots(self):
        center_x, center_y = 200, 200  
        for i in range(self.num_dots):
            angle = 2 * math.pi * i / self.num_dots
            x = center_x + self.radius * math.cos(angle)
            y = center_y + self.radius * math.sin(angle)
            self.dots.append({"x": x, "y": y, "color": QColor("blue")})

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for dot in self.dots:
            painter.setBrush(dot["color"])
            painter.drawEllipse(
                int(dot["x"] - self.dot_radius / 2 ),
                int(dot["y"] - self.dot_radius / 2 ),
                self.dot_radius,
                self.dot_radius
            )

        painter.end()

    def update_dot_colors(self, sensor_data):
        """
        Sensör verilerine göre noktaların renklerini günceller.
        1 ise kırmızı, 0 ise mavi olur.
        """
        for i, value in enumerate(sensor_data):
            if i < len(self.dots):  # Sensör verilerinin nokta sayısından fazla olmamasını kontrol et
                self.dots[i]["color"] = QColor("red") if value == 1 else QColor("blue")
        self.update()  # Widget'ı yeniden çiz

class Needle_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  
        self.setMinimumSize(500, 500)
        self.angle = 0  # Direksiyon açısı, varsayılan 0 derecedir
        self.needle_image = QPixmap("img/needle.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Load your needle image here
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_rotation)
        self.target_angle = 0

    def set_angle(self, angle):
        """Animasyon için hedef açıyı ayarlayın."""
        self.target_angle = angle
        if not self.timer.isActive():
            self.timer.start(16)  # ~60 FPS'de çalıştırın

    def animate_rotation(self):
        """İğneyi hedef açıya doğru kademeli olarak döndürün."""
        if self.angle < self.target_angle:
            self.angle += 5  # Açıyı artırın
        elif self.angle > self.target_angle:
            self.angle -= 5  # Açıyı azaltma
        else:
            self.timer.stop()  # Hedefe ulaşıldığında animasyonu durdur

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        print("NeedleWidget paintEvent called")
        # Döndürülmüş iğne resmini çizin
        center = self.rect().center()
        y_offset = +150  # İğneyi gerektiği gibi yukarı veya aşağı hareket ettirmek için bu değeri ayarlayın
        x_offset = +0 

        # painter çevirme
        painter.translate(center.x() + x_offset , center.y() + y_offset)
        painter.rotate(self.angle)  # painter döndürme
        painter.translate(-self.needle_image.width() // 2, -self.needle_image.height() // 2)
        painter.drawPixmap(0, 0, self.needle_image)

        painter.end()

class GifWidget(QLabel):
    def __init__(self, parent=None, gif_path="img/road3.gif"):
        super().__init__(parent)
        self.setGeometry(parent.geometry())  # Ana widget ile aynı boyut ve konum
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def start(self):
        """GIF animasyonunu başlat."""
        if self.movie.state() != QMovie.MovieState.Running:
            self.movie.start()

    def stop(self):
        """GIF animasyonunu durdur."""
        if self.movie.state() == QMovie.MovieState.Running:
            self.movie.stop()

    def update_position(self, geometry):
        """GIF'in konumunu ve boyutunu güncelleyin."""
        self.setGeometry(geometry)

def check_steering_grip(sensor_data, warning_label, ser=None):
    # Basılı noktaların (1'lerin) indekslerini listele
    indices = [i for i, value in enumerate(sensor_data) if value == 1]
    count = len(indices)
    print("Count:", count)

    # Stil tanımları
    red_style = (
        "background-color: #2c2c2c; color: #ff0000; border: 2px solid #444;"
        "font-size: 16px; font-weight: bold; text-transform: uppercase;"
        "letter-spacing: 1px;"
    )
    green_style = (
        "background-color: #2c2c2c; color: green; border: 2px solid #444;"
        "font-size: 16px; font-weight: bold; text-transform: uppercase;"
        "letter-spacing: 1px;"
    )

    # Arduino'ya veri göndermede kullanım kolaylığı için fonksiyon:
    def buzzer_on():
        
        if ser:
            ser.write(b'1')
            print("Buzzer çalıştırıldı")

    def buzzer_off():
        if ser:
            ser.write(b'0')
            print("Buzzer durduruldu")

    # 1) Eğer basılı nokta sayısı 2'den az ise
    if count < 2:
        warning_label.setText("Ellerinizi direksiyonda tutun.")
        warning_label.setStyleSheet(red_style)
        buzzer_on()
        return

    # 2) En az 2 nokta var => buzzer kapat
    buzzer_off()

    # Eğer tam 2 nokta basılıysa hangi kombinasyona yakın olduğuna bakalım
    if count == 2:
        left, right = sorted(indices)

        # Tolerans değeri (örnek: ±1)
        tolerance = 1  

        # İdeal tutuş noktalarını tanımlayalım (isim, (left, right))
        ideal_positions = {
            "9:15 tutuşu": (0, 8),
            "10:10 tutuşu": (8, 14),
            "11:05 tutuşu": (10, 12),
        }
        
        # Bu fonksiyon, left/right değerlerinin ideal_left/ideal_right
        # değerleri etrafında 'tolerance' kadar sapmaya izin verir
        def is_within_tolerance(l_val, r_val, ideal_l, ideal_r, tol):
            return abs(l_val - ideal_l) <= tol and abs(r_val - ideal_r) <= tol

        # Uygun eşleşmeyi bulduğumuzda yazacağımız mesaj
        # (bulunamazsa "Tavsiye edilen tutuşlar..." diyeceğiz)
        matched_position = None
        for name, (ideal_l, ideal_r) in ideal_positions.items():
            if is_within_tolerance(left, right, ideal_l, ideal_r, tolerance):
                matched_position = name
                break

        if matched_position:
            if matched_position == "9:15 tutuşu":
                warning_label.setText("9:15 tutuşu: Trafikte rahat bir kullanım")
            elif matched_position == "10:10 tutuşu":
                warning_label.setText("10:10 tutuşu: Daha fazla manevra")
            elif matched_position == "11:05 tutuşu":
                warning_label.setText("11:05 tutuşu: Operasyonel tutuş; manevra için")

            warning_label.setStyleSheet(green_style)

        else:
            # İki nokta var ama ideal kombinasyon(±tolerans) değil
            warning_label.setText("Tavsiye edilen tutuşlar: 9:15, 10:10, 11:05")
            warning_label.setStyleSheet(red_style)

    else:
        # 2'den fazla basılı nokta varsa (3,4,...)
        warning_label.setText("Tavsiye edilen tutuşlar: 9:15, 10:10 ve 11:05")
        warning_label.setStyleSheet(red_style)

def check_steering_grip2(sensor_data, warning_label, ser=None):
    indices = [i for i, value in enumerate(sensor_data) if value == 1]
    count = len(indices)
    print("Count:", count)
    
    if count == 0 or count == 1:
        warning_label.setText("Ellerinizi direksiyonda tutun.")
        warning_label.setStyleSheet("""background-color: #2c2c2c; color: #ff0000; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
        if ser:  # Arduino bağlantısı varsa
            ser.write(b'1')  # Buzzer'ı çalıştır
            print("Buzzer çalıştırıldı")
    elif count >= 2 and count <= 4:
        if ser:  # Arduino bağlantısı varsa
            ser.write(b'0')  # Buzzer'ı durdur
            print("Buzzer durduruldu")

        # Tolerans payı
        tolerance = 1

        # Mevcut tutuş pozisyonu kontrolleri...
        warning_label.setStyleSheet("""background-color: #2c2c2c; color: #ff0000; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
        left, right = indices
        if left == 0 and right == 8:
            warning_label.setText("9:15 tutuşu: Trafikte rahat bir kullanım")
            warning_label.setStyleSheet("""background-color: #2c2c2c; color: green; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
        elif left == 8 and right == 14:
            warning_label.setText("10:10 tutuşu: Daha fazla manevra")
            warning_label.setStyleSheet("""background-color: #2c2c2c; color: green; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
        elif left == 10 and right == 12:
            warning_label.setText("11:05 tutuşu: Operasyonel tutuş; manevra için")
            warning_label.setStyleSheet("""background-color: #2c2c2c; color: green; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
        else:
            warning_label.setText("Tavsiye edilen tutuşlar: 9:15, 10:10 ve 11:05")
            warning_label.setStyleSheet("""background-color: #2c2c2c; color: #ff0000; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)
    else:
        if ser:  # Arduino bağlantısı varsa
            ser.write(b'0')  # Buzzer'ı durdur
        warning_label.setText("Tavsiye edilen tutuşlar: 9:15, 10:10 ve 11:05")
        warning_label.setStyleSheet("""background-color: #2c2c2c; color: #ff0000; border: 2px solid #444; font-size: 16px; font-weight: bold;text-transform: uppercase; letter-spacing: 1px; """)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainScreen()
        self.ui.setupUi(self)
        self.angle = 0

        self.running = True  # İş parçacığının çalışıp çalışmayacağını kontrol eden bayrak
        
        # Arabayı sağa sola hareket ettirmek için başlangıç konumu ve sınırlar
        self.car_position = self.ui.car_img.geometry().x()
        self.car_min_x = 500  # Minimum x koordinatı
        self.car_max_x = 700  # Maksimum x koordinatı

        wheel_img = QPixmap("img/steering_wheel.png").scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ui.steering_wheel_img.setPixmap(wheel_img)
        
        # DotWidget oluştur ve steering_wheel_img üstüne yerleştir
        self.dot_widget = DotWidget(self.ui.steering_wheel_img)
        self.dot_widget.setGeometry(0, 0, 400, 400)  # steering_wheel_img boyutlarına uygun
        self.dot_widget.raise_()

        speedometer_img = QPixmap("img/speedometer.png").scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ui.speedometer_img.setPixmap(speedometer_img)

        self.SpeedometerNeedle = Needle_Widget(self.ui.centralwidget)
        self.SpeedometerNeedle.setGeometry(0, 0, 400, 400)

        car_img = QPixmap("img/car.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.ui.car_img.setPixmap(car_img)
        
        self.toggle = True  # İlk başta turn_right çağrılacak
        self.ui.pushButton.clicked.connect(self.toggle_turn)

        # GifWidget'ı başlatın ve araba animasyonunu araba görüntüsünün arkasına ayarlayın
        self.gif_widget = GifWidget(self.ui.centralwidget, "img/road3.gif")
        self.gif_widget.setGeometry(self.ui.car_img.geometry()) # Araba resmiyle aynı konumu ayarlayın
        self.gif_widget.lower() 

        # İlk olarak GIF'i başlatın
        self.gif_widget.start()
        self.gif_widget.stop()

        self.ui.warnig_info.setVisible(False)  # İlk başta görünmez hale getir
        self.ui.bpm_label.setVisible(False)
        self.ui.temp_label.setVisible(False)
        
        # Arduino bağlantısı
        self.arduino_port = "COM4"
        self.baud_rate = 9600
        global ser  # ser'i global olarak tanımla
        self.ser = None  # ser'i sınıf değişkeni olarak başlat
        
        # Arduino thread'ini başlat
        self.arduino_thread = threading.Thread(target=self.read_arduino_data, daemon=True)
        self.arduino_thread.start()

        # Sıcaklık uyarısı için yeni label oluştur
        self.warning_label = QLabel(self)
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.setStyleSheet("background-color: #2c2c2c; color: #ff0000;  border: 2px solid #ff0000;  /* Red border for emphasis */font-size: 16px;  /* Larger text size */font-weight: bold;  /* Bold text for visibility */text-transform: uppercase;  /* Uppercase for a professional look */letter-spacing: 1px;  /* Slight letter spacing for clarity */")
        self.warning_label.hide()  # Başlangıçta gizle
        
        # Uyarı için timer
        self.temp_warning_timer = QTimer()
        self.temp_warning_timer.timeout.connect(self.toggle_temp_warning)
        self.temp_warning_visible = True

        # Nabız uyarısı için yeni label oluştur
        self.pulse_warning_label = QLabel(self)
        self.pulse_warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pulse_warning_label.setStyleSheet("background-color: #2c2c2c; color: #ff0000;  border: 2px solid #ff0000;  /* Red border for emphasis */font-size: 16px;  /* Larger text size */font-weight: bold;  /* Bold text for visibility */text-transform: uppercase;  /* Uppercase for a professional look */letter-spacing: 1px;  /* Slight letter spacing for clarity */")
        self.pulse_warning_label.hide()  # Başlangıçta gizle
        
        # Nabız uyarısı için timer
        self.pulse_warning_timer = QTimer()
        self.pulse_warning_timer.timeout.connect(self.toggle_pulse_warning)
        self.pulse_warning_visible = True

        self.ui.close_button.clicked.connect(self.close)


    def read_arduino_data(self):
        try:
            global ser  # global ser'i kullan
            self.ser = serial.Serial(self.arduino_port, self.baud_rate, timeout=1)
            ser = self.ser  # global ser'i güncelle
            print("Arduino'ya bağlandı.")
            if ser:
                ser.write(b'0')  # Buzzer'ı kapat
                print("Buzzer başlangıçta kapatıldı")

            while self.running:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Gelen veri: {line}")  # Debug için veriyi yazdır
                    
                    try:
                        clean_data = line.replace("Sensör Durumları: ", "")
                        data = clean_data.split(",")
                        
                        if len(data) >= 17:
                            # Dokunma sensör verilerini int listesine çevir
                            touch_sensors = [int(x) for x in data[:15]]
                            pulse = int(data[15])
                            temperature = float(data[16])

                            print(f"İşlenen veriler: Touch={touch_sensors}, Pulse={pulse}, Temp={temperature}")  # Debug için

                            # GUI güncellemelerini ana thread'de yap
                            self.update_all_data(touch_sensors, pulse, temperature)

                    except ValueError as ve:
                        print(f"Veri dönüştürme hatası: {ve}")
                    except Exception as e:
                        print(f"Veri işleme hatası: {e}")

        except Exception as e:
            print(f"Arduino bağlantı hatası: {e}")
        finally:
            if 'ser' in locals():
                ser.close()
    
    def closeEvent(self, event):
        """Uygulama kapatılırken yapılacak işlemler."""
        if ser:  # Arduino bağlantısı varsa
            ser.write(b'0')  # Buzzer'ı durdur
            print("Buzzer durduruldu")
        self.running = False  # İş parçacığını durdur
        if self.arduino_thread.is_alive():
            self.arduino_thread.join()  # İş parçacığının kapanmasını bekle
        if self.ser and self.ser.is_open:
            self.ser.close()  # Seri portu kapat
        event.accept()

    @QtCore.pyqtSlot(list, int, float)
    def update_all_data(self, touch_sensors, pulse, temperature):
        try:
            # Dokunma sensörlerini güncelle
            if hasattr(self, 'dot_widget'):
                self.update_sensor_data(touch_sensors)  # Burada update_sensor_data'yı çağırıyoruz
            
            # Nabız ve sıcaklık değerlerini güncelle
            if hasattr(self, 'ui'):
                self.ui.bpm_label.setText(f"Nabız: {pulse} BPM")
                self.ui.temp_label.setText(f"Sıcaklık: {temperature:.1f} °C")
                
                # Direksiyon tutuş uyarılarını kontrol et
                check_steering_grip(touch_sensors, self.ui.warnig_info, self.ser)
                
                # Sıcaklık kontrolü ve uyarı
                if temperature > 39.4:
                    if not self.temp_warning_timer.isActive():
                        self.temp_warning_timer.start(500)  # 500ms'de bir yanıp sönme
                    
                    # Uyarı labelını güncelle ve göster
                    warning_text = f"Ateşiniz {temperature:.1f}°C sürüşünüz önerilmez!"
                    self.warning_label.setText(warning_text)
                    self.warning_label.adjustSize()  # Metne göre boyutu ayarla
                    
                    # Ekranın ortasına yerleştir
                    self.warning_label.move(
                        self.width() // 2 - self.warning_label.width() // 2,
                        self.height() // 2 - self.warning_label.height() // 2
                    )
                    self.warning_label.show()
                else:
                    if self.temp_warning_timer.isActive():
                        self.temp_warning_timer.stop()
                    self.warning_label.hide()
                
            # Nabız kontrolü ve uyarı
            if pulse > 101:
                if not self.pulse_warning_timer.isActive():
                    self.pulse_warning_timer.start(500)  # 500ms'de bir yanıp sönme
                
                # Uyarı labelını güncelle ve göster
                pulse_warning_text = f"Nabzınız {pulse} BPM sürüşünüz önerilmez!"
                self.pulse_warning_label.setText(pulse_warning_text)
                self.pulse_warning_label.adjustSize()  # Metne göre boyutu ayarla
                
                # Ekranın ortasına yerleştir (sıcaklık uyarısının altına)
                self.pulse_warning_label.move(
                    self.width() // 2 - self.pulse_warning_label.width() // 2,
                    (self.height() // 2 - self.pulse_warning_label.height() // 2) + 50  # +50 ile sıcaklık uyarısının altına yerleştir
                )
                self.pulse_warning_label.show()
            else:
                if self.pulse_warning_timer.isActive():
                    self.pulse_warning_timer.stop()
                self.pulse_warning_label.hide()
            
            print(f"GUI güncellendi: Touch={touch_sensors}, BPM={pulse}, Temp={temperature}")  # Debug için
        except Exception as e:
            print(f"GUI güncelleme hatası: {e}")


    def toggle_turn(self):
        if self.toggle:
            self.turn_right()  # turn_right fonksiyonunu çağır
            self.ui.pushButton.setText("Motoru Durdur")  # Sol dönüş, "Motoru Durdur" yazsın
            #self.update_sensor_data()
            self.gif_widget.start()
            sensor_datam = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.ui.warnig_info.setVisible(True)
            self.ui.bpm_label.setVisible(True)
            self.ui.temp_label.setVisible(True)
            check_steering_grip(sensor_datam, self.ui.warnig_info)
            
        else:
            self.turn_left()  # turn_left fonksiyonunu çağır
            self.ui.pushButton.setText("Motoru Çalıştır")  # Sağ dönüş, "Motoru Çalıştır" yazsın
            self.reset_sensor_data()
            self.gif_widget.stop()
            self.ui.warnig_info.setVisible(False)
            self.ui.bpm_label.setVisible(False)
            self.ui.temp_label.setVisible(False)
            
            if ser:  # Arduino bağlantısı varsa
                ser.write(b'0')  # Buzzer'ı durdur
                print("Buzzer durduruldu")


        self.toggle = not self.toggle  # toggle değerini değiştir, sıradaki fonksiyonu çağır

    def turn_left(self):
        self.SpeedometerNeedle.set_angle(self.SpeedometerNeedle.angle - 80)

    def turn_right(self):
        self.SpeedometerNeedle.set_angle(self.SpeedometerNeedle.angle + 80)

    def update_sensor_data(self, touch_sensors=None):
        if touch_sensors is None:
            # Eğer veri gelmezse varsayılan değerleri kullan
            touch_sensors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # DotWidget içindeki renkleri güncelle
        self.dot_widget.update_dot_colors(touch_sensors)

    def reset_sensor_data(self):
        # Örnek sensör verisi
        sensor_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # DotWidget içindeki renkleri güncelle
        self.dot_widget.update_dot_colors(sensor_data)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            # Sağ ok tuşuna basıldı
            self.car_position += 1
            if self.car_position > self.car_max_x:
                self.car_position = self.car_max_x
        elif event.key() == Qt.Key.Key_Left:
            # Sol ok tuşuna basıldı
            self.car_position -= 1
            if self.car_position < self.car_min_x:
                self.car_position = self.car_min_x
        
        # Arabayı yeni pozisyona taşı
        self.ui.car_img.move(self.car_position, self.ui.car_img.geometry().y())

    def toggle_temp_warning(self):
        if self.temp_warning_visible:
            self.warning_label.show()
        else:
            self.warning_label.hide()
        self.temp_warning_visible = not self.temp_warning_visible

    def toggle_pulse_warning(self):
        if self.pulse_warning_visible:
            self.pulse_warning_label.show()
        else:
            self.pulse_warning_label.hide()
        self.pulse_warning_visible = not self.pulse_warning_visible

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()
    sys.exit(app.exec())

