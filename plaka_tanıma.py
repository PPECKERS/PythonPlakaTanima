from os import system
import cv2
import pygame
import imutils
import numpy as np
import pytesseract

plaka = []

while True:
    secenek = input("1-Sisteme plaka kaydet\n2-Sistemden plaka sil\n3-Plaka sorgula\n4-Bütün plakaları sorgula\n5-Kapıdan giriş\nLütfen bir seçenek seçiniz: ")
    if secenek == "1":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        img = cv2.imread('A:\Yazilim\Plaka_Tanima\image_path/40.jpg', cv2.IMREAD_COLOR) # görüntü renkli olsun size
        img = cv2.resize(img, (600,400)) # daha kolay işleme için   
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # tasaruf kolaylık
        gray = cv2.bilateralFilter(gray, 13, 15, 15) # gürültüyü azaltma, netlik 1. ci filtre boyutu 2. benzerlik 3. uzamsal benzerlik
        edged = cv2.Canny(gray, 30, 200) # cv2.canny kenar tespit
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # CHAIN konturları yaklaşıklık temsili # RETR_TREE çeşitli konturları toplayıp analiz
        contours = imutils.grab_contours(contours)  # bu ifade kontur değişkeni zaten konturdaysa geri döndürür
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10] # keyler konturların alanı oluyor en buyuk 10 konturu sıralıyor reverse = True da huyukten kucuge
        screenCnt = None #plaka bulanana kadar konturunu temsil eder konturun köşe noktalarını saklamak ve ileride bu noktalara erişmek için kullanılan bir araçtır.

        for c in contours:
            peri = cv2.arcLength(c, True) # kontur çevresini ölçer # True : kapalı kontur
            approx = cv2.approxPolyDP(c, 0.018 * peri, True) # Konturun yaklaşık bir poligonla temsil edilmesini sağlar yani noktaları birleştirip köşe yaparak daha kolay temsil ettirir , 0.018 birim hata toleransıdır
            if len(approx) == 4: # poligon un 4 köşeli olmasını teyit # poligon birbirine bağlı çokgen
                screenCnt = approx # approx un köşe noktalarını saklıyor

        if screenCnt is not None:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3) # screenCnt boş değilse img e -1 konturunda (tüm konturlarda) çizilmesini sağlar , 255 rengi (kırmızı) 3 çizgi kalınlığı

            mask = np.zeros(gray.shape, np.uint8) # mask çizim için
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1) # 0 çizilicek konturun indeksi 255 beyaz renk pikselleri kullanarak kontur işaretleme , -1 de konturun içini dolduruyor tüm konturların içini doldurmayı sağlar çünkü birsürü olabilir hepsi dolsun

            new_image = cv2.bitwise_and(img, img, mask=mask) #  Bu işlem, maskenin beyaz piksellerine (255 değeri) karşılık gelen pikselleri img görüntüsündeki değerleriyle korurken siyahı korumaz plakadaki harfleri ayırmak için
            (x, y) = np.where(mask == 255) # Bu adım, maske içindeki beyaz piksellerin konumunu belirlemek için kullanılır.
            (topx, topy) = (np.min(x), np.min(y)) # kullanılarak sınırlayıcı dikdörtgenin sol üst köşe noktasının koordinatları (topx, topy) belirlenir.
            (bottomx, bottomy) = (np.max(x), np.max(y)) # kullanılarak sınırlayıcı dikdörtgenin sağ alt köşe noktasının koordinatları 
            Cropped = gray[topx:bottomx+1, topy:bottomy+1] #  Bu satırda, gray görüntüsünden sınırlayıcı dikdörtgen içindeki bölgeyi almak için dilimleme işlemi yapılır. 
            #  Bu sayede, belirli bir nesne veya bölge üzerinde daha spesifik işlemler yapmak için ilgili bölgeye odaklanılabilir.

            text = pytesseract.image_to_string(Cropped, config='--psm 11').replace('"', '').strip() # psm 11 OCR işlemi için kullanılan Tesseract OCR motorunun yapılandırmasını belirtir.
            print("Plaka Tanima Programlamasi\n") # ('"', '').strip() tırnagı kaldırıyor # Tesseract OCR motorunu tek sütunlu metinler için yapılandırır ve plaka numarasını doğru şekilde çıkarmak için uygun bir ayarlama sağlar.
            print("Plaka Numarasi:", text)
            plaka.append(text)
            print(plaka)

        else:
            print("Plaka bulunamadi")

        img = cv2.imshow('Plaka Tespiti', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("İşlem başarılı! Ana ekrana dönmek için herhangi bir tuşa basınız.")
        input()

    if secenek == "2":
        secenek2 = input("Silmek istediğiniz plakanın ilk 2 hanelerini giriniz (01 ORN) gibi numarasını giriniz : ")
        indexler = [i for i, plaka_kodu in enumerate(plaka) if plaka_kodu.startswith(secenek2)] #  enumerate() işlevi, liste öğelerinin indekslerini ve değerlerini döndürür. 
        if indexler:
            for i in sorted(indexler, reverse=True):# indexler listesindeki indekslerin üzerinde tersten (azalan sırada) dolaşılır.
                del plaka[i]
            print("Plaka silme işlemi başarılı.")
        else:
            print("Plaka bulunamadı.")
            print(plaka)
    print("Ana ekrana dönmek için herhangi bir tuşa basınız.")
    input()
    system("cls")

    if secenek == "3":
        secenek3 = input("Sorgulanacak plakayı giriniz : ")
        sonuc = secenek3 in plaka 
        if sonuc == True:
            print("Bu plaka sistemimizde bulunuyor")
            print("İşlemi başarılı ana ekrana dönmek için herhangi bir tuşa basınız: ")
            input()
            system("cls")
        else:
                print("Böyle bir plaka yok...")
    print(plaka)

    if secenek == "4":
        print(f"Bütün kayıtlı plakalarımız : {plaka}")
        print("İşlemi başarılı ana ekrana dönmek için herhangi bir tuşa basınız: ")
        input()
        system("cls")
    
    if secenek == "5":
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                break
                
            Cropped = frame[0:400, 0:400]
            text = pytesseract.image_to_string(Cropped, config='--psm 11').strip()
            if text in plaka:
                print("Plakanın numarası onaylandı, kapı açılıyor.")
                print(text)
                pygame.init()
                width = 500
                height = 500
                screen = pygame.display.set_mode((width, height))
                pygame.display.set_caption("Onay")
                GREEN = (0, 255, 0)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                    screen.fill((255, 255, 255))
                    pygame.draw.circle(screen, GREEN, (width // 2, height // 2), 100)
                    pygame.display.update()
                
                break

            else:
                print("Plaka listede bulunamadı.")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        print("Geçersiz seçenek! Lütfen tekrar deneyin.")

        print(plaka)
        print("Ana ekrana dönmek için herhangi bir tuşa basınız.")
        input()
        system("cls")