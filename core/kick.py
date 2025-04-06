import core.generators as generators
import numpy as np
import pygame


class Kick:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.amp = 1
        self.freq = 40
        self.high_freq = 100
        self.decay = 10
        self.attack = 50
        self.time = 20
        self.shape = 2

    def get_raw(self):
        max_volume = 32767
        inst = generators.generate_kick(self.sample_rate,
                                        self.duration,
                                        self.amp * max_volume,
                                        self.freq,
                                        self.high_freq,
                                        self.decay,
                                        self.attack,
                                        self.time,
                                        self.shape).astype(np.int16)
        return inst

    def get_sound(self):
        max_volume = 32767
        inst = generators.generate_kick(self.sample_rate,
                                        self.duration,
                                        self.amp * max_volume,
                                        self.freq,
                                        self.high_freq,
                                        self.decay,
                                        self.attack,
                                        self.time,
                                        self.shape).astype(np.int16)
        inst = np.repeat(inst.reshape(self.sample_rate, 1), 2, axis=1)
        inst = pygame.sndarray.make_sound(inst)

        return inst
