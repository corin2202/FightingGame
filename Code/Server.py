import socket
import threading
import json
import re

from Lobby import Lobby


class LobbyServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 8000))
        self.server.listen(5)
        # creats dict of socket:client_id
        self.clients = {}
      
        self.lock = threading.Lock()
        self.lobbies = Lobby()

    def start(self):
        server_address, port_number = self.server.getsockname()
        print(f"Listening on {server_address}:{port_number}")

        try:
            while True:
                client_socket, addr = self.server.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")
                with self.lock:
                    self.clients[client_socket] = ""
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
                
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            self.server.close()
            
    def handle_client(self, client_socket, addr):
        try:
            while True:
                request = client_socket.recv(1024).decode("utf-8")

                if request.lower() == "close":
                    client_socket.send("closed".encode("utf-8"))
                    break

                print(f"Received: {request}")

                if re.search(".*,H$", request):
                    host_id = request.split(",")[0]
                    self.lobbies.create_lobby(host_id)
                    response = "Received"
                    client_socket.send(response.encode("utf-8"))
                
                elif re.search("Connection from",request):
                    client_id = request.split(" ")[2]
                    self.clients[client_socket] = client_id
                    response = "accepted"
                    client_socket.send(response.encode("utf-8"))
             
                elif request == "lobby":
                    lobby_data = self.lobbies.get_lobby_data()
                    response = json.dumps(lobby_data)
                    client_socket.send(response.encode("utf-8"))
                    
                elif re.search("^Join lobby",request):
                    # splits request into list with individual elements
                    request_split = request.split(" ")
                    # third element is the lobby id
                    lobby_id = int(request_split[2])
                    # client id is the last element
                    client_id = request_split[-1]
                    self.lobbies.join_client(lobby_id,client_id)
                    response = "accepted"
                    client_socket.send(response.encode("utf-8"))
                    
                elif re.search("^Choose character",request):
                    request_split = request.split(" ")
                    character = request_split[2]
                    lobby_id = int(request_split[4])
                    player_num = request_split[-1]
                    self.lobbies.add_character(lobby_id,character,player_num)
                    response = "character received"
                    client_socket.send(response.encode("utf-8"))
                    
                    
                    
                else:
                    response = "accepted"
                    client_socket.send(response.encode("utf-8"))
                    
            

        except Exception as e:
            print(f"Error when handling client: {e}")
            
        finally:
            client_socket.close()
            with self.lock:
                client_id = self.clients[client_socket]
                # delete the client socket from clients list
                del self.clients[client_socket]
                # delete the client id from the lobby data
                self.lobbies.delete_client_id(client_id)
                
                        
                print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
                
                
        
                

    
server = LobbyServer()
server.start()

    