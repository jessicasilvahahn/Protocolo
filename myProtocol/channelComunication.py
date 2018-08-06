import socket

def iniciaConexao():
    channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Inicia Conexão")
    return channel

def enviaMsg(dest,channel,msg):
    print ("Enviando Mensagem\n")
    #sendto return the number of bytes sent
    return channel.sendto(msg.encode(),dest)

def recebeMsg(channel):
    print ("Recebendo Mensagem\n")
    msg,addr = channel.recvfrom(512)
    return msg,addr

def finalizaConexao(channel):
    print ("Finalizando Conexão\n")
    channel.close()

def bindServer(channel,orig):
    print("Binding")
    channel.bind(orig)