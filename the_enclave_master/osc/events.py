from .messages import send_osc_message


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

    def update(self, dt: float, value: float = None):
        if value is not None:
            send_osc_message(self.address, value)
        self.time += dt
        if self.time > self.duration:
            self.done = True


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

    def update(self):
        """Checks if all events are done and sets the done attribute of the parent class."""
        done = True
        for event in self.events:
            if not event.done:
                done = False
        self.done = done


class OSCEventSequence(OSCEventGroup):
    """A class representing a sequence of events to be processed in order.

    This class extends the OSCEventGroup class, which provides a data structure to
    hold a group of events.

    Attributes:
        events: A list of OSCEvent objects representing the events in the sequence.
    """

    def update(self, dt: float):
        """Calls the step method of the next non-completed event in the sequence,
        passing in the specified time increment."""
        for event in self.events:
            if not event.done:
                event.update(dt)
                break
        super().update()


class OSCEventStack(OSCEventGroup):
    """A class that represents a stack of OSC events to be executed in parallel.

    This class inherits from the OSCEventGroup class and defines
    a method called "step" for step-wise execution of a group of OSC
    events. The step method iterates over each event within the "events"
    attribute of the class, calling the step function of each non-done
    event with the provided dt value. Finally, the super class method
    "step" is called.

    Attributes:
        events (list): The list of OSC events to be executed.
    """

    def update(self, dt: float):
        """Executes the stack of OSC events on a
        step-wise basis with the provided time delta."""
        for event in self.events:
            if not event.done:
                event.update(dt)
        super().update()


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

    def update(self, dt: float):
        """Execute all events in the manager and remove completed events."""
        for event in self.__events:
            event.update(dt)
        self.__events = [e for e in self.__events if not e.done]


class OSCSleepEvent(OSCEvent):
    """A class representing a sleep event that extends the OSCEvent class.

    This event does not fire any events since the value passed to the parent class is always None.
    """

    def __init__(self, duration: float):
        super().__init__("sleep", duration)

    def update(self, dt: float):
        super().update(dt, None)
