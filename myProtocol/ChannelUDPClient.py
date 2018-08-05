import socket

HOST = ''  # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
print ('Para sair use CTRL+X\n')
msg = input()
while  msg != '\x18':
    udp.sendto(msg.encode(), dest)
    msg = input()
    serverMsg,addrServer = udp.recvfrom(512)
    print("Recebido de:",serverMsg,addrServer)