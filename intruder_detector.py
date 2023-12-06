import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from matplotlib import cm

FILE_NAME = "video1.mp4"
WIDTH = 1280
HEIGHT = 720

vidCap = cv2.VideoCapture(f'Video/{FILE_NAME}')

vidCap.set(3,WIDTH)
vidCap.set(4,HEIGHT)

ret, frame1 = vidCap.read()
ret, frame2 = vidCap.read()
##################

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self._draw_image()

    def _draw_image(self):
        img_cv2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        self.im = Image.fromarray(img_cv2)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        #one rectangle
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, )

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        global app

        global xStart
        global yStart
        global xEnd
        global yEnd

        xStart = self.start_x
        yStart = self.start_y
        xEnd = event.x
        yEnd = event.y
        app.quit()

xStart = 0
yStart = 0
xEnd = 0
yEnd = 0

app = ExampleApp()
app.mainloop()

########################

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
    cv2.rectangle(frame1, (xStart, yStart), (xEnd, yEnd), (0, 0, 255), 2)
    cv2.imshow("frame1", frame1)
    frame1 = frame2  #
    ret, frame2 = vidCap.read() #  
 
    if cv2.waitKey(40) == 27:
        break

vidCap.release()
cv2.destroyAllWindows()