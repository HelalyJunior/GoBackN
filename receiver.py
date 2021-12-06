import protocol

receiver = protocol.Protocol('receiver')
receiver.startSim() #starts the connection
fullMessage=[]
while True:
    
    frame = receiver.fromPhysicalLayer() #receive the frame
    
    if frame.seqNum != receiver.frame_expected: #if it's not correct , then return it 
        receiver.toPhysicalLayer(frame)

    while(frame.seqNum != receiver.frame_expected): #keep ignoring till you get the retransmission of the corrupted frame
        print("IGNORING")
        frame = receiver.fromPhysicalLayer()
        
    frame.frameType='ack'
    print("I just received " + str(frame.seqNum) + " value: " + str(frame.info))
    fullMessage.append(frame.info)
    receiver.toPhysicalLayer(frame)
            

    receiver.frame_expected =  (receiver.frame_expected + 1) % (int(receiver.MAX_SEQ))
    
    if receiver.frame_expected ==0: #after the 8-frame message is fully sent , print it
        print(fullMessage)

    

