from pyrsistent import v
from stopwatch import Stopwatch
import serial
arduino = serial.Serial("COM3", 9600, timeout=1.0)
running = False
espera = 0
conta_voltas = 0
minut = 0
segundos = 0
millis = 0
valorAnterior = -1
# Argument specifies decimal precision for __str__
# e.g 2 digits = 1.00, 3 digits = 1.000
# Optional, defaults to 2
stopwatch = Stopwatch(2)  # Start a stopwatch
# It's just math with time.perf_counter() so there isn't really a task
# running in background

# stopwatch.stop()  # Stop stopwatch, time freezes
# stopwatch.start()  # Start it again
# stopwatch.reset()  # Reset it back to 0
# stopwatch.restart()  # Reset and start again
# stopwatch.running  # Wether stopwatch is running
# x = stopwatch.duration  # Get the duration (in seconds)
while True:
    # Aqui recebo a informação do arduino e trato ela(tive q usar o for para tratar pq ela chegava em muitos bits por vez, assim eu consegui dividir ela, tratar e atribuir dnv)
    LDRvalue = arduino.readline()[:-2].decode()
    # esse text para concatenar tem q ser quando ainda era string, ou seja, antes dos aux, for e etc
    # label_ldr.config(text='Valor do LDR:' + LDRvalue)
    print("Valor Novo:" + " " + LDRvalue
          + " " "Valor Antigo:" + " " + str(valorAnterior) + " " + "Seconds: " + str(segundos) + " " + "Running: " + str(running) + " " + "Espera: " + str(espera) + " " + "Conta_Voltas: " + str(conta_voltas))
    aux = LDRvalue.split()
    for i in aux:
        LDRvalue = int(i)
    if(valorAnterior != LDRvalue):
        if(segundos == 0 and millis == 0 and espera > 5):
            stopwatch.start()
            running = True
        else:
            if(espera > 200):
                stopwatch.restart()

    if running:
        totalSec = stopwatch.duration

        millisTotal = 1000*totalSec
        # print(millisTotal)
        segundos = int(millisTotal/1000)
        minutos = int(millisTotal/60000)
        millis = int(millisTotal)
        if(segundos >= 59):
            segundos = segundos % 60
        if(millis >= 999):
            millis = millis % 1000
        print("Min: " + str(minutos) + " " + "Segundos: " +
              str(segundos)+" " + "Milisegundos: " + str(millis))

    valorAnterior = LDRvalue
    espera += 1

    # converti os segundos para valores inteiros. Ou faço isso depois ?
    # totalSec = int(totalSec)
    # # millis = seg*1000  # Valor de millis ?
    # # if seg >= 59.99:
    # #     minut += 1
    # #     stopwatch = Stopwatch(2)
    # if totalSec >= 59.99:
    #     secAtualizado = int(totalSec % 60)
    #     if secAtualizado == 59:
    #         minut += 1
    # else:
    #     secAtualizado = int(totalSec)
    # # print(secAtualizado)
    # print("Minutos: " + str(minut) + " " "Segundos: " + str(secAtualizado))

    # # Get a friendly duration string
    # print("Minutos: " + str(minut) + " " "Segundos: " +
    #       str(seg) + " " + "MilliSeconds: " + str(millis))
    # print(type(x))
