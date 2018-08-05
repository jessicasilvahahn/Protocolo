import socket
import sys
HOST = ''              # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)
while True:
    fileName, cliente = udp.recvfrom(512)
    print(cliente, fileName)
    fileServer = open(fileName,'r')
    data = fileServer.read(512)
    while(data):
        print(data,"\n")
        if(udp.sendto(data.encode(),(cliente[0],cliente[1]))):
                print("Sending\n")
                data = fileServer.read(512)
    print("Enviando finish")
    udp.sendto("finish".encode(), (cliente[0], cliente[1]))
    fileServer.close()