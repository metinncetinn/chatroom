#Client tarafında thread kullanmak için fonksiyona çevirdim.
from socket import *
import threading
#UDP soket oluşturma.
serverName = "localhost"#127.0.0.1
serverPort = 12346
clientSocket = socket(AF_INET, SOCK_DGRAM)

#Udp'de sürekli bir bağlantı olmadığından TCP'den farklı olarak mesaj gönderirken her seferinde server ismi ve portu lazım.
def send_messages(clientSocket, serverName, serverPort):
    while True:
        message = input()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        if message.lower() == "görüşürüz":
            print("Başarılı şekilde çıkış yaptınız...")
            break
        else:
            print("Mesajınız gönderildi.\nYeni mesaj girin:")

def receive_messages(clientSocket):
    while True:
        try:
            modifiedMessage, _ = clientSocket.recvfrom(1024)
            decodedMessage=modifiedMessage.decode()
            if not modifiedMessage:
                break
            if decodedMessage.split(" ")[0]=="Bu":
                print("\nSunucudan gelen uyarı mesajı:", decodedMessage)
            else:
                print("\nGelen mesaj:", decodedMessage, "\nMesaj girin:")
        except OSError:
            break

clientSocket.sendto("username".encode(), (serverName, serverPort))

username_request, garbage = clientSocket.recvfrom(1024)
username = input(username_request.decode())
clientSocket.sendto(username.encode(), (serverName, serverPort))

#Thread oluşturma ve başlatma.
send_thread = threading.Thread(target=send_messages, args=(clientSocket, serverName, serverPort))
receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
send_thread.start()
receive_thread.start()
try:
    receive_thread.join()
    send_thread.join()
except KeyboardInterrupt:
    clientSocket.close()
