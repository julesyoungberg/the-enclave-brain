import threading
import time

import simpy

from control import control_loop, transmit_scene
from simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0

def simulation_loop(sim: Simulation, env: simpy.Environment, tick: float):
    print("Running simulation")
    prev_scene = None
    while True:
        sim.update()
        scene = sim.get_scene()
        if scene != prev_scene:
            transmit_scene(scene)
        prev_scene = scene
        yield env.timeout(tick)
    

def main():
    sim = Simulation()
    env = simpy.Environment()

    control_thread = threading.Thread(target=control_loop, args=(sim,))
    control_thread.start()

    # @todo initialize reset timer

    env.process(simulation_loop(sim, env, TIME_STEP_SECONDS))
    env.run()


if __name__ == "__main__":
    main()
