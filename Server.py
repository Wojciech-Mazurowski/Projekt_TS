import math
import re
import socket
import datetime
import sys
import time
from _datetime import datetime
from time import sleep

IPw = input("Podaj IP serwera: ")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda
serversocket.bind((IPw, 1234))  # dowiazanie do portu 1234
serversocket.listen(5)

currentSessionID = "0"


def setID():  # funkcja tworzaca 6 cyfrowy identyfikator sesji, jest to godzina minuta sekunda polaczenia z uzupelnieniem zerem
    global currentSessionID
    nowTime = datetime.now()
    idHour = str(nowTime.hour)
    idMinute = str(nowTime.minute)
    idSecond = str(nowTime.second)
    nowTime = datetime.now()

    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")

    if len(idHour) == 1:
        idHour = str(0) + idHour

    if len(idMinute) == 1:
        idMinute = str(0) + idMinute

    if len(idSecond) == 1:
        idSecond = str(0) + idSecond

    id = str(idHour + idMinute + idSecond).zfill(6)

    currentSessionID = id
    operationID = "ID=" + str(id) + "$ST=" + "OK" + "$OP=" + "ID$" + "ZC=" + str(ZC) + "$"
    print("kod ID: " + str(operationID))

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
    print("3. Wyswietlenie wszystkich wykonanych obliczen. ")
    choice = input("\nWybierz operacje do wykonania (podaj numer):  ")

    return {

        '0': "FN",  # zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "HA",  # wykonywanie wszystkich wykonanych obliczen
    }.get(choice, "Podano nieprawidlowy numer operacji.")


operationInSessionHistory = []  # lista stringow z operacjami

operationHistory = []


def displayMathOperationsHistorySession():

    operation = input("Podaj 6-cyfrowy ID sesji aby wyswietlic wykonane operacje: \n")

    while len(operation) != 6:
        operation = input("ID sesji jest niewlasciwy, sprobuj ponownie: \n")
    matcher = str(operation)
    findOperation = list(filter(lambda x: matcher in x, operationHistory))

    if len(findOperation) != 0:

        print('\n'.join(operationHistory))
    else:

        print("\nNie znaleziono wskazanej sesji.\n")


def displayMathOperationsHistoryOperationID():

    operation = input("Podaj 3-znakowy ID operacji do wyswietlenia: \n")

    while len(operation) < 3:

        operation = input("ID operacji matematycznej jest niewlasciwy, sprobuj ponownie: \n")

    matcher = str(operation)
    matcher2 = str(ID)
    findOperation = list(filter(lambda x: matcher2 in x, operationHistory))

    if len(findOperation) != 0:
        findOperation2 = list(filter(lambda x: matcher in x, operationHistory))

        if len(findOperation2) != 0:
            print('\n'.join(operationHistory))
        else:
            print("\nNie znaleziono wskazanej operacji.\n")

    else:
        print("\nNie znaleziono wskazanej operacji.\n")


def displayAllMathOperations():

    if len(operationHistory) == 0:
        print("Historia operacji jest pusta.\n")

    else:
        print("\nWykonane dzialania matematyczne od momentu uruchomienia serwera: \n")
        print('\n'.join(operationHistory))


DOcounter = 1
ODcounter = 1
MNcounter = 1
DZcounter = 1
POcounter = 1
LOcounter = 1


ID = 0
ST = 0
IO = 0
OP = 0
OD = 0
WY = 0
Z1 = 0
Z2 = 0
HS = 0
HI = 0
UN = 0
ZC = 0


def decodeOperationCode(operationCode):

    global ID
    global ST
    global IO
    global OP
    global OD
    global Z1
    global Z2
    global WY
    global HS
    global HI
    global UN
    global ZC
    global X
    global DOcounter, ODcounter, MNcounter, DZcounter, POcounter, LOcounter

    operationCode = operationCode.split("$", 20)
    print("kod od klienta: " + str(operationCode))
    matcher = "OP"

    findOperation = list(filter(lambda x: matcher in x, operationCode))
    kod = findOperation[0]
    kod = kod[3:]
    OP = kod
    X = operationCode[3]

    if kod == "RE":
        DOcounter = 1
        ODcounter = 1
        MNcounter = 1
        DZcounter = 1
        POcounter = 1
        LOcounter = 1
        operationInSessionHistory.clear()

    if kod == "dodawaj" or kod == "odejmuj" or kod == "mnoz" or kod == "dziel" or kod == "poteguj" or kod == "logarytmuj":

        splitedOperationCode = operationCode
        #print("Otrzymany kod od klienta: " + operationCode)

        ID = splitedOperationCode[0]
        ID = ID[3:]
        print("ID: " + ID)

        ST = splitedOperationCode[1]
        ST = ST[3:]
        print("ST: " + ST)

        IO = splitedOperationCode[2]
        IO = IO[3:]
        print("IO: " + IO)

        OP = splitedOperationCode[3]
        OP = OP[3:]
        print("OP: " + OP)

        Z1 = splitedOperationCode[4]

        Z1 = Z1[3:]
        print("Z1: " + Z1)
        Z1 = int(Z1)

        Z2 = splitedOperationCode[5]
        Z2 = Z2[3:]
        print("Z2: " + Z2)
        Z2 = int(Z2)

        ZC = splitedOperationCode[6]
        ZC = ZC[3:-1]
        print("ZC: " + ZC)

    if kod == "HI" or kod == "HS":

        #print("\nTestowy print zebym widzial co przychodzi - Otrzymany kod od klienta historia: " + operationCode)
        splitedOperationCode = operationCode
        #print(splitedOperationCode)
        ID = splitedOperationCode[0]
        ID = ID[3:]

        ST = splitedOperationCode[1]

        print("ST przed oczyszczeniem: " + ST)
        ST = ST[3:]
        print("ST " + ST)
        OP = splitedOperationCode[2]
        OP = OP[3:]

        if OP == "HS":

            HS = splitedOperationCode[3]
            HS = HS[3:-1]
            # print("hHS: " + HS)

        if OP == "HI":

            HI = splitedOperationCode[3]
            HI = HI[3:-1]
            # print("hHI: " + HI)

        ZC = splitedOperationCode[4]
        ZC = ZC[3:-1]


def executeRequest():

    global DOcounter, ODcounter, MNcounter, DZcounter, POcounter, LOcounter, OD, WY, ST, OP, ZC, IO, X
    if OP == "FN":
        sys.exit()
    if OP == "RE":
        return setID()
    if OP == "dodawaj" or OP == "odejmuj" or OP == "mnoz" or OP == "dziel" or OP == "poteguj" or OP == "logarytmuj":

        if OP == 'dodawaj':

            WY = add(Z1, Z2)

            IO = "dodawaj" + str(DOcounter)

            DOcounter += 1

            ST = "OK"

        if OP == 'odejmuj':

            WY = subtract(Z1, Z2)

            IO = "odejmuj" + str(ODcounter)

            ODcounter += 1

            ST = "OK"

        if OP == 'mnoz':

            WY = multiply(Z1, Z2)

            IO = "mnoz" + str(MNcounter)

            MNcounter += 1

            ST = "OK"

        if OP == 'dziel':

            if Z2 != 0:

                WY = divide(Z1, Z2)

                IO = "dziel" + str(DZcounter)

                DZcounter += 1

                ST = "OK"

            else:

                print("dzielenie przez zero")

                ST = "ER"

                WY = "null"

        if OP == 'poteguj':

            WY = power(Z1, Z2)

            IO = "poteguj" + str(POcounter)

            POcounter += 1

            ST = "OK"

        if OP == 'logarytmuj':

            if Z1 <= 0 or Z1 == 1 or Z2 <= 0:

                print("dzielenie przez zero")
                ST = "ER"
                WY = "null"
            else:
                WY = log(Z2, Z1)
                IO = "logarytmuj" + str(LOcounter)
                LOcounter += 1
                ST = "OK"

        setMathOperation()

        nowTime = datetime.now()
        year = nowTime.strftime("%Y")
        month = nowTime.strftime("%m")
        day = nowTime.strftime("%d")
        time = nowTime.strftime("%H:%M:%S")
        ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
        #print("ZC: " + ZC)

        putToHistory(ZC)
        answerCode = "ID=" + str(ID) + "$ST=" + str(ST) + "$IO=" + str(IO) + "$OP=" + str(OP) + "$WY=" + str(

            WY) + "$ZC=" + str(ZC) + "$"

        print("\nUtworzona odpowiedz: " + answerCode + "\n")

        return answerCode



    #print("od klienta: " + operationCode)

    if OP == "HS":  # odpowiedz klienta na zapytanie o historie sesji

        nowTime = datetime.now()
        year = nowTime.strftime("%Y")
        month = nowTime.strftime("%m")
        day = nowTime.strftime("%d")
        time = nowTime.strftime("%H:%M:%S")
        ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")

        matcher = str(HS)
        findOperation = list(filter(lambda x: matcher in x, operationHistory))

        if len(findOperation) != 0:
            print("ilosc znalezionych operacji w hs: " + str(len(findOperation)))
            answerCode = "ID=" + str(ID) + "$ST=OK" + "$OP=HS" + "$ZC=" + str(ZC) + "$" + "NR=" + str(len(findOperation)) + "$"
            clientsocket.send(bytes(answerCode, "utf-8"))
            for x in findOperation:
                clientsocket.send(bytes(x, "utf-8"))
                sleep(0.1)
                print("minal sleep na 50 milisekund,  wyslana operacja: " + str(x))

            #answerCode = "ID=" + str(ID) + "$ST=OK" + "$OP=HS" + "$HS=" + str(stringHistory) + "$ZC=" + str(ZC) + "$"
        else:
            print("\nNie znaleziono wskazanej sesji.\n")
            info = "Nie znaleziono wpisow dla podanej sesji."

            nowTime = datetime.now()
            year = nowTime.strftime("%Y")
            month = nowTime.strftime("%m")
            day = nowTime.strftime("%d")
            time = nowTime.strftime("%H:%M:%S")
            ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")

            answerCode = "ID=" + str(ID) + "$ST=ER" + "$OP=HS" + "$ZC=" + str(ZC) + "$"
            clientsocket.send(bytes(answerCode, "utf-8"))

        return 0



    if OP == "HI":

        matcher2 = str(HI)
        findOperation2 = list(filter(lambda x: matcher2 in x, operationInSessionHistory))

        X = int(re.search(r'\d+', X).group())
        print("X TO: " + str(int(X)))
        print("Wielkosc to: " + str(int(len(findOperation2))))

        if len(findOperation2) != 0 and int(X) <= int(len(findOperation2)):
            nowTime = datetime.now()
            year = nowTime.strftime("%Y")
            month = nowTime.strftime("%m")
            day = nowTime.strftime("%d")
            time = nowTime.strftime("%H:%M:%S")
            ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
            answerCode = "ID=" + str(ID) + "$ST=OK" + "$OP=HI" + "$ZC=" + str(ZC) + "$"
            clientsocket.send(bytes(answerCode, "utf-8"))


            anwser = findOperation2[X-1]
            print("WITAM " + anwser)
            clientsocket.send(bytes(anwser, "utf-8"))
            print("wyslana operacja: " + findOperation2[0])

            nowTime = datetime.now()
            year = nowTime.strftime("%Y")
            month = nowTime.strftime("%m")
            day = nowTime.strftime("%d")
            time = nowTime.strftime("%H:%M:%S")
            ZC = nowTime.strftime("%d/%m/%Y, %H:%M:%S")


        else:

            print("\nNie znaleziono wskazanej operacji.\n")
            info = "null"

            nowTime = datetime.now()
            year = nowTime.strftime("%Y")
            month = nowTime.strftime("%m")
            day = nowTime.strftime("%d")
            time = nowTime.strftime("%H:%M:%S")
            ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
            print("ZC: " + ZC)

            answerCode = "ID=" + str(ID) + "$ST=" + "ER" + "$OP=" + "HI" + "$HI=" + "null" + "$ZC=" + str(ZC) + "$"
            sleep(0.1)
            clientsocket.send(bytes(answerCode, "utf-8"))
            print("odpowiedz do klienta na id operacji nie znaleziono: " + str(answerCode))

        return 0





def listenIncomingRequest():

    receivedOperationCode = clientsocket.recv(1024)

    operationCode = str(receivedOperationCode, 'utf-8')

    return operationCode





def sendIDsessionToClient():

    clientsocket.send(bytes(str(setID()), 'utf8'))





def sendAnswerForRequest():
    odpowiedz = executeRequest()
    if str(odpowiedz) != "0":
        clientsocket.send(bytes(str(odpowiedz), 'utf8'))


def putToHistory(ZC):

    global operationHistory, operationInSessionHistory

    mathOperation = "ID=" + str(ID) + "$IO=" + str(IO) + "$OP=" + str(OP) + "$Z1=" + str(Z1) + "$Z2=" + str(

        Z2) + "$WY=" + str(WY) + "$ZC=" + str(ZC) + "$"

    operationHistory.append(mathOperation)  # dodanie do historii sesji
    print("historia sesji: " + str(operationHistory))
    operationInSessionHistory.append(mathOperation)



def setMathOperation():

    global OP

    if OP == "DO":

        operation = "Dodawanie"

    if OP == "OD":

        operation = "Odejmowanie"

    if OP == "MN":

        operation = "Mnozenie"

    if OP == "DZ":

        operation = "Dzielenie"

    if OP == "PO":

        operation = "Potegowanie"

    if OP == "LO":

        operation = "Logarytmowanie"





# *** Uruchomienie serwera ***





while 1:



    clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja

    startTime = time.time()

    print('Polaczono z: ', address)

    sendIDsessionToClient()  # wysylanie id sesji do klienta
#x


    while 1:

        operationCode = listenIncomingRequest()  # nasluchiwanie na przyjscie zapytania

        decodeOperationCode(operationCode)

        if len(operationCode) != 24:

            sendAnswerForRequest()