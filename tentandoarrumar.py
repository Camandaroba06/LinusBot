import tkinter as tk
import serial
import threading
import os
pastaApp = os.path.dirname(__file__)


class Cronus(tk.Frame):
    # Aqui fica o construtor da minha classe(onde vou iniciar os trem tudo)---------------------------------------------------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master, bg="Black")
        self.master = master
        self.hilo1 = threading.Thread(target=self.getSensorValues, daemon=True)
        self.arduino = serial.Serial("COM3", 9600, timeout=1.0)
        self.LDRvalue = tk.IntVar()
        self.running = False
        self.update_time = ''
        self.valorAnterior = 6  # o importante é ser diferente de 0 e 1
        self.millis = 0
        self.seconds = 0
        self.minutes = 0
        self.espera = 0
        self.conta_voltas = 1
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
                  + " " "Valor Antigo:" + " " + str(self.valorAnterior) + " " + "Seconds: " + str(self.seconds) + " " + "Running: " + str(self.running) + " " + "Espera: " + str(self.espera) + " " + "Conta_Voltas: " + str(self.conta_voltas))
            aux = self.LDRvalue.split()
            for i in aux:
                self.LDRvalue = int(i)
            # print(self.LDRvalue)
            if((self.LDRvalue != self.valorAnterior) and self.espera > 2):
                if(self.seconds == 0 and self.minutes == 0):
                    self.inicio()
                else:
                    if(self.espera > 200):
                        self.voltas()
                        self.espera = 0
            self.valorAnterior = self.LDRvalue
            self.espera += 1

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
        self.texto_volta1 = tk.Label(
            self.master, text="Volta 1:", font="Arial 30", fg="Black", bg="#80c4e4")
        self.texto_volta1.place(x=50, y=375)
        self.texto_volta2 = tk.Label(
            self.master, text="Volta 2:", font="Arial 30", fg="Black", bg="#80c4e4")
        self.texto_volta2.place(x=50, y=430)
        self.texto_volta3 = tk.Label(
            self.master, text="Volta 3:", font="Arial 30", fg="Black", bg="#80c4e4")
        self.texto_volta3.place(x=50, y=485)
        self.texto_volta4 = tk.Label(
            self.master, text="Volta 4:", font="Arial 30", fg="Black", bg="#80c4e4")
        self.texto_volta4.place(x=50, y=540)
        self.tempo_volta1 = tk.Label(
            self.master, text="00:00:00", font="Times 30", fg="Black", bg="#80c4e4")
        self.tempo_volta1.place(x=200, y=375)
        self.tempo_volta2 = tk.Label(
            self.master, text="00:00:00", font="Times 30", fg="Black", bg="#80c4e4")
        self.tempo_volta2.place(x=200, y=430)
        self.tempo_volta3 = tk.Label(
            self.master, text="00:00:00", font="Times 30", fg="Black", bg="#80c4e4")
        self.tempo_volta3.place(x=200, y=485)
        self.tempo_volta4 = tk.Label(
            self.master, text="00:00:00", font="Times 30", fg="Black", bg="#80c4e4")
        self.tempo_volta4.place(x=200, y=540)

    def voltas(self):

        print("Valor click_lectura: " + str(self.conta_voltas))
        if self.conta_voltas == 1:
            self.tempo_volta1.config(text=' {}:{}:{}'.format(self.minutes, self.seconds, self.millis),
                                     fg='white', bg='#80c4e4')

        elif self.conta_voltas == 2:
            self.tempo_volta2.config(text=' {}:{}:{}'.format(self.minutes, self.seconds, self.millis),
                                     fg='white', bg='#80c4e4')

        elif self.conta_voltas == 3:
            self.tempo_volta3.config(text=' {}:{}:{}'.format(self.minutes, self.seconds, self.millis),
                                     fg='white', bg='#80c4e4')

        elif self.conta_voltas == 4:
            self.tempo_volta4.config(text=' {}:{}:{}'.format(self.minutes, self.seconds, self.millis),
                                     fg='white', bg='#80c4e4')
        self.conta_voltas += 1
        self.minutes, self.seconds, self.millis = 0, 0, 0
        self.label_TIME.config(text='00:00:00')

    def inicio(self):
        if not self.running:
            print("Chamei o update")
            self.update()
            self.running = True

    def pause(self):
        # Tirei o if running:
        self.label_TIME.after_cancel(self.update_time)
        self.running = False

        print("Pausou!!!!")

    # Aqui é a função que irá atualizar meus números no GUI
    def update(self):
        if self.running:
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
