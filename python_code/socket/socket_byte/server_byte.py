import socket 

HOST = '192.168.3.202'
PORT = 9999

BUFER_SIZE = 1024 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:

    s.sendto(b'string from server',(HOST, PORT))

    data_from_client = 0

    while(not data_from_client):

        data_from_client = s.recvfrom(1024)

        print('data_from_client', data_from_client)
