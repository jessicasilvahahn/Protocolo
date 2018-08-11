
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
    opcode = 3
    opByte = opcode.to_bytes(1,'big')
    bnum = bin(numSeq)
    separador = 0
    dataBytes = bytes(data, 'utf-8')
    msgData = opByte + dataBytes + separador.to_bytes(1,'big') + bytes(bnum,'utf-8')
    return msgData

def ACK_GET(fileSize):
    bsize = bin(fileSize)
    opcode = 4
    msgACK_GET = opcode.to_bytes(1,'big') + bytes(bsize,'utf-8')
    return msgACK_GET

def ACK_DATA(numeroSeq):
    opcode = 5
    opByte = opcode.to_bytes(1,'big')
    bnumSeq = bytes(bin(numeroSeq),'utf-8')
    msgACK = opByte + bnumSeq
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
    print(opcode)
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
