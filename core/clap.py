import core.generators as generators
import numpy as np
import pygame


class Clap:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.amp = 0.2
        self.master_amp = 1
        self.decay = 20
        self.num_claps = 3
        self.delay_interval = 50

    def get_raw(self):
        max_volume = 32767

        inst = generators.generate_clap(self.sample_rate,
                                        self.duration,
                                        self.amp * self.master_amp * max_volume,
                                        self.decay,
                                        self.num_claps,
                                        self.delay_interval).astype(np.int16)
        return inst

    def get_sound(self):
        max_volume = 32767

        inst = generators.generate_clap(self.sample_rate,
                                        self.duration,
                                        self.amp * self.master_amp * max_volume,
                                        self.decay,
                                        self.num_claps,
                                        self.delay_interval).astype(np.int16)
        inst = np.repeat(inst.reshape(self.sample_rate, 1), 2, axis=1)
        inst = pygame.sndarray.make_sound(inst)

        return inst
