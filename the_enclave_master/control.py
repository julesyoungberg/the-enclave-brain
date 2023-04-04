import time

import mido
from pythonosc.udp_client import SimpleUDPClient

from simulation import Simulation

CONFIG_MAPPING = {
    0: 'polution',
    1: 'deforestation',
    2: 'new_trees',
}

osc_client = SimpleUDPClient("127.0.0.1", 1337)

def control_loop(sim: Simulation):
    while True:
        with mido.open_input() as inport:
            print("Listening on MIDI port", inport)
            for msg in inport:
                print("Received MIDI message", msg)
                key = msg.channel
                value = msg.value
                if key not in CONFIG_MAPPING:
                    print("Unknown channel:", key)
                    continue
                sim.update_config(CONFIG_MAPPING[key], float(value) / 255.0)
        print("MIDI port unavailable, sleeping and retrying")
        time.sleep(5)


def transmit_scene(scene: int):
    print("Transmitting scene:", scene)
    osc_client.send_message("/scene", [scene])
