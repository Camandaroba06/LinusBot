import serial
import time
from tkinter import *
import os


arduino = serial.Serial("COM3", 9600)
pastaApp = os.path.dirname(__file__)


gui = Tk()
gui.title("Tentando usar tkinter no arduino")
gui.geometry("1366x768")
# jpeg da erro, então faz o favor de converter e taca aqui
images = PhotoImage(file=pastaApp+"\\imgLogo.png")
label_image = Label(gui, image=images)
label_image.pack()
while True:
    valorLDR = arduino.readline()
    ldr = Label(gui, text=valorLDR, font=("Arial", 20))
    ldr.place(x=150, y=110)
    gui.update()
