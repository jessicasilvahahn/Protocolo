from Cechahn_Cliente_Servidor import channelComunication
from Cechahn_Cliente_Servidor import Cechahn
import os
from pathlib import Path

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
            if(os.path.exists(fileOrig)):
                sizeFile = os.path.getsize(fileOrig)
                msgAckGet = Cechahn.ACK_GET(sizeFile)
                bytes = channelComunication.enviaMsg(dest, canalUdp, msgAckGet)
                estado = 7  # ENVIA_DADO

            else:
                estado = 8

        else:
            estado = 6

    if(estado==7):
        print("ENVIA_DADO\n")
        # envia Arquivo
        if (os.path.isfile(fileOrig)):
            try:
                if (Path(fileOrig).suffix == '.txt'):
                    File = open(fileOrig, 'r')
                else:
                    estado = 8
            except ValueError:
                estado = 8  # ERROR
        else:
            estado=8
        if estado != 8:
            ackAnterior = 1
            data = File.read(512)
            while(data):
                #criar pacote data
                dataSend = Cechahn.DATA(data,ackAnterior)
                print("DATA SEND:",dataSend,"\n")
                if (channelComunication.enviaMsg(dest, canalUdp, dataSend)):
                    msg, cliente = channelComunication.recebeMsg(canalUdp)
                    dest = (cliente[0],cliente[1])
                    isAck, seq = Cechahn.splitMsg(msg)
                    if isAck == 5:
                        binario = bin(ackAnterior)
                        if binario==seq:
                            print("proximo bloco\n")
                            ackAnterior = ackAnterior + 1
                            # proximo bloco
                            data = File.read(512)
                        else:
                            print("RETRANSMISSÃO\n")



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
