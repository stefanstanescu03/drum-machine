import numpy as np
import time
import pygame
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


class Sequencer:
    def __init__(self, bpm, hat, kick, snare, open_hat, clap):
        self.bpm = bpm
        self.pattern = np.zeros((5, 16))
        self.hat = hat
        self.kick = kick
        self.snare = snare
        self.open_hat = open_hat
        self.clap = clap

        self.kick_channel = pygame.mixer.Channel(0)
        self.snare_channel = pygame.mixer.Channel(1)
        self.hat_channel = pygame.mixer.Channel(2)
        self.open_hat_channel = pygame.mixer.Channel(3)
        self.clap_channel = pygame.mixer.Channel(4)

    def add_sound(self, position, lane):
        self.pattern[lane][position] = 1

    def remove_sound(self, position, lane):
        self.pattern[lane][position] = 0

    def play(self):

        step_time = 15.0 / self.bpm
        last_time = pygame.time.get_ticks()

        for j in range(0, len(self.pattern[0])):
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - last_time) / 1000.0

            if elapsed_time < step_time:
                pygame.time.delay(int((step_time - elapsed_time) * 1000))

            last_time = pygame.time.get_ticks()

            if self.pattern[0][j]:
                self.kick_channel.play(self.kick.get_sound(), fade_ms=0)
            if self.pattern[1][j]:
                self.snare_channel.play(self.snare.get_sound(), fade_ms=0)
            if self.pattern[2][j]:
                self.hat_channel.play(self.hat.get_sound(), fade_ms=0)
            if self.pattern[3][j]:
                self.open_hat_channel.play(self.open_hat.get_sound(), fade_ms=0)
            if self.pattern[4][j]:
                self.clap_channel.play(self.clap.get_sound(), fade_ms=0)

    def export_pattern(self, filename, sample_rate):
        exported_pattern = np.zeros(int(sample_rate * 240 / self.bpm))

        kick_array = self.kick.get_raw()
        snare_array = self.snare.get_raw()
        hat_array = self.hat.get_raw()
        open_hat_array = self.open_hat.get_raw()
        clap_array = self.clap.get_raw()

        for j in range(0, len(self.pattern[0])):
            if self.pattern[0][j]:
                for index, sample in enumerate(kick_array):
                    index_in_export = int(j * sample_rate * 15 / self.bpm) + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break
                    # exported_pattern[min(int(j * sample_rate * 15 / self.bpm) + index,
                    #                      len(exported_pattern) - 1)] += sample
            if self.pattern[1][j]:
                for index, sample in enumerate(snare_array):
                    index_in_export = int(j * sample_rate * 15 / self.bpm) + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break
                    # exported_pattern[min(int(j * sample_rate * 15 / self.bpm) + index,
                    #                      len(exported_pattern) - 1)] += sample
            if self.pattern[2][j]:
                for index, sample in enumerate(hat_array):
                    index_in_export = int(j * sample_rate * 15 / self.bpm) + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break
                    # exported_pattern[min(int(j * sample_rate * 15 / self.bpm) + index,
                    #                      len(exported_pattern) - 1)] += sample
            if self.pattern[3][j]:
                for index, sample in enumerate(open_hat_array):
                    index_in_export = int(j * sample_rate * 15 / self.bpm) + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break
                    # exported_pattern[min(int(j * sample_rate * 15 / self.bpm) + index,
                    #                      len(exported_pattern) - 1)] += sample
            if self.pattern[4][j]:
                for index, sample in enumerate(clap_array):
                    index_in_export = int(j * sample_rate * 15 / self.bpm) + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break
                    # exported_pattern[min(int(j * sample_rate * 15 / self.bpm) + index,
                    #                      len(exported_pattern) - 1)] += sample

        scaled = np.int16(exported_pattern / np.max(np.abs(exported_pattern)) * 32767)
        # t = np.linspace(0, len(scaled), len(scaled))
        # plt.plot(t, scaled)
        # plt.show()
        write(filename, sample_rate, scaled)
