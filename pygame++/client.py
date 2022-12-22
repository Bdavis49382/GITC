import socket
import json
import csv

HEADER = 64
PORT = 5050
SERVER = "10.244.254.229"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)


class Client():
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_via_terminal()
    
    def connect_via_terminal(self):
        try:
            with open('pygame++/saved_servers.csv','r') as saved_servers:
                servers = csv.reader(saved_servers)
                addresses = []
                option = 1
                for server in servers:
                    print(f'{option}) {server[1]}({server[0]})')
                    addresses.append(server[0])
                    option += 1

                response = input("Enter IP Address or select an option from above:\n>")
                try:
                    if len(response) == 1:
                        self.client.connect((addresses[int(response)-1], PORT))
                    else:
                        server_name = input("what would you like to call this server?")
                        with open('pygame++/saved_servers.csv','a') as write_file:
                            write_file.write(f'\n{response},{server_name}')
                        self.client.connect((response, PORT))
                except:
                    print('there was an issue connecting')
        except FileNotFoundError:
            response = input("You have no saved ip addresses.\nPlease enter your server's ip address\n>")
            with open('pygame++/saved_servers.csv','w') as write_file:
                server_name = input("what would you like to call this server?")
                write_file.write(f'{response},{server_name}')
            self.client.connect((response, PORT))
    

    def send(self,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        return self.handle_response()
        
    def handle_response(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(FORMAT)
            return json.loads(msg)
    
