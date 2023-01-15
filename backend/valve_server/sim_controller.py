from controller import Controller
import socketio

class SimulationController(Controller):
    def __init__(self, count=10):
        super().__init__(count)

    def init_socket(self, sio):
        self.sio = sio
    
    def activate(self, index):
        self.sio.emit("simulated_pour", {"status": True})
    
    def deactivate(self, index):
        self.sio.emit("simulated_pour", {"status": False})
    
    def cleanup(self):
        pass