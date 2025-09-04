import socket
import json
import threading
from Player import Player
from UDPserver import GameServer

class GameClient:
    def __init__(self, player_num,p1_choice,p2_choice,lobby_id,game):
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_port = 16000 + 10* int(lobby_id) 
        self.server_address = ("127.0.0.1", self.server_port)
        self.local_player_num = player_num
        self.lobby_id = lobby_id
        self.game = game
        
        
        if player_num == 1:
            # If the local player is player 1, create a GameServer
            self.local_player = Player(1, p1_choice, ai_mode=False, online=False,client_sock=self.game_socket,serv_address=self.server_address)
            self.remote_player = Player(2 ,p2_choice, ai_mode=False, online=True,client_sock=self.game_socket,serv_address=self.server_address)
            self.game_server = GameServer(lobby_id)
            self.game_server.start()
            
        else:
            # Initialize players based on local player number
            self.local_player = Player(2, p2_choice, ai_mode=False, online=False,client_sock=self.game_socket,serv_address=self.server_address)
            self.remote_player = Player(1, p1_choice,ai_mode=False, online=True,client_sock=self.game_socket,serv_address=self.server_address)
        
        

           
        local_port = self.server_port + int(player_num)

        print(f"Local port: {local_port}")
        

        try:
            self.game_socket.bind(("127.0.0.1", local_port))
        except Exception as e:
            print(f"Error binding socket: {e}")
            

     
        self.lock = threading.Lock()
        self.is_running = False
        
        
        

    def start(self):
        with self.lock:
            self.is_running = True

        thread = threading.Thread(target=self.receive_messages)
        thread.start()

   
    def receive_messages(self):
        running = True
        while running:
            with self.lock:
                if not self.is_running:
                    running = False

            try:
                
              
                
                # receives data from socket as a tuple, code that comes after is blocked until data received
                data = self.game_socket.recvfrom(1024)
                decoded_data = data[0].decode('utf-8')
                deserialised_data = json.loads(decoded_data)
                #print(f"Received UDP message from : {decoded_data}")
                
                
                self.remote_player.char.update_movement(deserialised_data)
                
         
                    
                
            except socket.error as e:
                print(f"Error receiving data: {e}")
                
          

   

            




            
            
