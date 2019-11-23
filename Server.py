import math
import re
import socket
import datetime
import pickle
import time

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

   id = str(idHour + idMinute + idSecond).zfill(6)
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


operationHistory = [] # lista stringow z operacjami



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


def  displayAllMathOperations():
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


   if len(operationCode) >= 38:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
       splitedOperationCode = operationCode.split("$", 5)
       print("Otrzymany kod od klienta: " + operationCode)

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
       Z2 = Z2[3:-1]
       print("Z2: " + Z2)
       Z2 = int(Z2)
   else:
       print("\nTestowy print zebym widzial co przychodzi - Otrzymany kod od klienta historia: " + operationCode)
       splitedOperationCode = operationCode.split("$", 3)
       print(splitedOperationCode)
       ID = splitedOperationCode[0]
       ID = ID[3:]
       print("hID: " + ID)

       ST = splitedOperationCode[1]
       ST = ST[3:]
       print("hST: " + ST)

       OP = splitedOperationCode[2]
       OP = OP[3:]
       print("hOP: " + OP)

       if OP == "HS":
        HS = splitedOperationCode[3]
        HS = HS[3:-1]
        print("hHS: " + HS)
       if OP == "HI":
        HI = splitedOperationCode[3]
        HI = HI[3:-1]
        print("hHI: " + HI)



def executeRequest():
    global DOcounter, ODcounter, MNcounter, DZcounter, POcounter, LOcounter, OD, WY, ST, OP, ZC

    if OP == "DO" or OP == "OD" or OP == "MN" or OP == "DZ" or OP == "PO" or OP == "LO":
        if OP == 'DO':
            WY = add(Z1, Z2)
            IO = "DO" + str(DOcounter)
            DOcounter+=1
            ST = "OK"
        if OP == 'OD':
            WY = subtract(Z1, Z2)
            IO = "OD" + str(ODcounter)
            ODcounter += 1
            ST = "OK"
        if OP == 'MN':
            WY = multiply(Z1, Z2)
            IO = "MN" + str(MNcounter)
            MNcounter += 1
            ST = "OK"
        if OP == 'DZ':
            if Z2 != 0:
                WY = divide(Z1, Z2)
                IO = "DZ" + str(DZcounter)
                DZcounter += 1
                ST = "OK"
            else:
                print("dzielenie przez zero")
                ST = "ER"
                WY = "null"
        if OP == 'PO':
            WY = power(Z1, Z2)
            IO = "PO" + str(POcounter)
            POcounter += 1
            ST = "OK"
        if OP == 'LO':
            WY = log(Z2, Z1)
            IO = "LO" + str(LOcounter)
            LOcounter += 1
            ST = "OK"

        setMathOperation()
        putToHistory()
        ZC = time.time() - startTime
        ZC = str(round(ZC, 2))
        answerCode = "ID=" + str(ID) + "$ST=" + str(ST) + "$IO=" + str(IO) + "$OP=" + str(OP) + "$WY=" + str(WY) + "$ZC=" + str(ZC) + "$"
        print("\nUtworzona odpowiedz: " + answerCode + "\n")
        return answerCode

    if OP == "HS": #odpowiedz klienta na zapytanie o historie sesji

        matcher = str(HS)
        findOperation = list(filter(lambda x: matcher in x, operationHistory))
        if len(findOperation) != 0:
            print("\nZnaleziono historie dla podanego id sesji.\n")
            print(findOperation)
            stringHistory = "@".join(findOperation)
            print("String z historia: " + stringHistory)
            ZC = time.time() - startTime
            ZC = str(round(ZC, 2))
            answerCode = "ID=" + str(ID) + "$ST=OK" + "$OP=" + "HS" + "$HS=" + str(stringHistory) + "$ZC=" + str(ZC) + "$"  # string z historia
        else:
            print("\nNie znaleziono wskazanej sesji.\n")
            info = "Nie znaleziono wpisow dla podanej sesji."
            ZC = time.time() - startTime
            ZC = str(round(ZC, 2))
            answerCode = "ID=" + str(ID) + "$ST=ER" + "$OP=HS" + "$ZC=" + str(ZC) + "$"  #nie znaleziono wpisow dla podanego id
        return answerCode

    if OP == "HI":
        matcher2 = str(HI)
        findOperation2 = list(filter(lambda x: matcher2 in x, operationHistory))
        if len(findOperation2) != 0:
           print("\nZnaleziono historie dla podanego id sesji.\n")
           print(findOperation2)
           findOperation2 = list(filter(lambda x: matcher2 in x, operationHistory))
           if len(findOperation2) != 0:
               ZC = time.time() - startTime
               ZC = str(round(ZC, 2))
               findOperation2 = str(findOperation2)
               findOperation2 = findOperation2[:-2]
               answerCode = "ID=" + str(ID) + "$ST=" + "OK" + "$OP=" + "HI" + "$HI=" + str(findOperation2) + "$ZC=" + str(ZC) + "$"
           else:
               print("\nNie znaleziono wskazanej operacji.\n")
               info = "Nie znaleziono wskazanej operacji."
               ZC = time.time() - startTime
               ZC = str(round(ZC, 2))
               answerCode = "ID=" + str(ID) + "$ST=" + "ER" + "$OP=" + "HI" + "$HI=" + str(info) + "$ZC=" + str(ZC) + "$"
           return answerCode


def listenIncomingRequest():
   receivedOperationCode = clientsocket.recv(1024)
   operationCode = str(receivedOperationCode, 'utf-8')
   return operationCode


def sendIDsessionToClient():
   clientsocket.send(bytes(str(setID()), 'utf8'))


def sendAnswerForRequest():
   clientsocket.send(bytes(str(executeRequest()), 'utf8'))


def putToHistory():
   global operationHistory

   mathOperation = "ID=" + str(ID) + "#IO=" + str(IO) + "#OP=" + str(OP) + "#Z1=" + str(Z1) + "#Z2=" + str(Z2) + "#WY=" + str(WY) + "#"
   operationHistory.append(mathOperation)

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



#*** Uruchomienie serwera ***


while 1:

   clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja
   startTime = time.time()
   print(f'Polaczono z: ', address)
   sendIDsessionToClient()  # wysylanie id sesji do klienta

   while 1:
       operationCode = listenIncomingRequest()  # nasluchiwanie na przyjscie zapytania
       decodeOperationCode(operationCode)
       sendAnswerForRequest()

       if OP=="RE":
           clientsocket.close()

           clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja
           startTime = time.time()
           print(f'Polaczono z: ', address)
           sendIDsessionToClient()  # wysylanie id sesji do klienta

""""
   while 1:
       
       print("1. Nasluchuj klienta 2. Wybierz operacje ")
       choice = input("Wybierz operacje do wykonania: ")
       if choice == "1":
               operationCode = listenIncomingRequest()  # nasluchiwanie na przyjscie zapytania
               decodeOperationCode(operationCode)
               sendAnswerForRequest()
       if choice == "2":

       operation = switchOperations()

       if operation == "FN":
           print("Zakonczono dzialanie programu.")
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
"""""