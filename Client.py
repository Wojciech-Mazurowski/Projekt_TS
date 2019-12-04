import re
import socket
import time
from time import sleep
from _datetime import datetime
from re import split

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda


def connectingg():                                  #resetowanie odpowiednich wartosci oraz oczekiwanie na polaczenie
    global iddod, idode, idmno, iddzi, idpot, idlog
    global id
    IPw = input("Podaj IP serwera: ")
    iddod = 0
    idode = 0
    idmno = 0
    global decodeID
    iddzi = 0
    idpot = 0
    idlog = 0
    connected = False
    print("Czekam na polaczenie...")
    while not connected:
        try:
            serversocket.connect((IPw, 1234))  # nawiazanie polaczenia
            connected = True
            id = serversocket.recv(1024)
            idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
            id = str(idstr)
            id = id.split("$", 10)
            decodeID = id[0]
            decodeID = decodeID[3:]
            czas = id[3]
            czas = czas[3:]
            print("\nPolaczono z serwerem. Twoj identyfikator sesji to: ", decodeID, sep="")
            print("Znacznik czasu: ", czas)
        except Exception as e:
            pass


z1 = 0
z2 = 0
connectingg()


def switchOperation():                                  #menu główne, zwraca odpowiedni wybór
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wykonywanie operacji matematycznych.")
    print("4. Zmien uzytkownika (zmiana id sesji).")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  # zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "OB",  # wykonywanie obliczen
        '4': "RE",  # relog bo pewnie potrzebny na rzecz sprawdzania
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def listenIncoming():           #nasłuchiwanie odpowiedzi od serwera
    receivedOperationCode = serversocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    decodeOperationCode(operationCode)

def ReadError(ER):              #dekodowanie errorow
    if ER == "ER1":
        print("Error: Dzielenie przez zero")
    if ER == "ER2":
        print("Error: Liczba wychodzi po za zakres zmiennej")
    if ER == "ER3":
        print("Error: Niewlasciwe wartosci przy logarytmowaniu")
    if ER == "ER4":
        print("Error: Brak historii dla podanej id sesji")
    if ER == "ER5":
        print("Error: Brak wskazanej operacji po IO")

def decodeOperationCodeHSIO(operationCode):         #dekodowanie historii sesji przez ID sesji oraz ID operacji
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2
    splitedOperationCode = operationCode.split("$", 5)  #podzielenie wiadomosci przez znak dolara

    ID = splitedOperationCode[0]        #kolejno przypisywanie odpowiednich wartosci oraz wypisywanie ich
    ID = ID[3:]
    print("\nID sesji: " + ID)

    ST = splitedOperationCode[1]
    ST = ST[3:]
    print("Status: " + ST)

    OP = splitedOperationCode[2]
    OP = OP[3:]
    NR = 1
    OP1= "D"
    print("Operacja: " + OP)
    if ST[:2] != "ER":                  #sprawdzanie czy otrzyamana wiadomosc jest pelna czy wstapil error
        ZC = splitedOperationCode[3]
        if OP == "HS":
            NRS = splitedOperationCode[4]
            NRS = NRS[3:]
            NR = int(NRS)
            OP1 = "HS"
    else:
        ZC = splitedOperationCode[3]
        ReadError(ST)
    ZC = ZC[3:]
    print("ZC: " + ZC)
    i = 0
    if ST[:2] != "ER":              #jesli nie bylo errora odbieranie histori sesji oraz wypisywanie jej
        print("\nWyszukane dzialania: ")
        for x in range(int(NR)):
            i=0
            receivedOperationCode = serversocket.recv(1024)

            operationCode = str(receivedOperationCode, 'utf-8')
            splitedOperationCode = operationCode.split("$", 30)
            if OP1=="HS":
                ID = splitedOperationCode[i]
                ID = ID[3:]
                print("\nID sesji: " + ID)
                i=i+1

                ST = splitedOperationCode[i]
                ST = ST[3:]
                print("Status: " + ST)
                i = i + 1
                IO = splitedOperationCode[i]
                IO = IO[3:]
                print("ID operacji: " + IO)
                i = i + 1
                ZC = splitedOperationCode[i]
                ZC = ZC[3:]
                print("ZC: " + ZC)
                i = i + 1


            ID = splitedOperationCode[i]
            ID = ID[3:]
            print("\nID sesji: " + ID)
            i = i + 1
            ST = splitedOperationCode[i]
            ST = ST[3:]
            print("Status: " + ST)
            i = i + 1

            IO = splitedOperationCode[i]
            IO = IO[3:]
            print("ID operacji: " + IO)
            i = i + 1

            OP  = splitedOperationCode[i]
            OP = OP[3:]
            print("Operacja: " + OP)
            i = i + 1

            ZC1 = splitedOperationCode[i]
            ZC1 = ZC1[3:]
            print("Zmienna 1: " + ZC1)
            i = i + 1

            ZC2 = splitedOperationCode[i]
            ZC2 = ZC2[3:]
            print("Zmienna 2: " + ZC2)
            i = i + 1

            WY = splitedOperationCode[i]
            WY = WY[3:]
            print("Wynik: " + WY)
            i = i + 1
            ZC = splitedOperationCode[i]
            ZC = ZC[3:-1]
            print("ZC: " + ZC)
            i = i + 1
    else:
        print("Wystapil blad - nie znaleziono operacji o podanym ID w historii")


def listenIncomingHSIO():                           #nasluchiwanie na kolejne komunikaty z historii
    receivedOperationCode = serversocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    decodeOperationCodeHSIO(operationCode)


def decodeOperationCode(operationCode):             #odbieranie wiadomosci oraz dekodowanie jej
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2

    splitedOperationCode = operationCode.split("$", 5)          #dzielenie otrzymanego komunikatu
    ID = splitedOperationCode[0]
    ID = ID[3:]
    print("\nid sesji: " + ID)

    ST = splitedOperationCode[1]
    ST = ST[3:]
    print("status: " + ST)


    if ST[:2] != "ER":                  #sprawdzanie czy error a jesli nie to dekodowanie
        IO = splitedOperationCode[2]
        IO = IO[3:]
        print("ID operacji: " + IO)

        OP = splitedOperationCode[3]
        OP = OP[3:]
        print("operacja mat: " + OP)

        WY = splitedOperationCode[4]
        WY = WY[3:]
        ZC = splitedOperationCode[5]
        ZC = ZC[3:-1]
        print("Odpowiedz: " + WY)
    if ST[:2] == "ER":                      #jesli error to odczytaj go i zdekoduj pozostale pola
        ReadError(ST)
        OP = splitedOperationCode[2]
        OP = OP[3:]
        print("Operacja: " + OP)
        ZC = splitedOperationCode[3]
        ZC = ZC[3:]



    print("Data, godzina wykonania operacji: " + ZC + "s")


def InputLiczby():          #wprowadzanie liczb oraz sprawdzanie ich poprawnosci
    global z1
    global z2
    z1 = input("Wprowadz pierwsza liczbe:")
    z2 = input("Wprowadz druga liczbe:")
    while True:
        try:
            z1 = float(z1)
            z2 = float(z2)
            break
        except Exception as e:
            print("Zmienne musza byc liczba!")
            z1 = input("Wprowadz pierwsza liczbe:")
            z2 = input("Wprowadz druga liczbe:")
            pass


def switchMathOperation():
    global z1
    global z2

    global iddod, idode, idmno, iddzi, idpot, idlog
    print("1. Dodawanie\n 2. Odejmowanie\n 3. Mnozenie\n 4. Dzielenie\n 5. Potegowanie\n 6. Logarytmowanie\n")  #wybieranie operacji oraz zwiekszanie jej ilosci wykonania (potrzebne do ID operacji)
    choice = input("\nWybierz operacje matematyczna, ktora chcesz wykonac (podaj numer): ")
    if choice == "1":
        print("\nWybrano dodawanie:")
        InputLiczby()
        iddod = iddod + 1
    if choice == "2":
        print("\nWybrano odejmowanie:")
        InputLiczby()
        idode = idode + 1
    if choice == "3":
        print("\nWybrano mnozenie:")
        InputLiczby()
        idmno = idmno + 1
    if choice == "4":
        print("\nWybrano dzielenie:")
        InputLiczby()
        iddzi = iddzi + 1
    if choice == "5":
        print("\nWybrano potegowanie:")
        InputLiczby()
        idpot = idpot + 1
    if choice == "6":
        print("\nWybrano logarytmowanie:")
        InputLiczby()
        idlog = idlog + 1

    return {
        '1': "dodawaj",  # dodawanie
        '2': "odejmuj",  # odejmowanie
        '3': "mnoz",  # mnozenie
        '4': "dziel",  # dzielenie
        '5': "poteguj",  # potegowanie
        '6': "logarytmuj",  # logarytmowanie
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def IDO(Operacja):
    global iddod, idode, idmno, iddzi, idpot, idlog
    if Operacja == "dodawaj":
        return iddod
    if Operacja == "odejmuj":
        return idode
    if Operacja == "mnoz":
        return idmno
    if Operacja == "dziel":
        return iddzi
    if Operacja == "poteguj":
        return idpot
    if Operacja == "logarytmuj":
        return idlog


def CreateAndSendMessage(Operacja):             #tworzenie wiadomosci z zapytaniem o obliczenia
    if not Operacja == "Podano nieprawidlowy numer operacji.":
        global z1
        global z2
        global id
        global decodeID
        nowTime = datetime.now()
        year = nowTime.strftime("%Y")
        month = nowTime.strftime("%m")
        day = nowTime.strftime("%d")
        time = nowTime.strftime("%H:%M:%S")
        ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
        wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$IO=" + Operacja + str(
            IDO(Operacja)) + "$OP=" + Operacja + "$Z1=" + str(z1) + "$Z2=" + str(z2) + "$ZC=" + str(ZC) + "$"
        serversocket.send(bytes(wiadomosc, 'utf-8'))
    else:
        return "0"


def AskForRelog():      #tworzenie wiadomosci z zapytaniem o nowe ID sesji
    global decodeID
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$OP=" + "RE$ZC=" + str(ZC) + "$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def ReceiveID():            #odbieranie ID sesji
    global decodeID
    id = serversocket.recv(1024)
    idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
    id = str(idstr)
    id = id.split("$", 10)
    decodeID = id[0]
    decodeID = decodeID[3:]
    czas = id[3]
    czas = czas[3:]
    print("\nPolaczono z serwerem. Twoj nowy identyfikator sesji to: ", decodeID, sep="")
    print("Znacznik czasu: ", czas)


def AskForHistoryByID():            #tworzenie oraz wysylanie zapytania o historie przez ID sesji
    global decodeID
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    IDS = input("Podaj ID sesji do wyswietlenia historii:")
    while len(IDS) != 6:
        IDS = input(
            "ID sesji jest niewlasciwy, sprobuj ponownie: \n")  # tutaj ma do skutku prosic o conajmniej 6 cyfrowy id sesji
    wiadomosc = "ID=" + str(
        decodeID) + "$ST=" + "null" + "$OP=" + "HS" + "$HS=" + IDS + "$ZC=" + ZC + "$"  # w kazdej wiadomosci ma byc wysylane id biezacej sesji dltego id = id sesji
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def EndSession():       #zakanczanie programu
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")

    wiadomosc = "ID=" + str(
        decodeID) + "$ST=" + "null" + "$OP=" + "FN" + "$ZC=" + ZC + "$"  # w kazdej wiadomosci ma byc wysylane id biezacej sesji dltego id = id sesji
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def AskForHistoryByIO():        #tworzenie oraz wysylanie wiadomosci o historie sesji przez id operacji
    IDOP = input("Podaj indentyfikator operacji:")
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    while len(IDOP) < 3:
        IDOP = input(
            "ID operacji matematycznej jest niewlasciwy, sprobuj ponownie: \n")  # tutaj ma do skutku prosic o conajmniej 3 znakowy id
    wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$OP=" + "HI" + "$IO=" + IDOP + "$ZC=" + str(ZC) + "$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))


while 1: #glowna petla while
    operation = switchOperation()
    # dziala
    if operation == "FN":
        print("Zakonczono dzialanie programu, rozlaczono z serwerem.")
        EndSession()
        serversocket.close()
        break
    elif operation == "HS":
        print("Wyswietlenie historii obliczen przez ID sesji.")
        AskForHistoryByID()
        listenIncomingHSIO()
    elif operation == "HO":
        print("Wyswietlenie historii obliczens przez ID obliczen.")
        AskForHistoryByIO()
        listenIncomingHSIO()
    elif operation == "OB":
        print("Wykonywanie operacji matematycznych.")
        sprawdzanko = CreateAndSendMessage(switchMathOperation())
        if sprawdzanko != "0":
            listenIncoming()
    elif operation == "RE":
        AskForRelog()
        ReceiveID()
    else:
        print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")