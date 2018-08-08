#canal de comunicacao via socket udp
from myProtocol import channelComunication
import time
from threading import *
from myProtocol import Cechahn
import os

class FSM:
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

    def __init__(self):
        self.time_on  = False
        self.time_out = False

    def FSMServidor(self,canal):
        global estado,opcode,host,ori,dest,port,canalUdp,sizeFile,ackAnterior
        canalUdp = canal
        estado = 0
        if estado==0:
            sizeFile = None
            msgBytes, cliente = channelComunication.recebeMsg(canalUdp)
            print("IDLE\n")
            ackAnterior = 1
            opcode, msg = Cechahn.splitMsg(msgBytes)
            msg, cliente = channelComunication.recebeMsg(canalUdp)
            print(msg)
            if opcode==1:
                seq = 1
                #cria ACK
                ack = Cechahn.ACK(seq)
                dest = (cliente[0],cliente[1])
                r = channelComunication.enviaMsg(dest,canalUdp,ack)
                estado = 6
            else: estado = 0
        pass

        if estado==6:
            print("ESPERA_GET\n")
            self.time_on = True #disparar timer / chamar método correspondente
            #self.TempoServer(5.0)
            #se estourou o timer
            if self.time_out==True:
                #monta msg de FINISH
                msgByteFinish = Cechahn.FINISH()
                #envia msg para cliente
                r = channelComunication.enviaMsg(dest,canalUdp,msgByteFinish)
                estado = 5 #finaliza conexao
            else:
                #msgGet,cliente = channelComunication.recebeMsg(canalUdp)
                opcode, fileOrig, fileDest = Cechahn.splitMsgDelimitadorGET(msg)
                print("caminhos\n")
                print(fileOrig,"\n")
                print(fileDest,"\n")
                if opcode==2:
                    print("GET")
                    #mandar ACK_GET
                    seq = 1
                    #Pegar tamanho do arquivo
                    #Ver se necessario e earrumar se necessario
                    sizeFile = 0
                    msgAckGet = Cechahn.ACK_GET(seq,sizeFile)
                    r  = channelComunication.enviaMsg(dest,canalUdp,msgAckGet)
                    estado = 7 #ENVIA_DADO

                if opcode!=2:
                    estado = 6

        if estado == 7:
            print("ENVIA_DADO\n")
            # VERFICAR SE O PACOTE É UM ACK, TEM QUE VERFICAR SE O NUMERO SEQUENCIAL É O MESMO DO PACOTE ANTERIOR
            # CASO FOR, RESTRANSMITIR PACOTE, CASO NAO FOR ENVIO O PRÓXIMO PACOTE
            #envia Arquivo
            try:
                File = open(fileOrig, 'r')
            except ValueError:
                    estado = 8  # ERROR
            if estado!=8:
                data = File.read(512)
                while(data):
                    print("data")
                    print("oi",data)
                    #envia primeiro dado
                    if (channelComunication.enviaMsg(dest, canalUdp, data.encode())):
                        # espera ACK
                        self.time_on = True
                        #self.TempoServer(5.0)
                        msg,cliente = channelComunication.recebeMsg(canalUdp)
                        isAck,seq = Cechahn.splitMsg(msg)
                        print("seq",seq)
                        if isAck==5:
                            print(ackAnterior)
                            if ackAnterior==seq:
                                print("retrasmissão\n")
                                #retransmite - > nao muda data
                                channelComunication.enviaMsg(dest, canalUdp, data.encode())
                            else:
                                print("proximo bloco\n")
                                ackAnterior = ackAnterior + 1
                                #proximo bloco
                                data = File.read(512)
                estado = 5

        if estado == 8:
            print("ERROR\n")
            msgErro = Cechahn.ERROR()
            channelComunication.enviaMsg(dest, canalUdp, msgErro)
            estado = 5  # FINALIZA

        if estado == 5:
            # espera o ack, se nao receber ack aguarda ate estourar p timeout, se estourar timeout, restransmit finish, se recebe ack fecha
            # o socket e muda estado para idle
            print("FINALIZA_CONEXÃO\n")
            # ENVIA FINISH
            if self.time_out == True:
                estado = 5

            msgFinish = Cechahn.FINISH()
            r = channelComunication.enviaMsg(dest, canalUdp, msgFinish)
            self.time_on = True
            msg, cliente = channelComunication.recebeMsg(canalUdp)
            isAck, seq = Cechahn.splitMsg(msg)
            if isAck==5:
                estado = 0
                channelComunication.finalizaConexao(canalUdp)

            else:
                estado = 5


    def TempoServer(self,sec):
        if self.time_on==True:
            print("Dispara timer\n")
            t = Timer(sec, self.TimeOutServer)
            #dispara timer
            t.start()


    def TimeOutServer(self):
        if self.time_out==False:
            print("Verifica Timeout\n")
            print(time.ctime())
            self.time_out = True
            self.time_on = False






#teste timer
#o = FSM()
#while True:
    #o.Tempo(5.0)
    #print("wait...\n")
    #time.sleep(10)
    #o.time_on = True

#teste Server
host = ''
port = 3400
# canal de comunicacao bidirecional do servidor
canalUdp = channelComunication.iniciaConexao()
orig = (host, port)
channelComunication.bindServer(canalUdp, orig)
fsm = FSM()
while True:
    fsm.FSMServidor(canalUdp)


