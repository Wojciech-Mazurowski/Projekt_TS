import re
import socket
from re import split
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie gniazda
def connectingg():
    global iddod, idode, idmno, iddzi, idpot, idlog
    global id
    iddod=0
    idode=0
    idmno=0
    global decodeID
    iddzi=0
    idpot=0
    idlog = 0
    connected = False
    print("Czekam na polaczenie...")
    while not connected:
            try:
                serversocket.connect((socket.gethostname(), 1234)) # nawiazanie polaczenia
                connected = True
                id = serversocket.recv(16)
                idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
                id = str(idstr)
                decodeID = re.findall(r'\d+', id)  # za pomoca regexu wyciaganie liczby ze stringa ID=tutajidsesji$
                print("\nPolaczono z serwerem. Twoj identyfikator sesji to: ", *decodeID, sep="")
                # gwiazdka i ten sep musi byc, bo regex po wyciagnieciu danej wartosci wrzuca ja do listy
                # i wtedy wyswietla z nawiasami kwadratowymi i rownoscia, dzieki temu wyswietla tylko sama wartosc
            except Exception as e:
                pass



z1=0
z2=0
connectingg()
def switchOperation():
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wykonywanie operacji matematycznych.")
    print("4. Polacz sie ponownie.")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  #zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "OB",  # wykonywanie obliczen
        '4': "RE",  # relog bo pewnie potrzebny na rzecz sprawdzania
    }.get(choice, "Podano nieprawidlowy numer operacji.")

def listenIncoming():
    receivedOperationCode = serversocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    decodeOperationCode(operationCode)


def decodeOperationCode(operationCode):
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2
    if len(operationCode) >= 40:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
        print("\nOtrzymany kod od serwea: " + operationCode)

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


def switchMathOperation():
    global z1
    global z2

    global iddod, idode, idmno, iddzi, idpot, idlog
    print("1. Dodawanie\n 2. Odejmowanie\n 3. Mnozenie\n 4. Dzielenie\n 5. Potegowanie\n 6. Logarytmowanie\n")
    choice = input("\nWybierz operacje matematyczna, ktora chcesz wykonac (podaj numer): ")
    if choice == "1":
        print("\nWybrano dodawanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        iddod = iddod +1
    if choice == "2":
        print("\nWybrano odejmowanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        idode = idode + 1
    if choice == "3":
        print("\nWybrano mnozenie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        idmno = idmno + 1
    if choice == "4":
        print("\nWybrano dzielenie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        iddzi = iddzi +1
        while z2 == 0:
            print("Nie wolno dzielic przez 0")
            z2 = int(input("Podaj liczbe rozna od 0"))
    if choice == "5":
        print("\nWybrano potegowanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        idpot = idpot + 1
    if choice == "6":
        print("\nWybrano logarytmowanie:")
        z1 = int(input("Wprowadz podstawe:"))
        idlog = idlog + 1
        while z1 <= 0 or z1 == 1:
            print("\nPodstawa logarytmu nie moze byc mniejsza lub rowna od 0 ani rowna 1:")
            z1 = int(input("wprowadz inna podstawe"))
        z2 = int(input("Wprowadz liczbe do logarytmowania:"))
        while z2 <= 0:
            z2 = int(input("Liczba logarytmowana musi byc dodatnia, podaj inna liczbe"))
    return {
        '1': "DO", #dodawanie
        '2': "OD", #odejmowanie
        '3': "MN", #mnozenie
        '4': "DZ", #dzielenie
        '5': "PO", #potegowanie
        '6': "LO", #logarytmowanie
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def printMathOperationsHistorySession():
    IS = input("podaj ID sesji:")


def printMathOperationsHistoryOperationID():
    IO = input("podaj ID operacji")


def IDO(Operacja):
    global iddod, idode, idmno, iddzi, idpot, idlog
    if Operacja == "DO":
        return iddod
    if Operacja == "OD":
        return idode
    if Operacja == "MN":
        return idmno
    if Operacja == "DZ":
        return iddzi
    if Operacja == "PO":
        return idpot
    if Operacja == "LO":
        return idlog
def CreateAndSendMessage(Operacja):
    global z1
    global z2
    global id
    global decodeID
    wiadomosc = "ID=" + str(*decodeID) + "$ST="+ "tu cos bedzie" + "$IO="+ Operacja + str(IDO(Operacja)) + "$OP=" + Operacja + "$OD=null$" + "Z1=" + str(z1) + "$Z2=" + str(z2) + "$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))

#  przykladowy naglowek: IS#1225$$IO#DO5$$OP#DO$$OD#null$$Z1#5Z2#4

while 1:
    operation = switchOperation()

    if operation == "FN":
        print ("Zakonczono dzialanie programu, rozlaczono z serwerem.")
        serversocket.close()
        break
    elif operation == "HS":
        print("Wyswietlenie historii obliczen przez ID sesji.")
        printMathOperationsHistorySession()
    elif operation == "HO":
        print("Wyswietlenie historii obliczens przez ID obliczen.")
        printMathOperationsHistoryOperationID()
    elif operation == "OB":
        print("Wykonywanie operacji matematycznych.")
        CreateAndSendMessage(switchMathOperation())
        listenIncoming()
    elif operation == "RE":
        serversocket.close()
        connectingg()
    else:
        print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")