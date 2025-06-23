import pygame



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
# set(
#     "UP",
#     "DOWN"
# )

class PlayerController:
    def __init__(self, controls, holdable_inputs=set()):
        self.update_controls(controls)

        self.inputs_pressed = {}
        for control_name in controls:
            self.inputs_pressed[control_name] = False

        self.holdable_inputs = holdable_inputs

        self.inputs_to_reset = []



    # this method is hooked up to the event loop and expects a key_code
    def key_down(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)



    # this method is hooked up to the event loop and expects a key_code
    # this method is only needed if there are controls the player is allowed to hold down
    def key_up(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = False

    

    # this method is hooked up to the event loop and expects a mouse btn code
    def mouse_down(self, mouse_btn):
        if mouse_btn in self.key_codes:
            control_name = self.key_codes[mouse_btn]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)
    


    # this method is hooked up to the event loop and expects a mouse btn code
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
    def update_controls(self, new_controls):
        self.controls = new_controls

        self.key_codes = {}
        for control_name in self.controls:
            key_code = self.controls[control_name]
            self.key_codes[key_code] = control_name