import serial
import time

arduino = serial.Serial('COM7', 9600) # Adjust 'COM3' to your Arduino's port
time.sleep(2) # Wait for the connection to establish


def control_led(command):
    arduino.write(command.encode())

while True:
    control_led('1')
    time.sleep(1) # Wait for 1 second


    control_led('0')
    time.sleep(1) # Wait for 1 second


arduino.close() # Close the connection

def arduino(clss):
    def control_led(command):
        arduino.write(command.encode())
    arduino = serial.Serial('COM7', 9600) 
    match clss:
        case 0:
            control_led('1')
        case 21:
            control_led('3')
    arduino.close()


from ultralytics import YOLO
import cv2
import math
import serial
import time

def control_led(command):
    arduino.write(command.encode())

# Web Camin Başlatılması
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 800)

# YOLO modelinin eklenmesi
model = YOLO("yolo-Weights/yolov8n.pt")

arduino = serial.Serial('COM7', 9600) # Adjust 'COM3' to your Arduino's port

while True:
    
    # Video kaydının okunması
    success, img = cap.read()
    # Kaydın modele aktarılması
    results = model(img, stream=True)
    
    # Koordinat ve görüntüyü işleme
    # Yolo modelinin verdiği sonucu for döngüsüne atılması
    for r in results:
        # Modelin verdiği sonuçtan algılanan objenin koordinatlarının çekilmesi
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            # Modelin verdiği sonuçtan sadece insan, ayı ve inek için sınırlama
            if cls == 0 or cls == 21 or cls == 19:
                # Sınırlayıcı Kutunun koordinatlarının integer değere çevrilmesi
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Kutuyu görüntüye yerleştirme
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Doğruluk Oranı
                confidence = math.ceil((box.conf[0]*100))/100
                print("Doğruluk --->",confidence)

                # Tanın objelerin isimlerinin tanımlanması
                className = "Tanımlanamadı"
                cls = int(box.cls[0])
                match cls:
                    case 0:
                        control_led('1')
                        className = "Insan"
                    case 19:
                        control_led('2')
                        className = "Inek"

                    case 21:
                        control_led('3')
                        className = "Ayi"
                # Yazı Ayarlaması
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                # Yazıyı görüntüye yerleştirme
                cv2.putText(img, className, org, font, fontScale, color, thickness)     

    cv2.imshow('Kapan Dedektoru', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

from ultralytics import YOLO
import cv2
import serial
import time

def control_led(command):
    arduino.write(command.encode())

# Web kamerasını başlatma
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 800)

# YOLO modelini yükleme
model = YOLO("yolo-Weights/yolov8n.pt")

# Arduino bağlantısını kurma
arduino = serial.Serial('COM7', 9600)  # COM portunu sisteminize göre ayarlayın
time.sleep(2)

insan_algilandi = False
ayi_algilandi = False

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    insan_algilandi = False
    ayi_algilandi = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 0:  # İnsan
                insan_algilandi = True
            elif cls == 21:  # Ayı
                ayi_algilandi = True
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

    if insan_algilandi:
        control_led('1')
    else:
        control_led('0')

    if ayi_algilandi:
        control_led('3')

    cv2.imshow('Kapan Dedektoru', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
