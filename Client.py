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

def decodeOperationCodeHS(operationCode):
   global IS
   global IO
   global OP
   global OD
   global Z1
   global Z2
   if len(operationCode) >= 20:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
      # print("\nOtrzymany kod od serwea: " + operationCode)

       splitedOperationCode = operationCode.split("$", 5)
       ID = splitedOperationCode[0]
       ID = ID[3:]
       print("\nID sesji: " + ID)

       ST = splitedOperationCode[1]
       ST = ST[3:]
       print("Status: " + ST)

       OP = splitedOperationCode[2]
       OP = OP[3:]
       print("Operacja: " + OP)

       WY= splitedOperationCode[3]
       WY = WY[3:]

       splitedanwser = WY.split("@", 1024)
       print("\nHISTORIA: ")
       for x in splitedanwser:
           decodeOperationCodeHSS(x)



   else:
       print("wystapil blad - prawdopodobnie podano zly identyfikator")



def listenIncomingHS():
   receivedOperationCode = serversocket.recv(1024)
   operationCode = str(receivedOperationCode, 'utf-8')
   decodeOperationCodeHS(operationCode)


def decodeOperationCodeHSS(operationCode):
   global IS
   global IO
   global OP
   global OD
   global Z1
   global Z2
   if len(operationCode) >= 20:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
       splitedOperationCode = operationCode.split("#", 5)
       ID = splitedOperationCode[0]
       ID = ID[3:]
      # print("id sesji: " + ID)

       ST = splitedOperationCode[1]
       ST = ST[3:]
       print("\nID operacji: " + ST)

       IO = splitedOperationCode[2]
       IO = IO[3:]
       print("Operacja: " + IO)

       OP = splitedOperationCode[3]
       OP = OP[3:]
       print("Pierwsza zmienna: " + OP)

       WY= splitedOperationCode[4]
       WY = WY[3:]
       print("Druga zmienna: " + WY)

       WYN = splitedOperationCode[5]
       WYN = WYN[3:-1]
       print("Wynik: " + WYN )


      # ZC = splitedOperationCode[6]
        #ZC = ZC[3:-1]
       #print("Czas od polaczenia:" + ZC + "s")


   else:
       print("Wystapil blad - prawdopodobnie podano zly identyfikator")


def decodeOperationCode(operationCode):
   global IS
   global IO
   global OP
   global OD
   global Z1
   global Z2

   if len(operationCode) >= 20:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie


       splitedOperationCode = operationCode.split("$", 5)
       ID = splitedOperationCode[0]
       ID = ID[3:]
       print("\nid sesji: " + ID)

       ST = splitedOperationCode[1]
       ST = ST[3:]
       print("status: " + ST)

       IO = splitedOperationCode[2]
       IO = IO[3:]
       print("ID operacji: " + IO)

       OP = splitedOperationCode[3]
       OP = OP[3:]
       print("operacja mat: " + OP)

       WY= splitedOperationCode[4]
       WY = WY[3:]
       print("Odpowiedz: " + WY)

       ZC = splitedOperationCode[5]
       ZC = ZC[3:-1]
       print("Czas od polaczenia:" + ZC + "s")


   else:
       print("Wystapil nieoczekiwany blad :(")


def switchMathOperation():
   global z1
   global z2

   global iddod, idode, idmno, iddzi, idpot, idlog
   print("1. Dodawanie\n 2. Odejmowanie\n 3. Mnozenie\n 4. Dzielenie\n 5. Potegowanie\n 6. Logarytmowanie\n")
   choice = input("\nWybierz operacje matematyczna, ktora chcesz wykonac (podaj numer): ")
   if choice == "1":
       print("\nWybrano dodawanie:")
       z1 = input("Wprowadz pierwsza liczbe:")
       z2 = input("Wprowadz druga liczbe:")
       iddod = iddod +1
   if choice == "2":
       print("\nWybrano odejmowanie:")
       z1 = input("Wprowadz pierwsza liczbe:")
       z2 = input("Wprowadz druga liczbe:")
       idode = idode + 1
   if choice == "3":
       print("\nWybrano mnozenie:")
       z1 = input("Wprowadz pierwsza liczbe:")
       z2 = input("Wprowadz druga liczbe:")
       idmno = idmno + 1
   if choice == "4":
       print("\nWybrano dzielenie:")
       z1 = input("Wprowadz pierwsza liczbe:")
       z2 = input("Wprowadz druga liczbe:")
       iddzi = iddzi +1
       while z2 == "0":
           print("Nie wolno dzielic przez 0")
           z2 = input("Podaj liczbe rozna od 0")
   if choice == "5":
       print("\nWybrano potegowanie:")
       z1 = input("Wprowadz pierwsza liczbe:")
       z2 = input("Wprowadz druga liczbe:")
       idpot = idpot + 1
   if choice == "6":
       print("\nWybrano logarytmowanie:")
       z1 = input("Wprowadz podstawe:")
       idlog = idlog + 1
       while z1.isalpha():
           print("Zmienne musza byc liczba!")
           z1 = input("Podaj pierwsza LICZBE: ")
       while int(z1) <= 0 or int(z1) == 1:
           print("\nPodstawa logarytmu nie moze byc mniejsza lub rowna od 0 ani rowna 1:")
           z1 = input("wprowadz inna podstawe")
       z2 = input("Wprowadz liczbe do logarytmowania:")
       while z2.isalpha():
           print("Zmienne musza byc liczba!")
           z2 = input("Podaj druga LICZBE: ")
       while int(z2) <= 0:
           z2 = input("Liczba logarytmowana musi byc dodatnia, podaj inna liczbe")

   while z1.isalpha() or z2.isalpha():
        print("Zmienne musza byc liczba!")
        z1 = input("Podaj pierwsza LICZBE: ")
        z2 = input("Podaj druga LICZBE: ")
   z1=int(z1)
   z2=int(z2)
   return {
       '1': "DO", #dodawanie
       '2': "OD", #odejmowanie
       '3': "MN", #mnozenie
       '4': "DZ", #dzielenie
       '5': "PO", #potegowanie
       '6': "LO", #logarytmowanie
   }.get(choice, "Podano nieprawidlowy numer operacji.")

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
   wiadomosc = "ID=" + str(*decodeID) + "$ST=" + "null" + "$IO="+ Operacja + str(IDO(Operacja)) + "$OP=" + Operacja + "$Z1=" + str(z1) + "$Z2=" + str(z2) + "$"
   serversocket.send(bytes(wiadomosc, 'utf-8'))

#  przykladowy naglowek: IS#1225$$IO#DO5$$OP#DO$$OD#null$$Z1#5Z2#4


def AskForRelog():
    global decodeID
    wiadomosc ="ID=" + str(*decodeID) + "$ST=" + "null" + "$OP=" + "RE$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def ReceiveID():
    global decodeID
    id = serversocket.recv(16)
    idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
    id = str(idstr)
    decodeID = re.findall(r'\d+', id)  # za pomoca regexu wyciaganie liczby ze stringa ID=tutajidsesji$
    print("\nPolaczono z serwerem. Twoj identyfikator sesji to: ", *decodeID, sep="")


def AskForHistoryByID():
   global decodeID
   IDS = input("Podaj ID sesji do wyswietlenia historii:")
   while len(IDS) != 6:
       IDS = input("ID sesji jest niewlasciwy, sprobuj ponownie: \n") #tutaj ma do skutku prosic o conajmniej 6 cyfrowy id sesji
   wiadomosc = "ID=" + str(*decodeID) + "$ST=" + "null" + "$OP=" + "HS" +  "$HS=" + IDS + "$" #w kazdej wiadomosci ma byc wysylane id biezacej sesji dltego id = id sesji
   serversocket.send(bytes(wiadomosc, 'utf-8'))

def AskForHistoryByIO():
   IDOP = input("Podaj indentyfikator operacji:")
   while len(IDOP) < 3:
       IDOP = input("ID operacji matematycznej jest niewlasciwy, sprobuj ponownie: \n") #tutaj ma do skutku prosic o conajmniej 3 znakowy id
   wiadomosc = "ID=" + str(*decodeID) + "$ST=" + "null" + "$OP=" + "HI" + "$IO=" + IDOP + "$"
   serversocket.send(bytes(wiadomosc, 'utf-8'))


while 1:
   operation = switchOperation()
    #dziala
   if operation == "FN":
       print ("Zakonczono dzialanie programu, rozlaczono z serwerem.")
       serversocket.close()
       break
   elif operation == "HS":
       print("Wyswietlenie historii obliczen przez ID sesji.")
       AskForHistoryByID()
       listenIncomingHS()
   elif operation == "HO":
       print("Wyswietlenie historii obliczens przez ID obliczen.")
       AskForHistoryByIO()
       listenIncomingHS()
   elif operation == "OB":
       print("Wykonywanie operacji matematycznych.")
       CreateAndSendMessage(switchMathOperation())
       listenIncoming()
   elif operation == "RE":
        AskForRelog()
        ReceiveID()
   else:
       print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")