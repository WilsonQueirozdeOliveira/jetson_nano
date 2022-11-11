import socket

HOST = '192.168.3.200'
PORT = 50007

BUFER_SIZE = 1024 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
    
    s.sendto(b'string from client',(HOST, PORT))

    data_from_server = s.recvfrom(BUFER_SIZE)

    print('Received: ', repr(data_from_server))