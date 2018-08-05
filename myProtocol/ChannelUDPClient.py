from myProtocol import channelComunication

msg = "/home/jessica/Documentos/teste/teste.txt"
fileNameClient = "/home/jessica/Documentos/teste2.txt"
HOST = ''
PORT = 3400
dest = (HOST,PORT)
channel = channelComunication.iniciaConexao()
channelComunication.enviaMsg(dest,channel,msg)
serverMsg, addrServer = channelComunication.recebeMsg(channel)
fileClient = open(fileNameClient, 'w')
while (serverMsg.decode() != "finish"):
    print("Recebido de:", serverMsg, addrServer)
    print("Sending to File\n")
    fileClient.write(serverMsg.decode('utf-8'))
    serverMsg, addrServer = channelComunication.recebeMsg(channel)
fileClient.close()
print("Arquivo Transferido\n")
channelComunication.finalizaConexao(channel)



