import numpy as np
import pygame
from scipy.io.wavfile import write
import core.effects as effects

import tkinter as tk
from tkinter import filedialog

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

        self.compressor_t = 0.9
        self.compressor_r = 1
        self.compressor_mg = 1

        self.swing_amount = 0.2
        self.apply_swing = False

    def add_sound(self, position, lane):
        self.pattern[lane][position] = 1

    def remove_sound(self, position, lane):
        self.pattern[lane][position] = 0

    def generate_raw(self, sample_rate):
        exported_pattern = np.zeros(int(sample_rate * 240 / self.bpm))

        kick_array = self.kick.get_raw()
        snare_array = self.snare.get_raw()
        hat_array = self.hat.get_raw()
        open_hat_array = self.open_hat.get_raw()
        clap_array = self.clap.get_raw()

        for j in range(0, len(self.pattern[0])):
            if self.pattern[0][j]:
                start = int(j * sample_rate * 15 / self.bpm)
                if j % 2 == 1 and self.apply_swing:
                    start += int(sample_rate * self.swing_amount * 15 / self.bpm)
                for index, sample in enumerate(kick_array):
                    index_in_export = start + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break

            if self.pattern[1][j]:
                start = int(j * sample_rate * 15 / self.bpm)
                if j % 2 == 1 and self.apply_swing:
                    start += int(sample_rate * self.swing_amount * 15 / self.bpm)
                for index, sample in enumerate(snare_array):
                    index_in_export = start + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break

            if self.pattern[2][j]:
                start = int(j * sample_rate * 15 / self.bpm)
                if j % 2 == 1 and self.apply_swing:
                    start += int(sample_rate * self.swing_amount * 15 / self.bpm)
                for index, sample in enumerate(hat_array):
                    index_in_export = start + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break

            if self.pattern[3][j]:
                start = int(j * sample_rate * 15 / self.bpm)
                if j % 2 == 1 and self.apply_swing:
                    start += int(sample_rate * self.swing_amount * 15 / self.bpm)
                for index, sample in enumerate(open_hat_array):
                    index_in_export = start + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break

            if self.pattern[4][j]:
                start = int(j * sample_rate * 15 / self.bpm)
                if j % 2 == 1 and self.apply_swing:
                    start += int(sample_rate * self.swing_amount * 15 / self.bpm)
                for index, sample in enumerate(clap_array):
                    index_in_export = start + index
                    if index_in_export < len(exported_pattern):
                        exported_pattern[index_in_export] += sample
                    else:
                        break

        scaled = np.int16(exported_pattern / np.max(np.abs(exported_pattern)) * 32767)
        return scaled

    def export_pattern(self, sample_rate):
        sound = self.generate_raw(sample_rate)
        sound = effects.dynamic_compressor(sound, self.compressor_t, self.compressor_r, self.compressor_mg)
        sound = effects.normalize(sound, 32767)

        root = tk.Tk()
        root.withdraw()

        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            title="Save your sound as..."
        )

        if filename:
            write(filename, sample_rate, sound)


    def get_sound(self, sample_rate):
        sound = self.generate_raw(sample_rate)
        sound = effects.dynamic_compressor(sound, self.compressor_t, self.compressor_r, self.compressor_mg)
        sound = effects.normalize(sound, 32767)
        sound = np.repeat(sound[:, np.newaxis], 2, axis=1)
        sound = pygame.sndarray.make_sound(sound)
        return sound