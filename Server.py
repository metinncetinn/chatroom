from socket import *
import threading
#TCP ve UDP portları
TCPPort=12345
UDPPort=12346
#Kullanıcı isimlerini tutmak için sözlük yapısı kullanıldı.Bunun yerine set(küme) kullanacaktım tekrarı engellemek için.
#Fakat clientSocket-usurname(TCP için)/clientAddress-usurname(UDP için) eşleşmesi için kullandım.
usernames = {}
tcpClients = []
udpClients = []
#Birden fazla thread kullanımı için lock.
lock = threading.Lock()
#TCP Client ve UDP Client 
def tcpClient(clientSocket,addr):
    try:
        #İlk mesaj kullanıcı adı olacak.
        clientSocket.send("Kullanıcı adı giriniz:".encode())
        username = clientSocket.recv(1024).decode()
        with lock:
            #Kullanıcı adı kontrolü.
            while username in usernames.values():
                clientSocket.send("Bu kullanıcı adı mevcut, lütfen başka bir kullanıcı adı girin:".encode())
                username = clientSocket.recv(1024).decode()
            usernames[clientSocket] = username
            tcpClients.append(clientSocket)
        broadcast(f"{username} [TCP] ile bağlanmıştır.", sender=clientSocket)
        #Bağlantı ilk oluşurken özel olarak usernameyi döndürdüm.
        #Çünkü oluşturduğum Broadcast ile kendisi alamaz.
        clientSocket.send(f"Hoşgeldiniz {username} TCP ile bağlısınız".encode())
        while True:
            message = clientSocket.recv(1024).decode()
            broadcast(f"{username}[TCP]: {message}", sender=clientSocket)    
    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        with lock:
            tcpClients.remove(clientSocket)
            username = usernames.pop(clientSocket, None)
        if username:
            #Herkese mesaj gönderme.
            broadcast(f"{username}[TCP] sohbet odasından ayrılmıştır.", sender=None)
        clientSocket.close()

def udp_messages(udpSocket):
    while True:
        message, clientAddress = udpSocket.recvfrom(1024)
        decoded_message = message.decode()
        if clientAddress not in udpClients:
            udpSocket.sendto("Kullanıcı adı girin:".encode(), clientAddress)
            username_message, clientAddress = udpSocket.recvfrom(1024)
            username = username_message.decode()
            with lock:
                while username in usernames.values():
                    udpSocket.sendto("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin:".encode(), clientAddress)
                    username_message, clientAddress = udpSocket.recvfrom(1024)
                    username = username_message.decode()
                usernames[clientAddress] = username
                udpClients.append(clientAddress)
            broadcast(f"{username} [UDP] isteği ile bağlandı.", sender=clientAddress)
            udpSocket.sendto(f"Hoşgeldiniz {username} UDP üzerinden mesajlaşıyorsunuz".encode(), clientAddress)
        else:
            username = usernames[clientAddress]
            #TCP den ayrı olarak UDP bağlantısının kapanacağını anlamak için özel mesaj.
            #Görüşümüz demeden UDPClient kapanırsa kullanıcı adı silinmiyor yani aynı isim verilmiyor.
            if decoded_message.lower() == "görüşürüz":
                with lock:
                    udpClients.remove(clientAddress)
                    usernames.pop(clientAddress, None)
                broadcast(f"{username}[UDP] sohbet odasından ayrılmıştır.", sender=None)
            else:
                broadcast(f"{username}[UDP]: {decoded_message}", sender=clientAddress)

#Mesajı ve atan kişiyi alır (gönderen hariç 77. ve 84. Satırlar) diğer tüm bağlantılara mesajı iletir.
def broadcast(message, sender=None):
    with lock:
        for client in tcpClients:
            if client != sender:
                try:
                    client.send(message.encode())
                except Exception:
                    client.close()
                    tcpClients.remove(client)
        for clientAddress in udpClients:
            if clientAddress != sender:
                udpSocket.sendto(message.encode(), clientAddress)
    print(message)

#TCP soketlerin oluşturulması
tcpSocket = socket(AF_INET, SOCK_STREAM)
#Ip ve portların bağlanması
tcpSocket.bind(('', TCPPort))
#Bağlantıalrı dinleme
tcpSocket.listen(5)
#UDP soketlerin oluşturulması
udpSocket = socket(AF_INET, SOCK_DGRAM)
#Ip ve portların bağlanması
udpSocket.bind(('', UDPPort))

print("Sunucu TCP ve UDP isteklerini dinliyor...")

#TCP ve UDP Thread oluştururken en büyük fark TCP de adres bilgisi de olmasıdır.
#Çünkü sürekli açık bir kanal vardır(Kapatılmak istenmedikçe.)
ThreadUDP = threading.Thread(target=udp_messages, args=(udpSocket,))
ThreadUDP.start()
while True:
    clientSocket, addr = tcpSocket.accept()
    ThreadTCP = threading.Thread(target=tcpClient, args=(clientSocket, addr))
    ThreadTCP.start()