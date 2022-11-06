# Echo server program
import socket

HOST = '192.168.3.200'    # ip from server
PORT = 50007              # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
                        socket.IPPROTO_UDP) as s:
    s.bind((HOST, PORT))

    print("UDP server up and listening")

    data_recived = 0

    while(not data_recived):

        data_recived = s.recvfrom(1024)
        
        print('Received data_recived[0]: ', 
        data_recived[0])# client massage
        
        print('Received data_recived[1]: ', 
        data_recived[1])# client adress
  
        # Sending a reply to client
        s.sendto(b'hello from server udp', 
        data_recived[1])
        
