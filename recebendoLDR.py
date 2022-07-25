import serial
global arduino
arduino = serial.Serial('COM3', 9600)


def ler():
    global leitura_Ard
    leitura_Ard = int(arduino.readline())


while True:
    ler()
    print(leitura_Ard)
