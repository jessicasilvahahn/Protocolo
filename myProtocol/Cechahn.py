
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

def DATA(data):
    return data

def ACK_GET(numeroSeq,fileSize):
    bnum = bin(numeroSeq)
    bsize = bin(fileSize)
    opcode = 4
    separador = 0
    msgACK_GET = opcode.to_bytes(1,'big') + bytes(bnum,'utf-8') + separador.to_bytes(1,'big') + bytes(bsize,'utf-8')
    return msgACK_GET

def ACK(numeroSeq):
    opcode = 5
    opByte = opcode.to_bytes(1,'big')
    bnumSeq = bytes(bin(numeroSeq),'utf-8')
    msgACK = opByte + bnumSeq
    return msgACK

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
    print(msgBytes)
    vetorMsg = list(msgBytes)
    print(vetorMsg)
    opcode = vetorMsg[0]
    print(opcode)
    msg = bytearray(vetorMsg[1:len(vetorMsg)])
    return opcode,str(msg,'utf-8')

def splitMsgDelimitadorGET(msgBytes):
    print(msgBytes)
    vetorMsg = list(msgBytes)
    print(vetorMsg)
    opcode = vetorMsg[0]
    print(opcode)
    stringMsg = str(msgBytes,'utf-8')
    delimitador =  stringMsg.find("\x00")
    print("pos",delimitador)
    origem = vetorMsg[1:delimitador]
    print(str(bytearray(origem),'utf-8'))
    destino = vetorMsg[delimitador+1:len(vetorMsg)]
    print(str(bytearray(destino),'utf-8'))
    stringOrigem = str(bytearray(origem),'utf-8')
    stringDestino = str(bytearray(destino),'utf-8')
    return opcode,stringOrigem,stringDestino


#testando
#msg = CONNECT()
#print(msg)
#print(type(msg))
#print(splitMsg(msg))

#op,s1,s2 = splitMsgDelimitadorGET(GET("/home/jessica/teste1.txt","teste2.txt"))
#print("aqui",s1,s2,op)

#print(FINISH())
