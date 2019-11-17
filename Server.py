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

DOcounter = 0
ODcounter = 0
MNcounter = 0
DZcounter = 0
POcounter = 0
LOcounter = 0
IS = 0
IO = 0
OP = 0
OD = 0
Z1 = 0
Z2 = 0

def decodeOperationCode(operationCode):
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2
    if len(operationCode) >= 40:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
        print("\nOtrzymany kod od klienta: " + operationCode)

        splitedOperationCode = operationCode.split("$$", 5)
        IS = splitedOperationCode[0]
        IS = IS[3:]
        print("id sesji: " + IS)
        IO = splitedOperationCode[1]
        IO = IO[3:]
        print("id operacji mat: " + IO)
        OP = splitedOperationCode[2]
        OP = OP[3:]
        print("operacja mat: " + OP)
        OD = splitedOperationCode[3]
        OD = OD[3:]
        print("wynik dzialania: " + OD)
        Z1 = splitedOperationCode[4]
        Z1 = Z1[3:]
        Z1 = int(Z1)
        print("wart z1: " + str(Z1))
        Z2 = splitedOperationCode[5]
        Z2 = Z2[3:-2]
        Z2 = int(Z2)
        print("wart z2: " + str(Z2))
    else:
        print("tutaj bedzie dekodowanie zapytania o historie sesji/konkretengo dzialnia")
    return IS, IO, OP, OD, Z1, Z2


def executeRequest():
    global DOcounter, ODcounter, MNcounter, DZcounter, POcounter, LOcounter
    if OP == 'DO':
        OD = add(Z1, Z2)
        IO = str(IS) + "DO" + str(DOcounter)
    if OP == 'OD':
        OD = subtract(Z1, Z2)
        IO = str(IS) + "OD" + str(ODcounter)
    if OP == 'MN':
        OD = multiply(Z1, Z2)
        IO = str(IS) + "MN" + str(MNcounter)
    if OP == 'DZ':
        OD = divide(Z1, Z2)
        IO = str(IS) + "DZ" + str(DZcounter)
    if OP == 'PO':
        OD = power(Z1, Z2)
        IO = str(IS) + "PO" + str(POcounter)
    if OP == 'LO':
        OD = log(Z1, Z2)
        IO = str(IS) + "LO" + str(LOcounter)

    answerCode = "IS=" + str(IS) + "$$IO=" + str(IO) + "$$OP=" + str(OP) + "$$OD=" + str(OD) + "$$Z1=" + str(Z1) + "$$Z2=" + str(Z2) + "$$"
    print("Utworzona odpowiedz: " + answerCode)
    return answerCode

def listenIncomingRequest():
    receivedOperationCode = clientsocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    return operationCode


def sendIDsessionToClient():
    clientsocket.send(bytes(str(setID()), 'utf8'))


def sendAnswerForRequest():
    clientsocket.send(bytes(str(executeRequest()), 'utf8'))  # wysylanie id sesji do klienta


#*** Uruchomienie serwera ***


while 1:

    clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja
    print(f'Polaczono z: ', address)
    sendIDsessionToClient()  # wysylanie id sesji do klienta
    while 1:
        wybor = input("1.Nawiaz poloczenie, 2.Operacje:")
        if wybor == "1":
            while 1:
                operationCode = listenIncomingRequest()  # nasluchiwanie na przyjscie zapytania
                decodeOperationCode(operationCode)
                sendAnswerForRequest()
        if wybor == "2":
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