from ..osc.addresses import lights_control_address
from ..osc.events import OSCEventManager, OSCEventStack, OSCEventSequence, OSCSleepEvent
from ..osc.transitions import OSCFlicker
from ..simulation import Simulation

class LightFlickerController:
    """
    A class representing a light flicker controller that manages light flicker events triggered 
    by varying simulation parameters.
    
    Args:
        event_manager (OSCEventManager): The OSCEventManager object where events will be added.
        simulation (Simulation): The Simulation object where parameters will be monitored.

    Attributes:
        event_manager (OSCEventManager): The OSCEventManager object where events will be added.
        sim (Simulation): The Simulation object where parameters will be monitored.
        current_event (OSCEventStack, None): The currently executing event stack, or None if no event is executing.
    """

    def __init__(self, event_manager: OSCEventManager, simulation: Simulation):
        self.event_manager = event_manager
        self.sim = simulation
        self.current_event = None
        self.max_frequency = 30.0
        self.current_time = 0.0

    def flicker_side_tubes(self, n_flicks=1):
        return [
            OSCFlicker(
                address=lights_control_address("tubes1_brightness"),
                n_flicks=n_flicks,
            ),
            OSCFlicker(
                address=lights_control_address("tubes3_brightness"),
                n_flicks=n_flicks,
            ),
        ]

    def update(self, dt: float):
        self.current_time += dt

        if self.current_event is not None and (not self.current_event.done or self.current_time < self.max_frequency):
            return
        
        self.current_time = 0.0
        events = []

        if self.sim.param("climate_change").has_changed():
            print("climate change flicker")
            events = [
                *self.flicker_side_tubes(),
                OSCEventSequence([
                    OSCSleepEvent(0.5),
                    OSCEventStack([
                        OSCFlicker(
                            address=lights_control_address("tubes2_brightness"),
                            n_flicks=1,
                        ),
                        OSCFlicker(
                            address=lights_control_address("lanterns1_brightness"),
                            n_flicks=1,
                        ),
                        OSCFlicker(
                            address=lights_control_address("lanterns2_brightness"),
                            n_flicks=1,
                        )
                    ])
                ]),
            ]
        elif self.sim.param("human_activity").has_changed():
            print("human activity flicker")
            events = [
                *self.flicker_side_tubes(n_flicks=2),
                OSCEventSequence([
                    OSCSleepEvent(0.5),
                    OSCFlicker(
                        address=lights_control_address("tubes2_brightness"),
                        n_flicks=2,
                    ),
                ]),
                OSCFlicker(
                    address=lights_control_address("lanterns1_brightness"),
                    n_flicks=2,
                    period=2.0
                ),
                OSCEventSequence([
                    OSCSleepEvent(1.0),
                    OSCFlicker(
                        address=lights_control_address("lanterns2_brightness"),
                        n_flicks=2,
                        period=2.0
                    ),
                ]),
            ]
        elif self.sim.param("fate").has_changed():
            print("fate flicker")
            events = [
                *self.flicker_side_tubes(n_flicks=3),
                OSCEventSequence([
                    OSCSleepEvent(0.5),
                    OSCFlicker(
                        address=lights_control_address("tubes2_brightness"),
                        n_flicks=3,
                    ),
                ]),
                OSCFlicker(
                    address=lights_control_address("lanterns1_brightness"),
                    n_flicks=3,
                ),
                OSCEventSequence([
                    OSCSleepEvent(0.5),
                    OSCFlicker(
                        address=lights_control_address("lanterns2_brightness"),
                        n_flicks=3,
                    ),
                ]),
            ]
        else:
            self.current_time = self.max_frequency

        if len(events) > 0:
            self.current_event = OSCEventStack(events)
            self.event_manager.add_event(self.current_event)
