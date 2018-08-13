
#CONSTRUÇÃO DAS MENSAGENS
def CONNECT():
    opcode = 1
    opByte = opcode.to_bytes(1,'big')
    mensagem = "Estou ouvindo"
    msgBytes = bytes(mensagem,'utf-8')
    msgConnect = opByte + msgBytes
    return msgConnect

def GET(fileOrigem,fileDestino):
    opcode = 2
    separador = 0
    msgGet = opcode.to_bytes(1,'big') + bytes(fileOrigem,'utf-8') + separador.to_bytes(1,'big') + bytes(fileDestino,'utf-8')
    return msgGet

def DATA(data, numSeq):
    print("num enviado",numSeq)
    opcode = 3
    opByte = opcode.to_bytes(1,'big')
    bnum = bin(numSeq)
    separador = 0
    separador2 = "#"
    dataBytes = bytes(data, 'utf-8')
    msgData = opByte + bytes(separador2,"utf-8") + bytes(bnum,'utf-8') + bytes(separador2,"utf-8") + separador.to_bytes(1,'big') + dataBytes

    return msgData

def ACK_GET(fileSize):
    bsize = bin(fileSize)
    opcode = 4
    msgACK_GET = opcode.to_bytes(1,'big') + bytes(bsize,'utf-8')
    return msgACK_GET

def ACK_DATA(numeroSeq):
    opcode = 5
    opByte = opcode.to_bytes(1,'big')
    #bnumSeq = bytes(bin(numeroSeq),'utf-8')
    msgACK = opByte + bytes(numeroSeq,'utf-8')
    print("montando ack",msgACK)
    return msgACK

def ACK():
    opcode = 8
    opByte = opcode.to_bytes(1,'big')
    mensagemAck = "Mensagem Recebida"
    bAck = bytes(mensagemAck, 'utf-8')
    msgAck = opByte + bAck
    return msgAck

def ERROR():
    opcode = 6
    opByte = opcode.to_bytes(1, 'big')
    mensagemErro = "Acesso negado ou Arquivo não encontrado"
    bErro = bytes(mensagemErro, 'utf-8')
    msgErro = opByte + bErro
    return msgErro

def FINISH():
    opcode = 7
    opByte = opcode.to_bytes(1, 'big')
    mensagem = "Finalizando a conexão"
    msgBytes = bytes(mensagem, 'utf-8')
    msgFinish = opByte + msgBytes
    return msgFinish

def splitMsg(msgBytes):
    vetorMsg = list(msgBytes)
    print(vetorMsg)
    opcode = vetorMsg[0]
    msg = bytearray(vetorMsg[1:len(vetorMsg)])
    return opcode,str(msg,'utf-8')

def splitMsgDelimitador(msgBytes):
    vetorMsg = list(msgBytes)
    opcode = vetorMsg[0]
    stringMsg = str(msgBytes,'utf-8')
    delimitador =  stringMsg.find("\x00")
    origem = vetorMsg[1:delimitador]
    destino = vetorMsg[delimitador+1:len(vetorMsg)]
    stringOrigem = str(bytearray(origem),'utf-8')
    stringDestino = str(bytearray(destino),'utf-8')
    return opcode,stringOrigem,stringDestino

def splitMsgSeq(msgBytes):
    vetorMsg = list(msgBytes)
    opcode = vetorMsg[0]
    if opcode==7:
        num = 0
        data = str(bytearray(vetorMsg[1:len(vetorMsg)]),"utf-8")
    else:
        stringMsg = str(msgBytes, 'utf-8')
        seq = stringMsg.split("#")
        num = seq[1]
        data = stringMsg.split("\x00")

    return opcode,data[1],num



