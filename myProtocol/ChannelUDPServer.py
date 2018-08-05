import socket
HOST = ''              # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)
while True:
    msg, cliente = udp.recvfrom(512)
    print(cliente, msg)
    print("Mensagem server\n")
    msgServer = input()
    udp.sendto(msgServer.encode(),(cliente[0],cliente[1]))