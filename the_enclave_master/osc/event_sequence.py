from .event_group import OSCEventGroup


class EventSequence(OSCEventGroup):
    """A class representing a sequence of events to be processed in order.

    This class extends the OSCEventGroup class, which provides a data structure to
    hold a group of events.

    Attributes:
        events: A list of OSCEvent objects representing the events in the sequence.
    """

    def step(self, dt: float):
        """Calls the step method of the next non-completed event in the sequence,
        passing in the specified time increment."""
        for event in self.events:
            if not event.done:
                event.step(dt)
                break
        super().step()
