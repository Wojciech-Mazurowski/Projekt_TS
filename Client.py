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
    iddzi=0
    idpot=0
    idlog = 0
    connected = False
    while not connected:
            try:
                serversocket.connect((socket.gethostname(), 1234)) # nawiazanie polaczenia
                connected = True
            except Exception as e:
                pass    # jezeli nie bylo polaczenia to wywalalo blad, to pozwoli na "czekanie" klienta az nastapi polaczenie

    id = serversocket.recv(16)
    idstr = str(id, 'utf8') #konwertowanie id sesji do formatu utf-8
    id = str(idstr)
    decodeID = re.findall(r'\d+', id) # za pomoca regexu wyciaganie liczby ze stringa ID=tutajidsesji$


    print("\nPolaczono z serwerem. Twoj identyfikator sesji to: ", *decodeID, sep="")
    #gwiazdka i ten sep musi byc, bo regex po wyciagnieciu danej wartosci wrzuca ja do listy
    # i wtedy wyswietla z nawiasami kwadratowymi i rownoscia, dzieki temu wyswietla tylko sama wartosc
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


#def readNumbers():
#    a = input("\nPodaj wartosc pierwszej liczby: ") nie zauwzylem tego, zrobilem wyzej xd
#    b = input("Podaj wartosc drugiej liczby: ")


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
    wiadomosc = "IS#" + str(id) + "$IO#"+ Operacja + str(IDO(Operacja)) + "$$OP#" + Operacja + "$$OD#null$$" + "Z1#" + str(z1) + "$$Z2#" + str(z2) + "$$"
    print(wiadomosc)
   # serversocket.send(bytes(wiadomosc, 'utf-8'))

#  przykladowy naglowek: IS#1225$$IO#DO5$$OP#DO$$OD#null$$Z1#5Z2#4

while 1:
    '''operationCode = "OP=dodawaj$" #testowo wysylam
    serversocket.send(bytes(operationCode, 'utf-8')) #j.w.

    operationCode2 = "Z1=15$"  # testowo wysylam
    serversocket.send(bytes(operationCode2, 'utf-8'))  # j.w.'''

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
    elif operation == "RE":
        print("To jescze nie dziala byq")
        #connectingg()
    else:
        print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")