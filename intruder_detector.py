import cv2
import tkinter
from PIL import Image, ImageTk

FILE_NAME = "video1.mp4"


vidCap = cv2.VideoCapture(f'Video/{FILE_NAME}')

vidCap.set(3,1280)
vidCap.set(4,700)

canvas = tkinter.Canvas(width=512, height=512, cursor="cross")
canvas.pack(side="top", fill="both", expand=True)
canvas.bind("<ButtonPress-1>", self.on_button_press)
canvas.bind("<B1-Motion>", self.on_move_press)
canvas.bind("<ButtonRelease-1>", self.on_button_release)

rect = None

start_x = None
start_y = None

_draw_image()

ret, frame1 = vidCap.read()
ret, frame2 = vidCap.read()

while vidCap.isOpened():
    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров

    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY) # метод для выделения кромки объекта белым цветом
 
    dilated = cv2.dilate(thresh, None, iterations = 3) # данный метод противоположен методу erosion(), т.е. эрозии объекта, и расширяет выделенную на предыдущем этапе область
    
    # CHAIN_APPROX_SIMPLE
    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # нахождение массива контурных точек
    
    
    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат
    
        # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить
        print(cv2.contourArea(contour))
    
        if cv2.contourArea(contour) < 700: # условие при котором площадь выделенного объекта меньше 700 px
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
        cv2.putText(frame1, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) # вставляем текст
    
    # cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2) # также можно было просто нарисовать контур объекта
    
    cv2.imshow("frame1", frame1)
    frame1 = frame2  #
    ret, frame2 = vidCap.read() #  
 
    if cv2.waitKey(40) == 27:
        break

vidCap.release()
cv2.destroyAllWindows()