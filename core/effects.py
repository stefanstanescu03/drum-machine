import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math

def clip(sound, max_volume):
    clipped_sound = []
    sound = sound / max_volume
    for sample in sound:
        if sample >= 1:
            clipped_sound.append(2 / 3)
        if sample <= -1:
            clipped_sound.append(-2 / 3)
        if -1 < sample < 1:
            clipped_sound.append(sample - sample**3  / 3)
    clipped_sound = np.array(clipped_sound)
    clipped_sound = (max_volume * clipped_sound).astype(np.int16)
    return clipped_sound

def hard_clip(sound, head_room):
    clipped_sound = []
    for sample in sound:
        if sample >= head_room:
            clipped_sound.append(head_room)
        if sample <= -head_room:
            clipped_sound.append(-head_room)
        if -head_room < sample < head_room:
            clipped_sound.append(sample)
    clipped_sound = np.array(clipped_sound)
    return clipped_sound


def echo(sound, sample_rate, g, delay):
    sound = sound / 32768.0
    final_sound = np.zeros(len(sound))

    d = int(delay * sample_rate)

    for n in range(0, len(sound)):
        if n > d:
            final_sound[n] = sound[n] + g * final_sound[n - d]
        else:
            final_sound[n] = sound[n]

    final_sound = np.clip(final_sound, -1.0, 1.0)
    final_sound = (final_sound * 32768).astype(np.int16)

    return final_sound


def dynamic_compressor(sound, threshold, ratio, makeup_gain):
    sound = sound / 32768.0
    final_sound = np.zeros(len(sound))

    for n in range(0, len(sound)):
        if sound[n] > threshold:
            final_sound[n] = (sound[n] - threshold) / ratio + threshold
        elif sound[n] < -threshold:
            final_sound[n] = (sound[n] + threshold) / ratio - threshold
        else:
            final_sound[n] = sound[n]

    final_sound *= makeup_gain
    final_sound *= 32768.0
    final_sound = clip(final_sound, 32768)
    return final_sound


def normalize(sound, max_volume):
    return np.int16(sound / np.max(np.abs(sound)) * max_volume)


def low_pass_filter(sound, freq, sample_rate):
    normal_cutoff = freq / (sample_rate * 0.5)
    b, a = signal.butter(2, normal_cutoff, 'low')
    sound = signal.filtfilt(b, a, sound)
    sound = np.clip(sound, -32767, 32767)
    return sound