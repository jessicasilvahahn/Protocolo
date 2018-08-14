from Cechahn_Cliente_Servidor import channelComunication
from Cechahn_Cliente_Servidor import Cechahn
import os
from pathlib import Path

def FSMCliente(estado, canalUdp,dest):
    if (estado == 0):
        print("IDLE")
        msgConnect = Cechahn.CONNECT()
        channelComunication.enviaMsg(dest, canalUdp, msgConnect)
        estado = 1
    if (estado == 1):
        print('ESPERA_ACK')
        # fazer logica ainda do timer, para verificar esse timer_on e se timerout.
        while True:
            msgBytes, addr = channelComunication.recebeMsg(canalUdp)
            opcode, msg = Cechahn.splitMsg(msgBytes)
            if (opcode == 8):  # opcode do ACK é 8
                print("Ack recebido")
                estado = 2
                break
            else:
                print("Ack não recebido")
                estado = 1
    if (estado == 2):
        print('PEDE ARQUIVO')
        fileOrigem = input('Insira o nome do Arquivo (com caminho absoluto) que deseja transferir: \n')
        fileDestino = input('\nInsira onde deseja armazenar o arquivo: \n')
        msgGet = Cechahn.GET(fileOrigem, fileDestino)
        channelComunication.enviaMsg(dest, canalUdp, msgGet)
        estado = 3

    if (estado == 3):
        print('ESPERA ACK_GET')
        msgBytes, addr = channelComunication.recebeMsg(canalUdp)
        opcode, numSeq, tamanhoFile = Cechahn.splitMsgDelimitador(msgBytes)
        if (opcode == 4):  # opcode do ACK_GET
            estado = 4
        if (opcode == 7):  # opcode do FINISH
            msgAck = Cechahn.ACK(numSeq)
            channelComunication.enviaMsg(dest, canalUdp, msgAck)
            estado = 5
        if(opcode==6):
            print("ERRO OCORRIDO\n")
            estado = 5

    if (estado == 4):
        print('ESPERA_DADOS')
        try:
            if(Path(fileDestino).suffix == '.txt'):
                fileClient = open(fileDestino, 'w+')
            else:
                estado = 6
        except ValueError:
            estado=6

        if estado!=6:
            msgBytes, addr = channelComunication.recebeMsg(canalUdp)
            opcode,data, numSeq = Cechahn.splitMsgSeq(msgBytes)
            numAtual = numSeq
            numAnterior = 0
            dest = (addr[0],addr[1])
            if (opcode == 3):  # opcode de DATA
                while opcode!=7:
                    #manda ack
                    msgAck = Cechahn.ACK_DATA(numSeq)
                    channelComunication.enviaMsg(dest, canalUdp, msgAck)
                    if numAtual!=numAnterior:
                        print("Enviando ...", data, "\n")
                        print("DATA", data, "\n")
                        fileClient.write(data)
                    numAnterior = numAtual
                    msgBytes, addr = channelComunication.recebeMsg(canalUdp)
                    opcode, data, numSeq = Cechahn.splitMsgSeq(msgBytes)
                    numAtual = numSeq
                    dest = (addr[0], addr[1])
                    msgAck = Cechahn.ACK_DATA(numSeq)
                    channelComunication.enviaMsg(dest, canalUdp, msgAck)
                    if (opcode == 6):  # opcode de ERROR
                        msgAckError = Cechahn.ACK()
                        channelComunication.enviaMsg(dest, canalUdp, msgAckError)
                        estado = 5

                fileClient.close()
                msgAckFinish = Cechahn.ACK()
                channelComunication.enviaMsg(dest, canalUdp, msgAckFinish)
                print("Arquivo Transferido\n")
                estado = 5

    if (estado == 5):
        print('FINALIZA_CONEXAO')
        msgAckFinish = Cechahn.ACK()
        channelComunication.enviaMsg(dest, canalUdp, msgAckFinish)
        channelComunication.finalizaConexao(canalUdp)

    if(estado==6):
        print("ERRO AO COPIAR ARQUIVO PARA CAMINHO DE DESTINO OU ERRO AO ENCONTRAR ARQUIVO DE ORIGEM\n")
        print('FINALIZA_CONEXAO')
        channelComunication.finalizaConexao(canalUdp)



host = ''
port = 3400
canalUdp = channelComunication.iniciaConexao()
dest = (host, port)
estado = 0

FSMCliente(estado, canalUdp,dest)