from .event import OSCEvent


class OSCTransition(OSCEvent):
    """Represents the transition of an OSC message's parameter value over time.

    Attributes:
        start (float): The start value of the parameter.
        end (float): The end value of the parameter.
    """

    def __init__(self, address: str, start: float, end: float, duration: float):
        super().__init__(address, duration)
        self.start = start
        self.end = end

    def step(self, dt: float):
        """Calculates the current parameter value based on time and sends an OSC message with the current value to the specified address.

        Args:
            dt (float): The time elapsed since the last call to step.
        """
        value = ((self.time / self.duration) * (self.end - self.start) + self.start,)
        super().step(dt, value)
