import cv2
import numpy as np
import serial
y1 = 0
y2 = 0
y3 = 0
COM = 'COM5'
BAUD = 9600
ser = serial.Serial(COM, BAUD)

cap = cv2.VideoCapture(0)
azulBajo = np.array([30, 90, 20], np.uint8)
azulAlto = np.array([80, 255, 255], np.uint8)
while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(frameHSV, azulBajo, azulAlto)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (0, 255, 0), 4)

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 1000:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                y = int(M['m01'] / M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

                if 300 <= x <= 520:
                    if y1 == 0:
                        print("Moviendo a la izquierda")
                        y2 = 0
                        y3 = 0
                        y1 = 1
                    ser.write(b"izq\n")
                elif 100 <= x <= 300:
                    ser.write(b"izq1\n")
                elif x < 100:
                    ser.write(b"izq2\n")
                elif 800 >= x >= 650:
                    if y2 == 0:
                        print("Moviendo a la derecha")
                        y1 = 0
                        y3 = 0
                        y2 = 1
                    ser.write(b"der\n")
                elif 1950 >= x >= 800:
                    ser.write(b"der1\n")
                elif x > 1950:
                    ser.write(b"der2\n")
                else:
                    if y3 == 0:
                        print("El objeto esta centrado")
                        y2 = 0
                        y1 = 0
                        y3 = 1

        # cv2.imshow('mascaraAzul', mascara)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            ser.close()
            break
cap.release()
cv2.destroyAllWindows()
