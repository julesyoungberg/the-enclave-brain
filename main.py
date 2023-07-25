from datetime import datetime

import simpy

from the_enclave_brain.app import App
from the_enclave_brain.config import TIME_STEP_SECONDS


def simulation_loop(app: App, env: simpy.Environment, tick: float):
    while True:
        app.update(tick)
        yield env.timeout(tick)


if __name__ == "__main__":
    app = App()
    env = simpy.rt.RealtimeEnvironment(strict=False)
    proc = env.process(simulation_loop(app, env, TIME_STEP_SECONDS))
    env.run(until=proc)
