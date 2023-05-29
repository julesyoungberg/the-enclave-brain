from .event import OSCEvent


class OSCSleep(OSCEvent):
    """A class representing a sleep event that extends the OSCEvent class.

    This event does not fire any events since the value passed to the parent class is always None.
    """

    def __init__(self, duration: float):
        super().__init__("sleep", duration)

    def step(self, dt: float):
        super().step(dt, None)
