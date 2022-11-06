# Echo client program
import socket

HOST = '192.168.3.200'    # The remote host (ip from server)
PORT = 50007              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
                        socket.IPPROTO_UDP) as s:
    
    s.sendto(b'Hello, world from client udp',(HOST, PORT))

    data_recived = s.recvfrom(1024)

    print('Received: ', repr(data_recived))

    print('Received data[0]: ', data_recived[0])

    print('Received data[1]: ', data_recived[1])
