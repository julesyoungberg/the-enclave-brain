from .message import send_osc_message


class OSCEvent:
    """
    A class representing an OSC event with an address and duration.

    Attributes:
    - address (str): the OSC address of the event.
    - duration (float): the duration of the event in seconds.
    - time (float): The current time.
    - done (bool): whether or not the event has finished.
    """

    def __init__(self, address: str, duration=0.0):
        self.address = address
        self.duration = duration
        self.time = 0.0
        self.done = False

    def step(self, dt: float, value: float = None):
        if value is not None:
            send_osc_message(self.address, value)
        self.time += dt
        if self.time > self.duration:
            self.done = True
