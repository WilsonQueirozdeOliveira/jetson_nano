import socket

HOST = '192.168.3.202'
PORT = 9999

BUF_SIZE = 1024 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
    
    s.sendto(b'string from client',(HOST, PORT))

    data_from_server = s.recvfrom(BUF_SIZE)

    server_msg , server_address = data_from_server

    print('data_from_server: ', repr(data_from_server))
    
    print('server_msg: ', server_msg)

    print('server_address: ', server_address)