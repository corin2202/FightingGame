class Lobby:
    def __init__(self):
        self.lobby_data = {}
        self.next_lobby_id = 1
        
        
    def create_lobby(self,host_player_id):
        # sets lobby id to current number
        lobby_id = self.next_lobby_id
        # increments for the next lobby created
        self.next_lobby_id += 1
        # creates a new dict entry with lobby info
        self.lobby_data[lobby_id] = {"players":[host_player_id]}
        
    def max_lobbies_reached(self):
        max_lobbies = 6
        lobby_data = self.get_lobby_data()
        if len(lobby_data) < max_lobbies:
            return False
        else:
            return True
        
    def add_character(self,lobby_id,character,player_num):
        self.lobby_data[lobby_id][f"player {player_num}"] = character
        
   
    def join_client(self,lobby_id,client_id):
        self.lobby_data[lobby_id]["players"].append(client_id)
        
        
    def get_lobby_data(self):
        return self.lobby_data
    
    
    def set_lobby_data(self,lobby_data):
        self.lobby_data = lobby_data
        
        
    def delete_client_id(self, client_id):
        # loops through the lobby num and lobby info
        for key,value in list(self.lobby_data.items()):
            # loops through the players and client ids
            for key_2, value_2 in list(value.items()):
                # if client id found in the value list of "players"
                if key_2 == "players" and client_id in value_2:
                    # remove it and if value is empty after removal, delete the key with the empty list
                    value_2.remove(client_id)
                    if len(value_2) == 0:
                        del value[key_2]
                        
                if key_2 == "player 1" or key_2 == "player 2":
                    del value[key_2]
                        
            # if the lobby is empty then delete that lobby number
            if len(value) == 0:
                del self.lobby_data[key]
            
        
    
                
            
    
    
