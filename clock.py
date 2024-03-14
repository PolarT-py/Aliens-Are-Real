import settings


class Timer:
    def __init__(self, milliseconds, start=True):
        self.initial_time = milliseconds
        if start:
            self.time = self.initial_time
        else:
            self.time = 0
        self.ring = False

    def update(self, dt):
        self.time -= settings.FPS * dt
        if self.time <= 0:
            self.ring = True

    def reset(self):
        self.ring = False
        self.time = self.initial_time
