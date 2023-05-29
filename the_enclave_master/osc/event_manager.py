from .event import OSCEvent


class OSCEventManager:
    """A class for managing OSC events.

    Attributes:
        __events (list[OSCEvent]): A private list of OSC events to manage.
    """

    def __init__(self):
        self.__events = list[OSCEvent]

    def add_event(self, event: OSCEvent):
        """Add an OSCEvent to the event manager."""
        self.__events.append(event)

    def step(self, dt: float):
        """Execute all events in the manager and remove completed events."""
        for event in self.__events:
            event.step(dt)
        self.__events = [e for e in self.__events if not e.done]
