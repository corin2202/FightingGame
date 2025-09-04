import os
import pickle

class HashTable:
    def __init__(self):
        self.table_size = 10
        
        self.cur_dir = os.getcwd()
        # stores the parent directory to the current working directory
        self.parent_dir = os.path.dirname(self.cur_dir)
        # creates a new path to the stats directory
        self.stats_folder_path = os.path.join(str(self.parent_dir),"Stats")
        self.stats_path = os.path.join(self.stats_folder_path,"stats.txt")
        
        
        # opens the stats file, loads with pickle
        try:
            with open(self.stats_path, 'rb') as stats_file:
                self.table = pickle.load(stats_file)
                
        except EOFError:
            # if file empty, populates an empty table
            self.table = [None] * self.table_size
            self.update_stat("Damage",0)
            self.update_stat("Wins",0)
            self.update_stat("Losses",0)
            self.update_stat("Deaths",0)
            self.update_stat("Kills",0)
            self.update_stat("Games Played",0)
            
            
    def get_table(self):
        return self.table
           
            

    def _hash_function(self, key):
        # adds total ascii values and mods by table size
        total = 0
        for letter in key:
            total += ord(letter)
            
        return total % self.table_size
    
    
    def _save_table(self):
        # serialises the table then stores as pickled format
        with open(self.stats_path, 'wb') as stats_file:
            pickle.dump(self.table, stats_file)
        

    def update_stat(self, stat_name, value):
        # performs key hash to find index of stat
        index = self._hash_function(stat_name)
        
        # updates a stat, if not present, creates a new one
        # if one already in its place, appends to the current one

        if self.table[index] is None:
            # if the slot is empty, create a new tuple
            self.table[index] = [(stat_name, value)]
            
        else:   
            in_table_index = False
            
            # loops through the list at the index, if there is a chain (more than one tuple)
            # will loop through the tuples until the stat is found & updates it
            # if not found, creates a new chain with new stat
            
            for i , (stat,val) in enumerate(self.table[index]):
                if stat == stat_name:
                    self.table[index][i] = (stat_name,value)
                    in_table_index = True
            
            
            if not in_table_index:
                self.table[index].append((stat_name, value))
                            
        self._save_table()
            
 
            
    def get_stat(self, stat_name):
        index = self._hash_function(stat_name)

        if self.table[index] is not None:
            for existing_stat, value in self.table[index]:
                if existing_stat == stat_name:
                    return value
                
        else:
            return "Empty"
        
        
    # adds a number to a current stat, e.g adding 1 win or 1 loss   
    def increment_stat(self,stat_name,value=1):
        current_stat_val = self.get_stat(stat_name)
        
        if current_stat_val != "Empty":
            new_stat_val = current_stat_val + value
            self.update_stat(stat_name,new_stat_val)
        

            



        
        

        




