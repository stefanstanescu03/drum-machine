import core.generators as generators
import numpy as np
import pygame
import core.effects as efx


class Snare:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.amp = 1
        self.freq = 100
        self.decay = 30
        self.attack = 50

    def get_raw(self):
        max_volume = 32767

        inst = generators.generate_snare(self.sample_rate,
                                         self.duration,
                                         self.amp * max_volume,
                                         self.freq,
                                         self.decay,
                                         self.attack).astype(np.int16)
        return inst

    def get_sound(self):
        max_volume = 32767

        inst = generators.generate_snare(self.sample_rate,
                                         self.duration,
                                         self.amp * max_volume,
                                         self.freq,
                                         self.decay,
                                         self.attack).astype(np.int16)
        inst = np.repeat(inst.reshape(self.sample_rate, 1), 2, axis=1)
        inst = pygame.sndarray.make_sound(inst)

        return inst
