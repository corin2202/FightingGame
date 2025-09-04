import socket
import threading
import uuid
import json
import pygame

from Lobby import Lobby


class LobbyClient:
    def __init__(self):
        self.lobby_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.client_id = str(uuid.uuid4())
        self.lobbies = Lobby()
        self.last_lobby_request = 0
        pygame.init()
        
        
    def get_lobby_data(self):
        return self.lobbies.get_lobby_data()
    
    def max_lobbies_reached(self):
        return self.lobbies.max_lobbies_reached()
    
    def get_client_id(self):
        return self.client_id
    
  
       
        
    def close_connection(self):
        request = "close"
        self.lobby_socket.send(request.encode("utf-8")[:1024])
        response = self.receive_lobby_data()
        if response == "closed":
            self.lobby_socket.close()
    
        print("Closed connection to server")
        

    def connect(self):
        while not self.connected:
            self.lobby_socket.connect(("127.0.0.1", 8000))
            msg = f"Connection from {self.client_id}"
            self.lobby_socket.send(msg.encode("utf-8")[:1024])
            response = self.receive_lobby_data()
            if response == "accepted":
                self.connected = True
                
    def join_game(self,lobby_id):
        try:
            request = f"Join lobby {lobby_id} by client {self.client_id}"
            self.lobby_socket.send(request.encode("utf-8")[:1024])
            response = self.receive_lobby_data()
        
            
        
        except Exception as e:
            print(f"Error: {e}")
    
    
    def send_character(self,character,lobby_id,player_num):
        try:
            
            request = f"Choose character {character} lobby {lobby_id} player {player_num}"
            self.lobby_socket.send(request.encode("utf-8")[:1024])
            response = self.receive_lobby_data()
            return response
            
        except Exception as e:
            print(f"Error: {e}")
    
    def host_game(self):
        try:
            request = f"{self.client_id},H"
            self.lobby_socket.send(request.encode("utf-8")[:1024])
            response = self.receive_lobby_data()
            return response
            
    
        except Exception as e:
            print(f"Error: {e}")
            
             
    def receive_lobby_data(self):
        return self.lobby_socket.recv(1024).decode("utf-8")
    

    def check_game_empty(self,lobby_id):
        lobby_data = self.get_lobby_data()
        if len(lobby_data[lobby_id]["players"]) == 1:
            return True
    
    def check_lobby_update(self,ping_time = 500):
        try:
                # every 1 seconds that pass, send a lobby request for the lobby data
                if pygame.time.get_ticks() - self.last_lobby_request >= ping_time:
                    self.last_lobby_request = pygame.time.get_ticks()
         
                    request = "lobby"
                    self.lobby_socket.send(request.encode("utf-8")[:1024])
                
                    # receive request here and set the received data to the lobby data
                    response = self.receive_lobby_data()
                    response = json.loads(response)
                    
                
                    if isinstance(response,dict):
                        self.lobbies.set_lobby_data(response)
                        
                    
            
                
        except Exception as e:
            print(f"Error: {e}")
         
         
    def lobby_client_delete_id(self,client_id):
        self.lobbies.delete_client_id(client_id)
        
        
        
                
        
           
        
        



            
        


