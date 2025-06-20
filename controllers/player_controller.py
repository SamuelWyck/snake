import pygame



class Player_Controller:
    def __init__(self, controls, holdable_inputs=set()):
        self.update_controls(controls)

        self.inputs_pressed = {}
        for control_name in controls:
            self.inputs_pressed[control_name] = False

        self.holdable_inputs = holdable_inputs

        self.inputs_to_reset = []



    def key_down(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)


    
    def key_up(self, key):
        if key in self.key_codes:
            control_name = self.key_codes[key]
            self.inputs_pressed[control_name] = False

    

    def mouse_down(self, mouse_btn):
        if mouse_btn in self.key_codes:
            control_name = self.key_codes[mouse_btn]
            self.inputs_pressed[control_name] = True

            if control_name not in self.holdable_inputs:
                self.inputs_to_reset.append(control_name)
    


    def mouse_up(self, mouse_btn):
        if mouse_btn in self.key_codes:
            control_name = self.key_codes[mouse_btn]
            self.inputs_pressed[control_name] = False

        
    
    def reset_inputs(self):
        for control_name in self.inputs_to_reset:
            self.inputs_pressed[control_name] = False
        self.inputs_to_reset = []
    


    def get_inputs(self):
        return self.inputs_pressed
    


    def update_controls(self, new_controls):
        self.controls = new_controls

        self.key_codes = {}
        for control_name in self.controls:
            key_code = self.controls[control_name]
            self.key_codes[key_code] = control_name