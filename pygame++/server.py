import socket
import threading
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Server():


    def __init__(self,data) -> None:
        self.data = data
        self.conn = None
    
    def launch(self):
        thread = threading.Thread(target=self.start)
        thread.start()



    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    print("Other player disconnected")
                    connected = False
                elif 'rqst' in msg:
                    self.send(json.dumps(self.data[msg.split(',')[1]]),conn)
                else:
                    print(msg)
                
        
        conn.close()

    def send(self,msg, conn):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def start(self):
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER} ")
        # while True:
        self.conn, addr = server.accept()
        thread = threading.Thread(target=self.handle_client, args=(self.conn, addr))
        thread.start()
                

