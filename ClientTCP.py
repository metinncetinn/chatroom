#Client tarafında thread kullanmak için fonksiyona çevirdim.
from socket import *
import threading
#TCP soket oluşturma.
serverName = "localhost"#127.0.0.1
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def send_messages(clientSocket):
    while True:
        sentence = input()
        clientSocket.send(sentence.encode())
        print("Mesajınız gönderildi.\nYeni mesaj girin:")

def receive_messages(clientSocket):
    while True:
        try:
            modifiedSentence = clientSocket.recv(1024)
            decodedSentence=modifiedSentence.decode()
            if not modifiedSentence:
                break
            if decodedSentence.split(" ")[0]=="Bu":
                print("\nSunucudan gelen uyarı mesajı:",decodedSentence)
            else:
                print("\nGelen Mesaj:",decodedSentence ,"\nMesaj girin:")
        except OSError:
            break

username = input(clientSocket.recv(1024).decode())
clientSocket.send(username.encode())

#Thread oluşturma ve başlatma.
send_thread = threading.Thread(target=send_messages, args=(clientSocket,))
receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
send_thread.start()
receive_thread.start()
try:
    receive_thread.join()
    send_thread.join()
except KeyboardInterrupt:
    clientSocket.close()