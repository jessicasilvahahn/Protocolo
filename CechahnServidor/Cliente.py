from CechahnServidor import channelComunication
from CechahnServidor import Cechahn


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
        fileOrigem = input('Insira o nome do Arquivo (com caminho absoluto) que deseja transferir:')
        fileDestino = input('Insira onde deseja armazenar o arquivo')
        msgGet = Cechahn.GET(fileOrigem, fileDestino)
        channelComunication.enviaMsg(dest, canalUdp, msgGet)
        timer_on = True
        estado = 3

    if (estado == 3):
        print('ESPERA ACK_GET')
        msgBytes, addr = channelComunication.recebeMsg(canalUdp)
        opcode, numSeq, tamanhoFile = Cechahn.splitMsgDelimitador(msgBytes)
        if (opcode == 4):  # opcode do ACK_GET
            timer_on = True
            estado = 4
        if (opcode == 7):  # opcode do FINISH
            msgAck = Cechahn.ACK(numSeq)
            channelComunication.enviaMsg(dest, canalUdp, msgAck)
            estado = 5
    if (estado == 4):
        print('ESPERA_DADOS')
        msgBytes, addr = channelComunication.recebeMsg(canalUdp)
        print("BYTES", msgBytes, "\n")
        opcode,numSeq, data = Cechahn.splitMsgDelimitador(msgBytes)  # Mexer na logica pra retornar numSeq
        dest = (addr[0],addr[1])
        # pegar opcode da mensagem e comparar, while opcode da mensagem for diferente do opcode FINISH(), escreve no arquivo
         # 7 é o opcode do FINISH e 6 do ERROR
        if (opcode == 3):  # opcode de DATA
            while opcode!=7:
                print("Enviando ...", numSeq, "\n")
                print("DATA",numSeq,"\n")
                fileClient = open(fileDestino, 'w')
                fileClient.write(numSeq)
                #manda ack
                #opcode, data, numSeq = Cechahn.splitMsgDelimitador(data)  # numSeq mexer na funcao de slipt pra retornar
                print("numero seq",data,"\n")
                msgAck = Cechahn.ACK_DATA(data)
                channelComunication.enviaMsg(dest, canalUdp, msgAck)
                msgBytes, addr = channelComunication.recebeMsg(canalUdp)
                print("BYTES", msgBytes, "\n")
                opcode, data, numSeq = Cechahn.splitMsgDelimitador(msgBytes)  # Mexer na logica pra retornar numSeq
                dest = (addr[0], addr[1])
                print("numero seq", data, "\n")
                msgAck = Cechahn.ACK_DATA(data)
                channelComunication.enviaMsg(dest, canalUdp, msgAck)
                # Implementar logica do timerout se buffer !=0, enviar o ultimo ACK'
                if (opcode == 6):  # opcode de ERROR
                    msgAckError = Cechahn.ACK()  # tratar diferenciacao entre ack do data e ack do erro, finish e connect que nao tem numSeq
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


host = ''
port = 3400
canalUdp = channelComunication.iniciaConexao()
dest = (host, port)
estado = 0

FSMCliente(estado, canalUdp,dest)