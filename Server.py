import math
import re
import socket
import datetime

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda
serversocket.bind((socket.gethostname(), 1234))  # dowiazanie do portu 1234
serversocket.listen(5)


def setID(): #funkcja tworzaca 6 cyfrowy identyfikator sesji, jest to godzina minuta sekunda polaczenia z uzupelnieniem zerem
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

def switchOperations():
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wyswietlenie wszystkich wykonanych obliczen.")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  #zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "HA",  # wykonywanie wszystkich wykonanych obliczen
    }.get(choice, "Podano nieprawidlowy numer operacji.")

def displayMathOperationsHistorySession():
    print("Tu bedzie wyswietlac historie obliczen w danej sesji")

def displayMathOperationsHistoryOperationID():
    print("Tu bedzie wyswietlac historie obliczen przez ID obliczenia.")

def  displayAllMathOperations():
    print("Tu bedzie wyswietlac wszystkie dotychczas wykonane obliczenia")


def decodeOperationCode(operationCode):
    print("\nOtrzymany kod od klienta: " + operationCode)
    splitedOperationCode = operationCode.split("=", 1)
    statusField = splitedOperationCode[0]
    print("Pole statusu operacji: " + statusField)
    operationField = splitedOperationCode[1]
    operationField = operationField[:-1]  # usuwanie dolara z konca wyrazu
    print("Operacja: " + operationField)


#*** Uruchomienie serwera ***

while 1:
    clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja
    print(f'Polaczono z: ', address)

    clientsocket.send(bytes(str(setID()), 'utf8')) #wysylanie id sesji do klienta

    receivedOperationCode = clientsocket.recv(1024) #testuję wyciaganie poszczegolnych danych z otrzymanego kodu od klienta
    operationCode = str(receivedOperationCode,'utf-8')
    decodeOperationCode(operationCode)

    receivedOperationCode2 = clientsocket.recv(1024)  # testuję wyciaganie poszczegolnych danych z otrzymanego kodu od klienta
    operationCode2 = str(receivedOperationCode2, 'utf-8')
    decodeOperationCode(operationCode2)


    while 1:
        operation = switchOperations()

        if operation == "FN":
            print ("Zakonczono dzialanie programu, rozlaczono z klientem.")
            clientsocket.close()
            break
        elif operation == "HS":
            print("Wyswietlenie historii obliczen przez ID sesji.\n")
            displayMathOperationsHistorySession()
        elif operation == "HO":
            print("Wyswietlenie historii obliczens przez ID obliczen.\n")
            displayMathOperationsHistoryOperationID()
        elif operation == "HA":
            print("Wyswietlenie wszystkich wykonanych dotychczas operacji matematycznych.\n")
            displayAllMathOperations()
        else:
            print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")