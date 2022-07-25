import tkinter as tk
import serial
import threading
import os
pastaApp = os.path.dirname(__file__)


class Cronus(tk.Frame):
    # Aqui fica o construtor da minha classe(onde vou iniciar os trem tudo)---------------------------------------------------------------------------------------------------
    def _init_(self, master=None):
        super()._init_(master, bg="Black")
        self.master = master
        self.hilo1 = threading.Thread(target=self.getSensorValues, daemon=True)
        self.arduino = serial.Serial("COM3", 9600, timeout=1.0)
        self.LDRvalue = 1
        self.running = False
        self.update_time = ''
        self.valorAnterior = 6  # o importante é ser diferente de 0 e 1
        self.millis = 0
        self.seconds = 0
        self.minutes = 0
        self.create_widgets()
        self.hilo1.start()
        # self.update()

    # Esse método leio a informação do arduino(no caso LDR)

    def getSensorValues(self):
        while True:
            # Aqui recebo a informação do arduino e trato ela(tive q usar o for para tratar pq ela chegava em muitos bits por vez, assim eu consegui dividir ela, tratar e atribuir dnv)
            self.LDRvalue = self.arduino.readline()[:-2].decode()
            # esse text para concatenar tem q ser quando ainda era string, ou seja, antes dos aux, for e etc
            self.label_ldr.config(text='Valor do LDR:' + self.LDRvalue)
            print("Valor Novo:" + " " + self.LDRvalue
                  + " " "Valor Antigo:" + " " + str(self.valorAnterior) + " " + "Seconds: " + str(self.seconds) + " " + "Running: " + str(self.running))
            aux = self.LDRvalue.split()
            for i in aux:
                self.LDRvalue = int(i)
            # print(self.LDRvalue)
            # if(self.valorAnterior == self.LDRvalue):
            #     continue
            if((self.valorAnterior == 1 and self.LDRvalue == 0) and self.seconds > 5):
                self.pause()

            elif (self.valorAnterior == 1 and self.LDRvalue == 0 and self.running == False and self.seconds == 0):
                self.inicio()
                print("Começouuu!!!")
            self.valorAnterior = self.LDRvalue

    # Esse método(ou função) cria meus Labels, textos e frames ---------------------------------------------------------------------------------------------------------------

    def create_widgets(self):
        self.master.geometry('1280x720')
        self.master.resizable(0, 0)
        self.frame1 = tk.Frame(self.master, borderwidth=1, relief="raise")
        self.frame1.place(x=10, y=10)
        self.images = tk.PhotoImage(file=pastaApp+"\\imgLogo.png")
        self.label_image = tk.Label(self.master, image=self.images)
        self.label_image.grid(row=0, column=0)
        self.label_TIME = tk.Label(
            self.master, text="00:00:00", font="Arial 80", bg="#80c4e4")
        self.label_TIME.place(x=150, y=150)
        self.label_ldr = tk.Label(
            self.master, text="Valor do LDR:", font="Times 40", bg="#80c4e4")
        self.label_ldr.place(x=140, y=20)
        self.pause_button = tk.Button(
            self.master, text='pause', height=2, width=7, font=('Arial', 20), command=self.pause)
        self.pause_button.place(x=10, y=10)

    def inicio(self):
        if not self.running:
            self.update()
            self.running = True

    def pause(self):
        # Tirei o if running:
        self.label_TIME.after_cancel(self.update_time)
        self.running = False
        print("Pausou!!!!")

    def reset(self):
        if self.running:
            self.label_TIME.after_cancel(self.update_time)
            self.running = False
            self.minutes, self.seconds, self.millis = 0, 0, 0
            self.label_TIME.config(text='00:00:00')

    # Aqui é a função que irá atualizar meus números no GUI
    def update(self):
        # if self.running:
        self.millis += 4
        # tive que colocar 4, pq ele n consegue fazer tão proximo de um relógio normal, então fui testando até se aproximar fds
        # provavelmente por causa do tempo de execução de todo o código, aumentando consideravelmente o erro
        if self.millis == 1000:
            self.seconds += 1
            self.millis = 0
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        millis_string = f'{self.millis}'
        # print(minutes_string + ':' + seconds_string + ':' + millis_string)
        self.label_TIME.config(
            text=minutes_string + ':' + seconds_string + ':' + millis_string)
        self.update_time = self.label_TIME.after(1, self.update)


root = tk.Tk()
app = Cronus(master=root)
app.mainloop()
