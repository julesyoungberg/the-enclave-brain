from .event_group import OSCEventGroup


class EventStack(OSCEventGroup):
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

    def step(self, dt: float):
        """Executes the stack of OSC events on a
        step-wise basis with the provided time delta."""
        for event in self.events:
            if not event.done:
                event.step(dt)
        super().step()
