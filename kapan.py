from ultralytics import YOLO
import cv2
import serial
import time
import math

#Function that sends value to Serial Port
def control_led(command):
    arduino.write(command.encode())

# Starting the Web Cam
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('video.mp4')
cap.set(3, 1500)
cap.set(4, 1080)

# Loading the YOLO model
model = YOLO("yolo-Weights/yolov8n.pt")

# Establishing the Arduino connection
arduino = serial.Serial('COM7', 9600) 
time.sleep(2)

while True:
    # Reading video recording
    success, img = cap.read()
    # Transferring the record to the model
    results = model(img, stream=True)

    # Coordinate and image processing
    # Putting the result of the Yolo model into the for loop
    for r in results:
        # Drawing the coordinates of the detected object from the result given by the model
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            # From the result given by the model, there are only limitations for humans, bears and cows.
            if cls == 0 or cls == 21 or cls == 19:
                # Converting the coordinates of the Bounding Box to integer value
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Place the box in the image
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Accuracy rate
                confidence = math.ceil((box.conf[0]*100))/100
                print("Doğruluk --->",confidence)

                # Defining the names of the defined objects
                # Calling the function and sending the values
                className = "Tanimlanamadi"
                match cls:
                    case 0:
                        className = "Insan"
                        control_led('1')
                    case 19:
                        className = "Inek"
                    case 21:
                        className = "Ayi"
                        control_led('3') 

                # Text Adjustment
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Placing the text on the image
                cv2.putText(img, className, org, font, fontScale, color, thickness)  

    cv2.imshow('Kapan Dedektoru', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
