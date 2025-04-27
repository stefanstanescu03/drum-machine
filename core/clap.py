import core.generators as generators
import numpy as np
import pygame
import core.effects as effects


class Clap:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.amp = 0.2
        self.master_amp = 1
        self.decay = 20
        self.num_claps = 3
        self.delay_interval = 50

        self.cutoff = 20000

        self.apply_echo = False
        self.g = 0.5
        self.d = 0.5

    def get_raw(self):
        max_volume = 32767

        inst = generators.generate_clap(self.sample_rate,
                                        self.duration,
                                        self.amp * self.master_amp * max_volume,
                                        self.decay,
                                        self.num_claps,
                                        self.delay_interval).astype(np.int16)
        inst = effects.hard_clip(inst, max_volume)
        inst = effects.low_pass_filter(inst, self.cutoff, self.sample_rate)
        if self.apply_echo:
            inst = effects.echo(inst, self.sample_rate, self.g, self.d)
        inst = inst.astype(np.int16)
        return inst

    def get_sound(self):
        max_volume = 32767

        inst = generators.generate_clap(self.sample_rate,
                                        self.duration,
                                        self.amp * self.master_amp * max_volume,
                                        self.decay,
                                        self.num_claps,
                                        self.delay_interval).astype(np.int16)
        inst = effects.hard_clip(inst, max_volume)
        inst = effects.low_pass_filter(inst, self.cutoff, self.sample_rate)
        if self.apply_echo:
            inst = effects.echo(inst, self.sample_rate, self.g, self.d)
        inst = inst.astype(np.int16)
        inst = np.repeat(inst.reshape(self.sample_rate, 1), 2, axis=1)
        inst = pygame.sndarray.make_sound(inst)

        return inst
