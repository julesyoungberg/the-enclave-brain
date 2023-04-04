import threading
import time

from control import control_loop, transmit_scene
from simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0

def simulation_loop(sim: Simulation):
    print("Running simulation")
    sim_elapsed = 0
    prev_scene = None
    while True:
        step_start = time.time()
        sim.update()
        scene = sim.get_scene()
        if scene != prev_scene:
            transmit_scene(scene)
        step_end = time.time()
        step_elapsed = step_end - step_start
        step_remaining = TIME_STEP_SECONDS - step_elapsed
        time.sleep(step_remaining)
        sim_elapsed += TIME_STEP_SECONDS
        prev_scene = scene


def main():
    sim = Simulation()

    control_thread = threading.Thread(target=control_loop, args=(sim,))
    control_thread.start()

    # @todo initialize reset timer

    simulation_loop(sim)


if __name__ == "__main__":
    main()
