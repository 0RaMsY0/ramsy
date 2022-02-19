"""
    The payload maker
"""

class MakeCameraStreamingPayload(object):
    def __init__(self, __host__, __socket_port__, __camera_streaming_port__, __name__, __injection__):
        self.host = __host__
        self.socket_port = __socket_port__
        self.camera_streaming_port = __camera_streaming_port__
        self.name = __name__
        self.injection = __injection__
    def WriteToFile(self):
        with open(f"{self.name}.sh", "w") as THE_DES:
            pass