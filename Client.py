import re
import socket
from re import split

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie gniazda
s.connect((socket.gethostname(), 1234)) # nawiazanie polaczenia

id = s.recv(16)
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

    return {
        '1': "DO", #dodawanie
        '2': "OD", #odejmowanie
        '3': "MN", #mnozenie
        '4': "DZ", #dzielenie
        '5': "PO", #potegowanie
        '6': "LO", #logarytmowanie
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def printMathOperationsHistorySession():
    print('\ndrukowanie historii przez id sesji')


def printMathOperationsHistoryOperationID():
    print('\ndrukowanie historii przez id operacji')


# Wybor operacji do wykonania

while 1:
    operation = switchOperation()

    if operation == "FN":
        print ("Zakonczono dzialanie programu, rozlaczono z serwerem.")
        break
    elif operation == "HS":
        print("Wyswietlenie historii obliczen przez ID sesji.")
        printMathOperationsHistorySession()
    elif operation == "HO":
        print("Wyswietlenie historii obliczen przez ID obliczen.")
        printMathOperationsHistoryOperationID()
    elif operation == "OB":
        print("Wykonywanie operacji matematycznych.")
        switchMathOperation()
    else:
        print("Podano nieprawidlowy numer operacji, sprobuj jeszcze raz...")
