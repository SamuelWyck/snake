import csv
# controls is a dict of the control names and key codes for each game control

# example of expected shape of controls param
# player_controls = {
#     "UP": pygame.K_w,
#     "DOWN": pygame.K_s,
#     "RIGHT": pygame.K_d,
#     "LEFT": pygame.K_a
# }

# holdable_inputs is a set of the control names of the inputs
# that the player is allowed to hold down to allow for repeated inputs 

# example of expected shape of holdable_inputs param
# set([
#     "UP",
#     "DOWN"
# ])

# save_file_path is the absolute path to the save file that the controller will use to save keybinds

class PlayerController:
    def __init__(self, controls, holdable_inputs=set(), save_file_path=None):
        self.save_file_path = save_file_path
        loaded_controls = self.load_saved_keybinds()
        if loaded_controls != None:
            controls = loaded_controls

        self.update_controls(controls, save_controls=False)

        self.inputs_pressed = {}
        for control_name in self.controls:
            self.inputs_pressed[control_name] = False

        self.holdable_inputs = holdable_inputs

        self.inputs_to_reset = []

    

    # a method to load saved keybinds 
    def load_saved_keybinds(self):
        if self.save_file_path is None:
            return None

        try:
            controls = {}

            with open(self.save_file_path, "r") as file:
                keybinds = csv.DictReader(file)
                for row in keybinds:
                    for key in row:
                        controls[key] = int(row[key])
                    
            return controls
        except FileNotFoundError:
            return None
        

    
    # this method saves the keybinds to a file if one was given
    def save_keybinds(self):
        if self.save_file_path == None:
            return
        
        try:
            fieldnames = [key for key in self.controls]
            with open(self.save_file_path, "w") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(self.controls)
        except:
            pass



    # this method is hooked up to the event loop and expects a key_code from the KEYDOWN event
    def key_down(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)



    # this method is hooked up to the event loop and expects a key_code from the KEYUP event
    # this method is only needed if there are controls the player is allowed to hold down
    def key_up(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = False

    

    # this method is hooked up to the event loop and expects a mouse_btn code from the MOUSEBUTTONDOWN event
    def mouse_down(self, mouse_btn):
        if mouse_btn in self.key_codes:
            control_name = self.key_codes[mouse_btn]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)
    


    # this method is hooked up to the event loop and expects a mouse_btn code from the MOUSEBUTTONUP event
    # this method is only needed if there are controls the player is allowed to hold down
    def mouse_up(self, mouse_btn):
        if mouse_btn in self.key_codes:
            control_name = self.key_codes[mouse_btn]
            self.inputs_pressed[control_name] = False

        
    
    # this method must be called at the end of the game loop
    def reset_inputs(self):
        for control_name in self.inputs_to_reset:
            self.inputs_pressed[control_name] = False
        self.inputs_to_reset = []
    


    # this method is the api for the player object to get the currently active controls
    def get_inputs(self):
        return self.inputs_pressed
    


    # this method expects a dict like the constructor does 
    # it is used for updating the controls
    def update_controls(self, new_controls, save_controls=True):
        self.controls = dict(new_controls)

        self.key_codes = {}
        for control_name in self.controls:
            key_code = self.controls[control_name]
            self.key_codes[key_code] = control_name
        
        if save_controls:
            self.save_keybinds()