import socket
import threading
import json


class GameServer:
    def __init__(self,lobby_id):
        self.lobby_id = lobby_id
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # uses new port for each lobby
        self.server_port = 16000 + 10* int(lobby_id)
        self.server_socket.bind(("127.0.0.1", self.server_port))
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            self.is_running = True

        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def stop(self):
        with self.lock:
            self.is_running = False

    def receive_messages(self):
        while True:
            with self.lock:
                if not self.is_running:
                    break
            try:
                
                data,addr = self.server_socket.recvfrom(1024)
                decoded_data = data.decode("utf-8")
                deserialised_data = json.loads(decoded_data)
            
            
                # player ports are 1/2 ports after the server ports
                # if data coming from player 1, send to player 2, player 2 is one port after p1
                if deserialised_data["player_num"] == 1:
                    serialised_data = json.dumps(deserialised_data)
                    player_2_port = self.server_port + 2
                    self.server_socket.sendto(serialised_data.encode("utf-8"),(addr[0],player_2_port))
                 
                
                # if data coming from player2, send to player 1, player 1 is one port before player 2
                else:
                    serialised_data = json.dumps(deserialised_data)
                    player_1_port = self.server_port + 1
                    self.server_socket.sendto(serialised_data.encode("utf-8"),(addr[0],player_1_port))
                 
                    
            except:
                print("Client not listening.")

    def send_message(self, message, address):
        self.server_socket.sendto(message.encode("utf-8"), address)
            

     
        


