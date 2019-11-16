import math
import socket
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda
s.bind((socket.gethostname(), 1234))  # dowiazanie do portu 8888
s.listen(5)


ido = 0  # identyfikator obliczen


def setID():
    nowTime = datetime.datetime.now()
    idHour = str(nowTime.hour)
    idMinute = str(nowTime.minute)
    idSecond = str(nowTime.second)

    if len(idHour) == 1:
        idHour = str(0) + idHour

    if len(idMinute) == 1:
        idMinute = str(0) + idMinute

    if len(idSecond) == 1:
        idSecond = str(0) + idSecond

    id = int(idHour + idMinute + idSecond)

    operationID = "ID=" + str(id) + "$"

    return operationID


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def log(a, b):
    return math.log(a, b)


def power(a, b):
    return math.pow(a, b)


while 1:
    clientsocket, address = s.accept()  # odebranie polaczenia
    print(f'Polaczono z: ', address)

    clientsocket.send(bytes(str(setID()), 'utf8')) #wysylanie id sesji do klienta
