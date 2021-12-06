from enum import Enum
from os import error
import socket
import pickle

HOST = '127.0.0.1' #only client that is on this computer will access the socket
PORT = 5000


class Packet:
    def __init__(self,data,seqNum):
        self.data = data    # the data sent
        self.seqNum = seqNum # sequence number needed for retransmission


class Frame_kind(Enum):
    data = 1 
    ack  = 2
    nak  = 3
    
    
class Frame:
    def __init__(self,info,frameType,seqNum):
        self.info = info    # the data sent
        self.seqNum = seqNum # sequence number needed for retransmission
        self.frameType=frameType # can be ack , nak or data
        
class Protocol:   
    errorFlag=1
    MAX_SEQ=8
    next_frame_to_send = 0
    frame_expected = 0 
    buffer = ['0'] * (int(MAX_SEQ))
    
    def __init__(self, role):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #using IPV4 and TCP 
        self.type = role
        if(self.type == "Sender"):
            self.socket.bind((HOST, PORT))
    
    def startSim(self):
        if(self.type == "Sender"):
            self.socket.listen() #start listening for client that tries to connect
            self.conn, self.addr = self.socket.accept()
        else:
            self.socket.connect((HOST, PORT))
            print("Reciever connected succesfully")
        
    def fromNetworkLayer(self):
        packet = input()
        return packet
    
    def toPhysicalLayer(self,data):
        frame=pickle.dumps(data)
        if(self.type == "Sender"):
            self.conn.sendall(frame)
        else:
            self.socket.sendall(frame)
            
    def fromPhysicalLayer(self):
        if(self.type == "Sender"):
            data = self.conn.recv(1024)
            data = pickle.loads(data)
            return data
        else:
            data = self.socket.recv(1024)
            data = pickle.loads(data)
            if(data.seqNum==3 and self.errorFlag==1): #manually corrupting the received frame
                print('CREATING ERROR')
                self.errorFlag=0
                data.info='wrong data'
                data.seqNum=2
            return data

    def send_data(self,seq_nr,fk='data'):
        info=self.buffer[seq_nr]
        frame=Frame(info,fk,seq_nr)
        self.toPhysicalLayer(frame)        
    