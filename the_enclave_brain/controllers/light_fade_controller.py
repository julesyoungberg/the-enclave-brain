from ..utils import scale_value

FADE_SECONDS = 6.0


class LightFadeController:
    def __init__(self, start_color, end_color):
        self.start_color = list(start_color)
        self.end_color = list(end_color)
        self.current_color = list(start_color)
        self.current_time = 0.0
        self.done = False
    
    def update(self, dt: float):
        self.current_time += dt
        progress = self.current_time / FADE_SECONDS
        for i in range(3):
            self.current_color[i] = min(
                1.0,
                max(
                    0.0,
                    progress * (self.end_color[i] - self.start_color[i]) + self.start_color[i]
                )
            )
            # self.current_color[i] = scale_value(
            #     self.current_time,
            #     0.0,
            #     FADE_SECONDS,
            #     self.start_color[i],
            #     self.end_color[i]
            # )
        if self.current_time > FADE_SECONDS:
            self.done = True

    def get_current_color(self):
        return tuple([int(x) for x in self.current_color])
