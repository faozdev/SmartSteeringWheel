# SteerWise Projesi

SteerWise, akıllı direksiyon simidi uygulamasıdır. Bu uygulama, kullanıcıların direksiyon tutuş pozisyonlarını izleyerek güvenli sürüş deneyimi sağlamayı amaçlar. Uygulama, PyQt6 kütüphanesi kullanılarak geliştirilmiştir ve Arduino ile entegre çalışmaktadır.

## İçindekiler

- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Dosya Yapısı](#dosya-yapısı)
- [Geliştirici Notları](#geliştirici-notları)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install PyQt6 Pillow pyserial
   ```

2. Arduino'yu bağlayın ve uygun portu ayarlayın. `MainWindow` sınıfında `self.arduino_port` değişkenini güncelleyin.

3. Uygulamayı çalıştırın:
   ```bash
   python main.py
   ```

## Kullanım

- Uygulama açıldığında bir yükleme ekranı görüntülenir. Yükleme tamamlandığında ana pencere açılır.
- Ana pencerede, direksiyon simidi ve hız göstergesi görüntülenir.
- Kullanıcı, direksiyonu sağa veya sola döndürmek için butona tıklayabilir.
- Uygulama, kullanıcının direksiyon tutuş pozisyonunu izler ve uygun pozisyonu sağlamazsa uyarılar gösterir.

## Dosya Yapısı

- `main.py`: Uygulamanın ana giriş noktasıdır. Yükleme ekranı ve ana pencereyi içerir.
- `main_screen.py`: Ana pencere arayüzünü tanımlar. Hız göstergesi, direksiyon simidi ve uyarı etiketlerini içerir.
- `loading_screen.py`: Uygulama açıldığında gösterilen yükleme ekranı arayüzünü tanımlar.

## Geliştirici Notları

- Uygulama, PyQt6 kullanılarak geliştirilmiştir. UI bileşenleri, `QWidget`, `QLabel`, `QPushButton` gibi sınıflar kullanılarak oluşturulmuştur.
- Arduino ile iletişim için `pyserial` kütüphanesi kullanılmıştır. Sensör verileri, ana iş parçacığında okunur ve GUI güncellemeleri yapılır.
- Uygulama, kullanıcıdan gelen sensör verilerine göre dinamik olarak tepki verir ve kullanıcıyı bilgilendirir.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.
