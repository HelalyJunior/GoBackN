import protocol

sender = protocol.Protocol('Sender')
sender.startSim()
errorFlag=False
frameToReTransmit=None
while True:
    
    while errorFlag: #if an error occured
        while sender.next_frame_to_send<sender.MAX_SEQ: #keep sending till you hit the maximum of the buffer
            data=sender.fromNetworkLayer()
            packet = protocol.Packet(data,sender.next_frame_to_send)
            sender.buffer[sender.next_frame_to_send]=packet.data
            sender.send_data(sender.next_frame_to_send)
            sender.next_frame_to_send = sender.next_frame_to_send + 1
            
        sender.next_frame_to_send=frameToReTransmit #start sending from the corrupted frame
        
        while sender.next_frame_to_send<sender.MAX_SEQ:
            sender.send_data(sender.next_frame_to_send)
            print("Retransmitting frame # " + str(sender.next_frame_to_send))
            ack=sender.fromPhysicalLayer()
            print('acknowledge received for frame no. #' + str(ack.seqNum))
            sender.next_frame_to_send =  sender.next_frame_to_send + 1
        sender.next_frame_to_send=0 #after retransmitting , start new 8-frame message
        errorFlag=False
            
                
                    
    data=sender.fromNetworkLayer() #get packet from network layer represented by keyboard
    packet = protocol.Packet(data,sender.next_frame_to_send) #create packet from the data received
    sender.buffer[sender.next_frame_to_send]=packet.data #add it to the buffer
    sender.send_data(sender.next_frame_to_send,packet) #internally uses the toPhysicalLayer()
    print('sending frame no. #' + str(sender.next_frame_to_send))
    ack=sender.fromPhysicalLayer()
    print('acknowledge received for frame no. #' + str(ack.seqNum))
    if 'ack' != ack.frameType or ack.seqNum != sender.next_frame_to_send: #if an error occurs
        print('Error occured in transmitting frame no. #' + str(sender.next_frame_to_send))
        errorFlag=True
        frameToReTransmit=sender.next_frame_to_send
        
    
    sender.next_frame_to_send =  (sender.next_frame_to_send + 1) % (int(sender.MAX_SEQ)) #increment the frame
        