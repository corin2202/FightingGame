class MenuStack:
    def __init__(self):
        self.menu_stack_list = []
        
    def peek(self):
        return self.menu_stack_list[-1]
    
    def push(self,menu_object):
        self.menu_stack_list.append(menu_object)
        
    def pop_off(self,x_times = 1):
        if len(self.menu_stack_list) > 1:
            for x in range(x_times):
                self.menu_stack_list.pop()
        else:
            print("At main menu, please press the quit button")