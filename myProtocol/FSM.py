#canal de comunicacao via socket udp
from myProtocol import channelComunication
import time
from threading import *
from myProtocol import Cechahn

class FSM():
    def __init__(self):
        #ESTADOS DA MAQUINA PARA CLIENTE E SERVIDOR
        self.estado = 0
        self.time_on = False
        self.time_out = False
        self.erro = 0
        #IDLE = 0
        #ESPERA_ACK = 1
        #PEDE_ARQUIVO = 2
        #ESPERA_ACK_GET = 3
        #ESPERA_DADOS = 4
        #FINALIZA_CONEXAO = 5
        #ESPERA_GET = 6
        #ENVIA_DADO = 7
        #ERROR = 8


    def FSMServidor(self,msgBytes):
        if(self.estado==0):
            print("IDLE")
            opcode, msg = Cechahn.splitMsg(msgBytes)
            host = ''
            port = 3400
            #canal de comunicacao bidirecional
            canalUdp = channelComunication.iniciaConexao()
            orig = (host, port)
            channelComunication.bindServer(canalUdp, orig)
            while True:
                msg, cliente = channelComunication.recebeMsg(canalUdp)
                if(opcode==1):
                    print(str(msg,'utf-8'))
                    seq = 1
                    #cria ACK
                    ack = Cechahn.ACK(seq)
                    dest = (cliente[0],cliente[1])
                    channelComunication.enviaMsg(dest,canalUdp,ack)
                    break

            self.estado = 6

        if(self.estado==6):
            print("ESPERA_GET")
            self.time_on == True #disparar timer / chamar método correspondente
            #se estourou o timer
            if(self.time_out==True):
                #monta msg de FINISH
                msgByteFinish = Cechahn.FINISH()
                #envia msg para cliente
                channelComunication.enviaMsg(dest,canalUdp,msgByteFinish)
                self.estado = 5 #finaliza conexao
            else:
                while True:
                    msgGet = channelComunication.recebeMsg(canalUdp)
                    opcode, fileOrig, fileDest = Cechahn.splitMsgDelimitadorGET(msgGet)
                    if(opcode==2): break

                #mandar ACK_GET
                seq = 1
                #Pegar tamanho do arquivo
                try:
                    File = open(fileOrig,'r')
                except ValueError:
                    self.erro = 1
                    self.estado=8 #ERROR

                sizeFile = len(File)
                msgAckGet = Cechahn.ACK_GET(seq,sizeFile)
                channelComunication.enviaMsg(dest,canalUdp,msgAckGet)
                self.estado = 7 #ENVIA_DADO

        if(self.estado==7):
            print("ENVIA_DADO")
            #TERMINAR
            #VERFICAR SE O PACOTE É UM ACK, TEM QUE VERFICAR SE O NUMERO SEQUENCIAL É O MESMO DO PACOTE ANTERIOR
            #CASO FOR, RESTRANSMITIR PACOTE, CASO NAO FOR ENVIO O PRÓXIMO PACOTE

        if(self.estado==8):
            print("ERROR")
            msgErro = Cechahn.ERROR()
            channelComunication.enviaMsg(dest,canalUdp,msgErro)
            self.estado = 5 #FINALIZA

        if(self.estado==5):
            print("FINALIZA_CONEXÃO")
            #ENVIA FINISH
            #espera o ack, se nao receber ack aguarda ate estourar p timeout, se estourar timeout, restransmit finish, se recebe ack fecha
            #o socket e muda estado para idle









    def Tempo():
        print(time.ctime())
        t = Timer(5.0, Tempo)
        t.start()

