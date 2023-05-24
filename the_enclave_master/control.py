import time

import mido
from pythonosc.udp_client import SimpleUDPClient

from simulation import Simulation

CONFIG_MAPPING = {
    0: 'polution',
    1: 'deforestation',
    2: 'new_trees',
}

osc_client = SimpleUDPClient("127.0.0.1", 8010)

def control_loop(sim: Simulation):
    while True:
        try:
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
        except Exception as e:
            print(e)
        print("MIDI port unavailable, sleeping and retrying")
        time.sleep(5)


def send_osc(address: str, value: float):
    osc_client.send_message(address, [value])


def transmit_scene(scene: str):
    print("Transmitting scene:", scene)
    send_osc(scene, 1.0)
