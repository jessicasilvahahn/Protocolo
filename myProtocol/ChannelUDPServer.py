from myProtocol import channelComunication

HOST = ''              # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
channel = channelComunication.iniciaConexao()
orig = (HOST, PORT)
channelComunication.bindServer(channel,orig)
while True:
    fileName, cliente = channelComunication.recebeMsg(channel)
    fileServer = open(fileName, 'r')
    print(cliente, fileName)
    data = fileServer.read(512)
    while(data):
        print(data,"\n")
        dest = (cliente[0],cliente[1])
        if(channelComunication.enviaMsg(dest,channel,data)):
            print("Sending\n")
            data = fileServer.read(512)
    print("Enviando finish")
    channelComunication.enviaMsg(dest,channel,"finish")
    fileServer.close()