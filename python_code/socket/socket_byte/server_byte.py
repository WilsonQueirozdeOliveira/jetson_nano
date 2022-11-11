import socket 

HOST = '192.168.3.202'
PORT = 9999

BUF_SIZE = 1024 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:

    s.bind((HOST, PORT))

    while(True):

        data_from_client = s.recvfrom(BUF_SIZE)

        client_msg , client_address = data_from_client

        print('data_from_client: ', data_from_client)

        print('client_msg: ', client_msg)

        print('client_address: ', client_address)

        s.sendto(b'string from server', client_address)
