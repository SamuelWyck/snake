class Transmitter:
    def __init__(self):
        self.receivers = []

    

    def link_receiver(self, receiver):
        self.receivers.append(receiver)
    


    def open_receivers(self):
        for receiver in self.receivers:
            receiver.open()
    


    def close_receivers(self):
        for receiver in self.receivers:
            receiver.close()

    

    def toggle_receivers(self):
        for receiver in self.receivers:
            receiver.toggle()