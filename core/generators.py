import math
import numpy as np
import scipy.signal as signal


def triangle_wave(x):
    return 2 / math.pi * math.asin(math.sin(x))


def generate_kick(sample_rate, duration, amp, freq, high_freq, decay, attack, time, shape):
    num_samples = int(sample_rate * duration)
    kick = []

    if shape == 1:
        for i in range(num_samples):
            transient = (1 - math.exp(-attack * (i / sample_rate)))
            tail = math.exp(-decay * (i / sample_rate))
            sample = (transient * amp * math.sin(2 * math.pi * (freq + high_freq *
                                                               math.exp(-time * i / sample_rate)) * i / sample_rate)
                      * tail)
            kick.append(sample)
    elif shape == 2:
        for i in range(num_samples):
            transient = (1 - math.exp(-attack * i / sample_rate))
            tail = math.exp(-decay * i / sample_rate)
            sample = (transient * amp * triangle_wave(2 * math.pi * (freq + high_freq *
                                                                     math.exp(-time * i / sample_rate)) * i / sample_rate)
                      * tail)
            kick.append(sample)

    kick = np.array(kick)
    return kick


def generate_snare(sample_rate, duration, amp, freq, decay, attack):
    num_samples = int(sample_rate * duration)
    noise = amp * np.random.uniform(-1, 1, num_samples)

    drum = []

    for i in range(num_samples):
        noise[i] *= math.exp(-decay * i / sample_rate) * (1 - math.exp(-attack * i / sample_rate))

    noise /= 2

    for i in range(num_samples):
        tail = math.exp(-decay * i / sample_rate)
        transient = (1 - math.exp(-attack * i / sample_rate))
        sample = amp * triangle_wave(2 * freq * math.pi * i / sample_rate) * tail * transient
        drum.append(sample)

    snare = (noise + drum)

    return snare


def generate_cymbal(sample_rate, duration, amp, freq, decay, attack):
    num_samples = int(sample_rate * duration)
    cymbal = amp * np.random.uniform(-1, 1, num_samples)
    Q = 10
    w0 = freq / (0.5 * sample_rate)
    b, a = signal.iirpeak(w0, Q)
    cymbal = signal.lfilter(b, a, cymbal)

    for i in range(num_samples):
        cymbal[i] *= math.exp(-decay * i / sample_rate) * (1 - math.exp(-attack * i / sample_rate))

    return cymbal


def generate_single_clap(sample_rate, duration, amp, decay, ms):
    num_samples = int(sample_rate * duration)
    clap = amp * np.random.uniform(-1, 1, num_samples)

    silence = np.zeros(int(sample_rate * ms * 0.001))
    clap = np.concatenate((silence, clap))[0:num_samples]

    for i in range(len(silence), num_samples):
        clap[i] *= math.exp(-decay * ((i - len(silence)) / sample_rate))
    return clap

def generate_clap(sample_rate, duration, amp, decay, num_claps, delay_interval):
    num_samples = int(sample_rate * duration)

    interval = np.linspace(0, delay_interval, num_claps)
    fade = np.linspace(0.5, 1, num_claps)

    clap = np.zeros(num_samples)

    for i in range(num_claps):
        single_clap = generate_single_clap(sample_rate, duration, amp * fade[num_claps - i - 1], decay, interval[i])
        clap += single_clap

    return clap