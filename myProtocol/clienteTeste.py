from myProtocol import channelComunication
from myProtocol import Cechahn
import time


fileOrigem = "/home/jessica/Documentos/teste/teste.txt"
fileDest = "/home/jessica/Documentos/teste.txt"
HOST = ''
PORT = 3400
dest = (HOST,PORT)
channel = channelComunication.iniciaConexao()
connect = Cechahn.CONNECT()
channelComunication.enviaMsg(dest,channel,connect)
time.sleep(5.0)
get = Cechahn.GET(fileOrigem,fileDest)
channelComunication.enviaMsg(dest,channel,get)
seq = 1
time.sleep(2)
ack = Cechahn.ACK(seq)
channelComunication.enviaMsg(dest,channel,ack)
seq  = 1
channelComunication.enviaMsg(dest,channel,ack)



