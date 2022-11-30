import socket
import json

HEADER = 64
PORT = 5050
SERVER = "10.244.254.229"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)


class Client():
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        response = input("Enter IP Address or select an option below:\n1) Heritage \n2) BYUI \n3) Heritage Girls\n>")
        if response == '1':
            self.client.connect(('10.11.6.55', PORT))
        elif response == '2':
            self.client.connect(('10.244.6.55', PORT))
        elif response == '3':
            self.client.connect(('10.10.7.82', PORT))
        else:
            self.client.connect((response, PORT))

    def send(self,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        # print("Waiting for server...")
        return self.handle_response()
        
    def handle_response(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                return json.loads(msg)
    
