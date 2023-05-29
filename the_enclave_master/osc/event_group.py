from .event import OSCEvent


class OSCEventGroup(OSCEvent):
    """A class defining a group of OSC events to be executed together.

    Inherits from the OSCEvent class and overrides the step method. Takes in a list
    of OSCEvent objects and assigns them to an instance variable named 'events'. The
    step method sets the 'done' flag to True only if all the events in the 'events'
    list have been 'done'. Otherwise, it sets the 'done' flag to False.

    Attributes:
        events (list[OSCEvent]): A list of OSCEvent objects to be executed.
    """

    def __init__(self, events: list[OSCEvent]):
        self.events = events
        # the address here is a dummy value
        # no osc messages are sent to the address since the step method is overriden
        super().__init__("event_group")

    def step(self):
        """Checks if all events are done and sets the done attribute of the parent class."""
        done = True
        for event in self.events:
            if not event.done:
                done = False
        self.done = done
