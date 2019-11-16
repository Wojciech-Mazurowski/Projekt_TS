import re
import socket
from re import split

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie gniazda
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

def switchOperation():
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wykonywanie operacji matematycznych.")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  #zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "OB",  # wykonywanie obliczen
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def switchMathOperation():
    print("1. Dodawanie\n 2. Odejmowanie\n 3. Mnozenie\n 4. Dzielenie\n 5. Potegowanie\n 6. Logarytmowanie\n")
    choice = input("\nWybierz operacje matematyczna, ktora chcesz wykonac (podaj numer): ")
    if choice == "1":
        print("\nWybrano dodawanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
    if choice == "2":
        print("\nWybrano odejmowanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
    if choice == "3":
        print("\nWybrano mnozenie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
    if choice == "4":
        print("\nWybrano dzielenie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
        while z2 == 0:
            print("Nie wolno dzielic przez 0")
            z2 = int(input("Podaj liczbe rozna od 0"))
    if choice == "5":
        print("\nWybrano potegowanie:")
        z1 = int(input("Wprowadz pierwsza liczbe:"))
        z2 = int(input("Wprowadz druga liczbe:"))
    if choice == "6":
        print("\nWybrano logarytmowanie:")
        z1 = int(input("Wprowadz podstawe:"))
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
    IDS = input("podaj ID sesji:")


def printMathOperationsHistoryOperationID():
    IDO = input("podaj ID operacji")



while 1:
    operationCode = "OP=dodawaj$" #testowo wysylam
    serversocket.send(bytes(operationCode, 'utf-8')) #j.w.

    operationCode2 = "Z1=15$"  # testowo wysylam
    serversocket.send(bytes(operationCode2, 'utf-8'))  # j.w.

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
        switchMathOperation()
    else:
        print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")