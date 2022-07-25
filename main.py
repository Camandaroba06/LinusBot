from tkinter import *
import tkinter
import serial


# cores
cor1 = "#0a0a0a"  # black / preta
cor2 = "#fafcff"  # white / branca
cor3 = "#21c25c"  # green / verde
cor4 = "#eb463b"  # red / vermelha
cor5 = "#dedcdc"  # gray / Cizenta
cor6 = "#3080f0"  # blue / azul

janela = Tk()
janela.title("")
# janela.geometry('1280x800')
#janela.resizable(width=FALSE, height=FALSE)
janela.configure(background=cor3)

global tempo
tempo = '00:00:00'

count = -5
run = False


# Funcao iniciar
def iniciar():
    global arduino
    arduino = serial.Serial('COM3', 9600)

    def ler():
        leitura_Ard = int(arduino.readline())
        print(leitura_Ard)

    def valor():
        if run:
            global count
            global tempo
            # antes de começar
            if count <= -1:
                inicio = "começando em " + str(abs(count))
                label_time['text'] = inicio
                label_time['font'] = 'Times 120 bold'
            else:
                label_time['font'] = 'Times 200 bold'
                d = str(tempo)
                h, m, s = map(int, d.split(":"))
                h = int(h)
                m = int(m)
                s = int(count)

                if(s > 59):
                    count = 0
                    s = 0
                    m += 1

                s = str(0)+str(s)
                m = str(0)+str(m)
                h = str(0)+str(h)

                d = str(h[-2:])+":"+str(m[-2:])+":"+str(s[-2:])
                label_time['text'] = d
                tempo = d

                s = int(count)
                m = int(m)
                h = int(h)

            label_time.after(1000, valor)
            countAntigo = count
            count += 1
            if count != countAntigo:
                ler()
    valor()


# Função para iniciar


def start():
    global run
    run = True
    iniciar()

# Função para pausar


def stop():
    global run
    run = False

# Função para reiniciar


def reset():
    global count
    count = -5

    # Se estiver pausado ira reiniciar do zero
    if run == False:
        global tempo
        tempo = '00:00:00'
        label_time['text'] = tempo

    # Se nao estiver pausado ira continuar onde parou antes
    else:
        label_time['font'] = 'ivy 20 '
        label_time['text'] = 'Iniciando...'


# Aqui é quando configuramos a visualização da GUI:
label_app = Label(janela, text='cronômetro',
                  font=('Arial 10'), bg=cor1, fg=cor2)
label_app.place(x=20, y=5)

label_time = Label(janela, text=tempo, font=(
    'Times 200 bold'), bg=cor1, fg=cor6)
label_time.grid(row=0, column=0, sticky=NSEW, padx=450, pady=200)

label_app.lift()

frameBaixo = Frame(janela, width=310, height=350, bg=cor1, relief="flat")
frameBaixo.grid(row=1, column=0, pady=0, padx=30, sticky=NSEW)

botao_start = Button(frameBaixo, command=start, text="Iniciar", width=10, height=2,
                     bg=cor1, fg=cor2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
botao_start.grid(row=0, column=0, sticky=NSEW, padx=2, pady=10)

botao_stop = Button(frameBaixo, command=stop, text="Pausar", width=10, height=2,
                    bg=cor1, fg=cor2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
botao_stop.grid(row=0, column=1, sticky=NSEW, padx=2, pady=10)

botao_reset = Button(frameBaixo, command=reset, text="Reiniciar", width=10, height=2,
                     bg=cor1, fg=cor2, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE)
botao_reset.grid(row=0, column=2, sticky=NSEW, padx=2, pady=10)


janela.mainloop()
