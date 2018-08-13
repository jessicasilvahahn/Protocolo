from CechahnServidor import channelComunication
from CechahnServidor import Cechahn
import os

# ESTADOS DA MAQUINA PARA CLIENTE E SERVIDOR
# IDLE = 0
# ESPERA_ACK = 1
# PEDE_ARQUIVO = 2
# ESPERA_ACK_GET = 3
# ESPERA_DADOS = 4
# FINALIZA_CONEXAO = 5
# ESPERA_GET = 6
# ENVIA_DADO = 7
# ERROR = 8

def FSMServer(estadoIncial,canal):

    global estado, opcode, host, ori, dest, port, canalUdp, sizeFile, ackAnterior
    estado = estadoIncial
    canalUdp = canal

    if(estado==0):
        print("IDLE\n")
        # ler a mensagem do canal
        msg, cliente = channelComunication.recebeMsg(canalUdp)
        #pega o cliente que se comunicar através do canal
        opcode, msg = Cechahn.splitMsg(msg)

        if opcode == 1:
            print("RECEBIDO UM CONNECT\n")
            numseq = 1
            #cria ACK
            msgAck = Cechahn.ACK()
            dest = (cliente[0], cliente[1])
            byte = channelComunication.enviaMsg(dest, canalUdp, msgAck)
            print("Byte Recebido", byte)
            estado = 6
        else:
            estado = 0

    if(estado==6):
        print("ESPERA_GET\n")
        # ler a mensagem do canal
        msg, cliente = channelComunication.recebeMsg(canalUdp)
        opcode, fileOrig, fileDest = Cechahn.splitMsgDelimitador(msg)
        if opcode == 2:
            print("RECEBEU GET\n")
            sizeFile = os.path.getsize(fileOrig)
            print("tamanho arquivo",sizeFile)
            msgAckGet = Cechahn.ACK_GET(sizeFile)
            bytes = channelComunication.enviaMsg(dest, canalUdp, msgAckGet)
            print("Byte Recebido\n",bytes)
            estado = 7  # ENVIA_DADO
        else:
            estado = 6

    if(estado==7):
        print("ENVIA_DADO\n")
        # envia Arquivo
        try:
            File = open(fileOrig, 'r')
        except ValueError:
            estado = 8  # ERROR
        if estado != 8:
            ackAtual = 1
            data = File.read(512)
            print("data lido:",data,"\n")
            while(data):
                ackAnterior = ackAtual
                print("Dado a ser enviado:",data)
                #criar pacote data
                dataSend = Cechahn.DATA(data,ackAtual)
                print("Data SEND:",dataSend,"\n")
                print("destino",dest)
                if (channelComunication.enviaMsg(dest, canalUdp, dataSend)):
                    msg, cliente = channelComunication.recebeMsg(canalUdp)
                    dest = (cliente[0],cliente[1])
                    print("cliente envou",msg)
                    print("ack")
                    isAck, seq = Cechahn.splitMsg(msg)
                    print("numero sequencial",seq)
                    if isAck == 5:
                        binario = bin(ackAnterior)
                        #ackAnteriorBytes = bytes(binario,'utf-8')
                        #print("AckAnterior (bytes):",ackAnteriorBytes,"Ack Recebido (bytes):",seq)
                        if binario==seq:
                            print("proximo bloco\n")
                            ackAtual = ackAtual + 1
                            # proximo bloco
                            data = File.read(512)
                        else:
                            print("RETRANSMISSÃO\n")
                            channelComunication.enviaMsg(dest, canalUdp, dataSend)


            estado = 5
    if estado == 8:
        print("ERROR\n")
        msgErro = Cechahn.ERROR()
        channelComunication.enviaMsg(dest, canalUdp, msgErro)
        estado = 5  # FINALIZA

    if(estado==5):
        print("FINALIZA_CONEXÃO\n")
        msgFinish = Cechahn.FINISH()
        bytes = channelComunication.enviaMsg(dest, canalUdp, msgFinish)
        print("Byte Recebido\n", bytes)
        msg, cliente = channelComunication.recebeMsg(canalUdp)
        isAck, seq = Cechahn.splitMsg(msg)
        if isAck == 5:
            estado = 0
        else:
            estado = 5

#inicia canal de comunicacao
HOST = ''              # Endereco IP do Servidor
PORT = 3400            # Porta que o Servidor esta
canal = channelComunication.iniciaConexao()
orig = (HOST, PORT)
channelComunication.bindServer(canal,orig)
estadoIncial = 0

while True:
    FSMServer(estadoIncial,canal)
