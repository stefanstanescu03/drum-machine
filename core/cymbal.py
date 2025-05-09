import core.generators as generators
import core.effects as effects
import numpy as np
import pygame


class Cymbal:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.amp = 1
        self.freq = 5000
        self.decay = 20
        self.attack = 50

        self.apply_echo = False
        self.g = 0.5
        self.d = 0.5

    def get_raw(self):
        max_volume = 32767
        inst = generators.generate_cymbal(self.sample_rate,
                                          self.duration,
                                          self.amp * max_volume,
                                          self.freq,
                                          self.decay,
                                          self.attack)
        inst = effects.clip(inst, max_volume).astype(np.int16)
        if self.apply_echo:
            inst = effects.echo(inst, self.sample_rate, self.g, self.d)
        inst.astype(np.int16)
        return inst


    def get_sound(self):
        max_volume = 32767
        inst = generators.generate_cymbal(self.sample_rate,
                                          self.duration,
                                          self.amp * max_volume,
                                          self.freq,
                                          self.decay,
                                          self.attack)
        inst = effects.clip(inst, max_volume).astype(np.int16)
        if self.apply_echo:
            inst = effects.echo(inst, self.sample_rate, self.g, self.d)
        inst.astype(np.int16)
        inst = np.repeat(inst.reshape(self.sample_rate, 1), 2, axis=1)
        inst = pygame.sndarray.make_sound(inst)

        return inst