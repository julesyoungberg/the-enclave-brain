import time

import mido

from .simulation import Simulation

CONFIG_MAPPING = {
    0: "polution",
    1: "deforestation",
    2: "new_trees",
}


def control_loop(sim: Simulation):
    """
    This function runs an infinite control loop that listens for MIDI input and updates the simulation accordingly.
    The input parameter is a simulation object (sim).
    The loop continuously listens on the MIDI port.
    It parses the MIDI messages, updates the simulation config if a valid mapping is found, and ignores unknown channels.
    If the MIDI port becomes unavailable, the loop sleeps before retrying.
    """
    return None
    # while True:
    #     try:
    #         with mido.open_input() as inport:
    #             print("Listening on MIDI port", inport)
    #             for msg in inport:
    #                 print("Received MIDI message", msg)
    #                 key = msg.channel
    #                 value = msg.value
    #                 if key not in CONFIG_MAPPING:
    #                     print("Unknown channel:", key)
    #                     continue
    #                 sim.update_config(CONFIG_MAPPING[key], float(value) / 255.0)
    #     except Exception as e:
    #         print(e)
    #     print("MIDI port unavailable, sleeping and retrying")
    #     time.sleep(5)
