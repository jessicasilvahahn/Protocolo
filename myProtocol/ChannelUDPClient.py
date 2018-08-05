import socket

HOST = ''  # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
msg = "/home/jessica/Documentos/teste/teste.txt"
fileNameClient = "/home/jessica/Documentos/teste2.txt"
udp.sendto(msg.encode(), dest)
serverMsg,addrServer = udp.recvfrom(512)
fileClient = open(fileNameClient, 'w')
while(serverMsg.decode()!="finish"):
    print("Recebido de:",serverMsg,addrServer)
    print("Sending to File\n")
    fileClient.write(serverMsg.decode('utf-8'))
    serverMsg, addrServer = udp.recvfrom(512)
fileClient.close()
print("Arquivo Transferido\n")
udp.close()


