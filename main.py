import pygame

import widgets.button
import widgets.digital_display
import widgets.dial
import widgets.sound_display
import widgets.line_delimiter
import widgets.numbers_strip
import widgets.action_button
import widgets.shape_button
import core.kick
import core.snare
import core.cymbal
import core.clap
from sequencer import Sequencer


def change_buttons_status(selected_sound, seq, buttons):
    for i in range(len(buttons)):
        if not ((buttons[i].status is True and seq.pattern[selected_sound][i] == 1) or
                (buttons[i].status is False and seq.pattern[selected_sound][i] == 0)):
            buttons[i].change_status()


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 8, 1024)
    pygame.mixer.init()

    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((1300, 600))
    pygame.display.set_caption("Drum Machine")

    background_color = (241, 239, 236)

    buttons = []
    padding = 70
    curr = 25
    for i in range(0, 16):
        button = widgets.button.Button(curr + padding, 500, 50, 50, i)
        buttons.append(button)
        curr += padding

    bpm = 155

    tempo_display = widgets.digital_display.DigitalDisplay(95, 400, 120, 50, str(bpm))
    bpm_dial = widgets.dial.Dial(260, 425, 30, 0.5, 20, "Tempo", 15)

    kick = core.kick.Kick(44100, 1)
    kick.amp = 1
    kick_attack_knob = widgets.dial.Dial(115, 120, 20, 0.1, 10, "Attack", 10)
    kick_attack_knob.init_angle(kick.attack)
    kick_decay_knob = widgets.dial.Dial(170, 120, 20, 0.1, 10, "Decay", 10)
    kick_decay_knob.init_angle(kick.decay)
    kick_time_knob = widgets.dial.Dial(115, 180, 20, 0.04, 5, "Time", 10)
    kick_time_knob.init_angle(kick.time)
    kick_freq_knob = widgets.dial.Dial(170, 180, 20, 0.2, 30, "Tone", 10)
    kick_freq_knob.init_angle(kick.freq)
    kick_level_knob = widgets.dial.Dial(115, 240, 20, 0.02, 0.5, "Level", 10)
    kick_level_knob.init_angle(kick.amp)
    kick_cutoff_knob = widgets.dial.Dial(170, 240, 20, 55.5, 20, "Cutoff", 10)
    kick_cutoff_knob.init_angle(kick.cutoff)
    kick_shape_button = widgets.shape_button.ShapeButton(210, 110, 20, 20, "Shape")
    kick_display = widgets.sound_display.SoundDisplay(kick, "Bass Drum", 95, 50, 150, 30)

    snare = core.snare.Snare(44100, 1)
    snare_attack_knob = widgets.dial.Dial(320, 120, 20, 0.1, 10, "Attack", 10)
    snare_attack_knob.init_angle(snare.attack)
    snare_decay_knob = widgets.dial.Dial(375, 120, 20, 0.1, 10, "Decay", 10)
    snare_decay_knob.init_angle(snare.decay)
    snare_freq_knob = widgets.dial.Dial(320, 180, 20, 0.3, 80, "Tone", 10)
    snare_freq_knob.init_angle(snare.freq)
    snare_level_knob = widgets.dial.Dial(375, 180, 20, 0.02, 0.5, "Level", 10)
    snare_level_knob.init_angle(snare.amp)
    snare_cutoff_knob = widgets.dial.Dial(430, 120, 20, 55.5, 20, "Cutoff", 10)
    snare_cutoff_knob.init_angle(snare.cutoff)
    snare_echo_delay_knob = widgets.dial.Dial(320, 240, 20, 0.001, 0.001, "Echo", 10)
    snare_echo_delay_knob.init_angle(snare.d)
    snare_echo_feedback_knob = widgets.dial.Dial(375, 240, 20, 0.002, 0.01, "Feedback", 10)
    snare_echo_feedback_knob.init_angle(snare.g)
    snare_echo_button = widgets.shape_button.ShapeButton(430, 229, 20, 20, "Echo")
    snare_display = widgets.sound_display.SoundDisplay(snare, "Snare Drum", 300, 50, 150, 30)

    hh = core.cymbal.Cymbal(44100, 1)
    hh_attack_knob = widgets.dial.Dial(525, 120, 20, 0.1, 10, "Attack", 10)
    hh_attack_knob.init_angle(hh.attack)
    hh_decay_knob = widgets.dial.Dial(580, 120, 20, 0.04, 15, "Decay", 10)
    hh_decay_knob.init_angle(hh.decay)
    hh_freq_knob = widgets.dial.Dial(525, 180, 20, 11, 2000, "Tone", 10)
    hh_freq_knob.init_angle(hh.freq)
    hh_level_knob = widgets.dial.Dial(580, 180, 20, 0.02, 0.5, "Level", 10)
    hh_level_knob.init_angle(hh.amp)
    hh_echo_delay_knob = widgets.dial.Dial(525, 240, 20, 0.001, 0.001, "Echo", 10)
    hh_echo_delay_knob.init_angle(snare.d)
    hh_echo_feedback_knob = widgets.dial.Dial(580, 240, 20, 0.002, 0.01, "Feedback", 10)
    hh_echo_feedback_knob.init_angle(snare.g)
    hh_echo_button = widgets.shape_button.ShapeButton(635, 229, 20, 20, "Echo")
    hh_display = widgets.sound_display.SoundDisplay(hh, "Hi Hat", 505, 50, 150, 30)

    cymbal = core.cymbal.Cymbal(44100, 1)
    cymbal.decay = 10
    cymbal.attack = 30
    cymbal_attack_knob = widgets.dial.Dial(730, 120, 20, 0.1, 10, "Attack", 10)
    cymbal_attack_knob.init_angle(cymbal.attack)
    cymbal_decay_knob = widgets.dial.Dial(785, 120, 20, 0.04, 5, "Decay", 10)
    cymbal_decay_knob.init_angle(cymbal.decay)
    cymbal_freq_knob = widgets.dial.Dial(730, 180, 20, 11, 2000, "Tone", 10)
    cymbal_freq_knob.init_angle(cymbal.freq)
    cymbal_level_knob = widgets.dial.Dial(785, 180, 20, 0.02, 0.5, "Level", 10)
    cymbal_level_knob.init_angle(cymbal.amp)
    cymbal_echo_delay_knob = widgets.dial.Dial(730, 240, 20, 0.001, 0.001, "Echo", 10)
    cymbal_echo_delay_knob.init_angle(snare.d)
    cymbal_echo_feedback_knob = widgets.dial.Dial(785, 240, 20, 0.002, 0.01, "Feedback", 10)
    cymbal_echo_feedback_knob.init_angle(snare.g)
    cymbal_echo_button = widgets.shape_button.ShapeButton(840, 229, 20, 20, "Echo")
    cymbal_display = widgets.sound_display.SoundDisplay(cymbal, "Cymbal", 710, 50, 150, 30)

    clap = core.clap.Clap(44100, 1)
    clap_decay_knob = widgets.dial.Dial(935, 120, 20, 0.1, 10, "Decay", 10)
    clap_decay_knob.init_angle(clap.decay)
    clap_delay_knob = widgets.dial.Dial(990, 120, 20, 0.12, 5, "Delay", 10)
    clap_delay_knob.init_angle(clap.delay_interval)
    clap_level_knob = widgets.dial.Dial(935, 180, 20, 0.005, 0.1, "Level", 10)
    clap_level_knob.init_angle(clap.amp)
    clap_echo_delay_knob = widgets.dial.Dial(935, 240, 20, 0.001, 0.001, "Echo", 10)
    clap_echo_delay_knob.init_angle(snare.d)
    clap_echo_feedback_knob = widgets.dial.Dial(990, 240, 20, 0.002, 0.01, "Feedback", 10)
    clap_echo_feedback_knob.init_angle(snare.g)
    clap_echo_button = widgets.shape_button.ShapeButton(1054, 229, 20, 20, "Echo")
    clap_cutoff_knob = widgets.dial.Dial(1045, 120, 20, 55.5, 20, "Cutoff", 10)
    clap_cutoff_knob.init_angle(snare.cutoff)
    clap_display = widgets.sound_display.SoundDisplay(clap, "Clap", 915, 50, 150, 30)

    master_level_knob = widgets.dial.Dial(1150, 120, 30, 0.02, 0.5, "Master", 15)
    master_level_knob.init_angle(1)

    kick_display.change_status()
    selected_sound = 0
    seq = Sequencer(bpm, hh, kick, snare, cymbal, clap)

    strip = widgets.numbers_strip.NumbersStrip(95, 560, 1100, 25, 17)

    save_button = widgets.action_button.ActionButton(375, 400, 50, 50, "Save")

    delimiters = []
    padding = 280
    for i in range(0, 3):
        delimiters.append(widgets.line_delimiter.LineDelimiter(365 + i * padding, 500, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check_clicked(event.pos):
                        button.change_status()
                        if button.status:
                            seq.add_sound(button.id, selected_sound)
                        else:
                            seq.remove_sound(button.id, selected_sound)
                        print(seq.pattern[selected_sound])

                if save_button.check_clicked(event.pos):
                    try:
                        seq.export_pattern("demo.wav", 44100)
                    except Exception as e:
                        print(e)

                if kick_shape_button.check_clicked(event.pos):
                    if kick.shape == 2:
                        kick.shape = 1
                    else:
                        kick.shape = 2
                    kick_shape_button.change_status()

                if snare_echo_button.check_clicked(event.pos):
                    if snare.apply_echo is False:
                        snare.apply_echo = True
                    else:
                        snare.apply_echo = False
                    snare_echo_button.change_status()

                if hh_echo_button.check_clicked(event.pos):
                    if hh.apply_echo is False:
                        hh.apply_echo = True
                    else:
                        hh.apply_echo = False
                    hh_echo_button.change_status()

                if cymbal_echo_button.check_clicked(event.pos):
                    if cymbal.apply_echo is False:
                        cymbal.apply_echo = True
                    else:
                        cymbal.apply_echo = False
                    cymbal_echo_button.change_status()

                if clap_echo_button.check_clicked(event.pos):
                    if clap.apply_echo is False:
                        clap.apply_echo = True
                    else:
                        clap.apply_echo = False
                    clap_echo_button.change_status()

                if bpm_dial.check_clicked(event.pos):
                    bpm_dial.dragging = True
                    bpm_dial.prev_angle = bpm_dial.calculate_angle(event.pos[0], event.pos[1])

                if kick_attack_knob.check_clicked(event.pos):
                    kick_attack_knob.dragging = True
                    kick_attack_knob.prev_angle = kick_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_decay_knob.check_clicked(event.pos):
                    kick_decay_knob.dragging = True
                    kick_decay_knob.prev_angle = kick_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_time_knob.check_clicked(event.pos):
                    kick_time_knob.dragging = True
                    kick_time_knob.prev_angle = kick_time_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_freq_knob.check_clicked(event.pos):
                    kick_freq_knob.dragging = True
                    kick_freq_knob.prev_angle = kick_freq_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_level_knob.check_clicked(event.pos):
                    kick_level_knob.dragging = True
                    kick_level_knob.prev_angle = kick_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_cutoff_knob.check_clicked(event.pos):
                    kick_cutoff_knob.dragging = True
                    kick_cutoff_knob.prev_angle = kick_cutoff_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_attack_knob.check_clicked(event.pos):
                    snare_attack_knob.dragging = True
                    snare_attack_knob.prev_angle = snare_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_decay_knob.check_clicked(event.pos):
                    snare_decay_knob.dragging = True
                    snare_decay_knob.prev_angle = snare_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_freq_knob.check_clicked(event.pos):
                    snare_freq_knob.dragging = True
                    snare_freq_knob.prev_angle = snare_freq_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_level_knob.check_clicked(event.pos):
                    snare_level_knob.dragging = True
                    snare_level_knob.prev_angle = snare_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_cutoff_knob.check_clicked(event.pos):
                    snare_cutoff_knob.dragging = True
                    snare_cutoff_knob.prev_angle = snare_cutoff_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_echo_delay_knob.check_clicked(event.pos):
                    snare_echo_delay_knob.dragging = True
                    snare_echo_delay_knob.prev_angle = snare_echo_delay_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_echo_feedback_knob.check_clicked(event.pos):
                    snare_echo_feedback_knob.dragging = True
                    snare_echo_feedback_knob.prev_angle = snare_echo_feedback_knob.calculate_angle(event.pos[0],
                                                                                                   event.pos[1])
                if hh_attack_knob.check_clicked(event.pos):
                    hh_attack_knob.dragging = True
                    hh_attack_knob.prev_angle = hh_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_decay_knob.check_clicked(event.pos):
                    hh_decay_knob.dragging = True
                    hh_decay_knob.prev_angle = hh_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_freq_knob.check_clicked(event.pos):
                    hh_freq_knob.dragging = True
                    hh_freq_knob.prev_angle = hh_freq_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_level_knob.check_clicked(event.pos):
                    hh_level_knob.dragging = True
                    hh_level_knob.prev_angle = hh_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_echo_delay_knob.check_clicked(event.pos):
                    hh_echo_delay_knob.dragging = True
                    hh_echo_delay_knob.prev_angle = hh_echo_delay_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_echo_feedback_knob.check_clicked(event.pos):
                    hh_echo_feedback_knob.dragging = True
                    hh_echo_feedback_knob.prev_angle = hh_echo_feedback_knob.calculate_angle(event.pos[0], event.pos[1])

                if cymbal_attack_knob.check_clicked(event.pos):
                    cymbal_attack_knob.dragging = True
                    cymbal_attack_knob.prev_angle = cymbal_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if cymbal_decay_knob.check_clicked(event.pos):
                    cymbal_decay_knob.dragging = True
                    cymbal_decay_knob.prev_angle = cymbal_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if cymbal_freq_knob.check_clicked(event.pos):
                    cymbal_freq_knob.dragging = True
                    cymbal_freq_knob.prev_angle = cymbal_freq_knob.calculate_angle(event.pos[0], event.pos[1])

                if cymbal_level_knob.check_clicked(event.pos):
                    cymbal_level_knob.dragging = True
                    cymbal_level_knob.prev_angle = cymbal_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if cymbal_echo_delay_knob.check_clicked(event.pos):
                    cymbal_echo_delay_knob.dragging = True
                    cymbal_echo_delay_knob.prev_angle = cymbal_echo_delay_knob.calculate_angle(event.pos[0],
                                                                                               event.pos[1])

                if cymbal_echo_feedback_knob.check_clicked(event.pos):
                    cymbal_echo_feedback_knob.dragging = True
                    cymbal_echo_feedback_knob.prev_angle = cymbal_echo_feedback_knob.calculate_angle(event.pos[0],
                                                                                                     event.pos[1])

                if clap_decay_knob.check_clicked(event.pos):
                    clap_decay_knob.dragging = True
                    clap_decay_knob.prev_angle = clap_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if clap_delay_knob.check_clicked(event.pos):
                    clap_delay_knob.dragging = True
                    clap_delay_knob.prev_angle = clap_delay_knob.calculate_angle(event.pos[0], event.pos[1])

                if clap_level_knob.check_clicked(event.pos):
                    clap_level_knob.dragging = True
                    clap_level_knob.prev_angle = clap_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if clap_echo_delay_knob.check_clicked(event.pos):
                    clap_echo_delay_knob.dragging = True
                    clap_echo_delay_knob.prev_angle = clap_echo_delay_knob.calculate_angle(event.pos[0], event.pos[1])

                if clap_echo_feedback_knob.check_clicked(event.pos):
                    clap_echo_feedback_knob.dragging = True
                    clap_echo_feedback_knob.prev_angle = clap_echo_feedback_knob.calculate_angle(event.pos[0],
                                                                                                 event.pos[1])

                if clap_cutoff_knob.check_clicked(event.pos):
                    clap_cutoff_knob.dragging = True
                    clap_cutoff_knob.prev_angle = clap_cutoff_knob.calculate_angle(event.pos[0], event.pos[1])

                if master_level_knob.check_clicked(event.pos):
                    master_level_knob.dragging = True
                    master_level_knob.prev_angle = master_level_knob.calculate_angle(event.pos[0], event.pos[1])

                if kick_display.check_clicked(event.pos):
                    kick_display.play_sample()
                    if not kick_display.status:
                        kick_display.change_status()
                        selected_sound = 0
                        if snare_display.status:
                            snare_display.change_status()
                        if hh_display.status:
                            hh_display.change_status()
                        if cymbal_display.status:
                            cymbal_display.change_status()
                        if clap_display.status:
                            clap_display.change_status()
                        change_buttons_status(selected_sound, seq, buttons)

                if snare_display.check_clicked(event.pos):
                    snare_display.play_sample()
                    if not snare_display.status:
                        snare_display.change_status()
                        selected_sound = 1
                        if kick_display.status:
                            kick_display.change_status()
                        if hh_display.status:
                            hh_display.change_status()
                        if cymbal_display.status:
                            cymbal_display.change_status()
                        if clap_display.status:
                            clap_display.change_status()
                        change_buttons_status(selected_sound, seq, buttons)

                if hh_display.check_clicked(event.pos):
                    hh_display.play_sample()
                    if not hh_display.status:
                        hh_display.change_status()
                        selected_sound = 2
                        if kick_display.status:
                            kick_display.change_status()
                        if snare_display.status:
                            snare_display.change_status()
                        if cymbal_display.status:
                            cymbal_display.change_status()
                        if clap_display.status:
                            clap_display.change_status()
                        change_buttons_status(selected_sound, seq, buttons)

                if cymbal_display.check_clicked(event.pos):
                    cymbal_display.play_sample()
                    if not cymbal_display.status:
                        cymbal_display.change_status()
                        selected_sound = 3
                        if kick_display.status:
                            kick_display.change_status()
                        if snare_display.status:
                            snare_display.change_status()
                        if hh_display.status:
                            hh_display.change_status()
                        if clap_display.status:
                            clap_display.change_status()
                        change_buttons_status(selected_sound, seq, buttons)

                if clap_display.check_clicked(event.pos):
                    clap_display.play_sample()
                    if not clap_display.status:
                        clap_display.change_status()
                        selected_sound = 4
                        if kick_display.status:
                            kick_display.change_status()
                        if snare_display.status:
                            snare_display.change_status()
                        if hh_display.status:
                            hh_display.change_status()
                        if cymbal_display.status:
                            cymbal_display.change_status()
                        change_buttons_status(selected_sound, seq, buttons)

            elif event.type == pygame.MOUSEBUTTONUP:
                bpm_dial.dragging = False

                kick_attack_knob.dragging = False
                kick_decay_knob.dragging = False
                kick_time_knob.dragging = False
                kick_freq_knob.dragging = False
                kick_level_knob.dragging = False
                kick_cutoff_knob.dragging = False

                snare_attack_knob.dragging = False
                snare_decay_knob.dragging = False
                snare_freq_knob.dragging = False
                snare_level_knob.dragging = False
                snare_cutoff_knob.dragging = False
                snare_echo_delay_knob.dragging = False
                snare_echo_feedback_knob.dragging = False

                hh_attack_knob.dragging = False
                hh_decay_knob.dragging = False
                hh_freq_knob.dragging = False
                hh_level_knob.dragging = False
                hh_echo_delay_knob.dragging = False
                hh_echo_feedback_knob.dragging = False

                cymbal_attack_knob.dragging = False
                cymbal_decay_knob.dragging = False
                cymbal_freq_knob.dragging = False
                cymbal_level_knob.dragging = False
                cymbal_echo_delay_knob.dragging = False
                cymbal_echo_feedback_knob.dragging = False

                clap_decay_knob.dragging = False
                clap_delay_knob.dragging = False
                clap_level_knob.dragging = False
                clap_echo_delay_knob.dragging = False
                clap_echo_feedback_knob.dragging = False
                clap_cutoff_knob.dragging = False

                master_level_knob.dragging = False

        if bpm_dial.dragging:
            bpm_dial.drag()
            bpm = bpm_dial.get_value()
            tempo_display.set_text(str(int(bpm)))
            seq.bpm = bpm

        if kick_attack_knob.dragging:
            kick_attack_knob.drag()
            kick.attack = kick_attack_knob.get_value()

        if kick_decay_knob.dragging:
            kick_decay_knob.drag()
            kick.decay = kick_decay_knob.get_value()

        if kick_time_knob.dragging:
            kick_time_knob.drag()
            kick.time = kick_time_knob.get_value()

        if kick_freq_knob.dragging:
            kick_freq_knob.drag()
            kick.freq = kick_freq_knob.get_value()

        if kick_level_knob.dragging:
            kick_level_knob.drag()
            kick.amp = kick_level_knob.get_value()

        if kick_cutoff_knob.dragging:
            kick_cutoff_knob.drag()
            kick.cutoff = kick_cutoff_knob.get_value()

        if snare_attack_knob.dragging:
            snare_attack_knob.drag()
            snare.attack = snare_attack_knob.get_value()

        if snare_decay_knob.dragging:
            snare_decay_knob.drag()
            snare.decay = snare_decay_knob.get_value()

        if snare_freq_knob.dragging:
            snare_freq_knob.drag()
            snare.freq = snare_freq_knob.get_value()

        if snare_level_knob.dragging:
            snare_level_knob.drag()
            snare.amp = snare_level_knob.get_value()

        if snare_cutoff_knob.dragging:
            snare_cutoff_knob.drag()
            snare.cutoff = snare_cutoff_knob.get_value()

        if snare_echo_delay_knob.dragging:
            snare_echo_delay_knob.drag()
            snare.d = snare_echo_delay_knob.get_value()

        if snare_echo_feedback_knob.dragging:
            snare_echo_feedback_knob.drag()
            snare.g = snare_echo_feedback_knob.get_value()

        if hh_attack_knob.dragging:
            hh_attack_knob.drag()
            hh.attack = hh_attack_knob.get_value()

        if hh_decay_knob.dragging:
            hh_decay_knob.drag()
            hh.decay = hh_decay_knob.get_value()

        if hh_freq_knob.dragging:
            hh_freq_knob.drag()
            hh.freq = hh_freq_knob.get_value()

        if hh_level_knob.dragging:
            hh_level_knob.drag()
            hh.amp = hh_level_knob.get_value()

        if hh_echo_delay_knob.dragging:
            hh_echo_delay_knob.drag()
            hh.d = hh_echo_delay_knob.get_value()

        if hh_echo_feedback_knob.dragging:
            hh_echo_feedback_knob.drag()
            hh.g = hh_echo_feedback_knob.get_value()

        if cymbal_attack_knob.dragging:
            cymbal_attack_knob.drag()
            cymbal.attack = cymbal_attack_knob.get_value()

        if cymbal_decay_knob.dragging:
            cymbal_decay_knob.drag()
            cymbal.decay = cymbal_decay_knob.get_value()

        if cymbal_freq_knob.dragging:
            cymbal_freq_knob.drag()
            cymbal.freq = cymbal_freq_knob.get_value()

        if cymbal_level_knob.dragging:
            cymbal_level_knob.drag()
            cymbal.amp = cymbal_level_knob.get_value()

        if cymbal_echo_delay_knob.dragging:
            cymbal_echo_delay_knob.drag()
            cymbal.d = cymbal_echo_delay_knob.get_value()

        if cymbal_echo_feedback_knob.dragging:
            cymbal_echo_feedback_knob.drag()
            cymbal.g = cymbal_echo_feedback_knob.get_value()

        if clap_decay_knob.dragging:
            clap_decay_knob.drag()
            clap.decay = clap_decay_knob.get_value()

        if clap_delay_knob.dragging:
            clap_delay_knob.drag()
            clap.delay_interval = clap_delay_knob.get_value()

        if clap_level_knob.dragging:
            clap_level_knob.drag()
            clap.amp = clap_level_knob.get_value()

        if clap_echo_delay_knob.dragging:
            clap_echo_delay_knob.drag()
            clap.d = clap_echo_delay_knob.get_value()

        if clap_echo_feedback_knob.dragging:
            clap_echo_feedback_knob.drag()
            clap.g = clap_echo_feedback_knob.get_value()

        if clap_cutoff_knob.dragging:
            clap_cutoff_knob.drag()
            clap.cutoff = clap_cutoff_knob.get_value()

        if master_level_knob.dragging:
            master_level_knob.drag()
            kick.master_amp = master_level_knob.get_value()
            snare.master_amp = master_level_knob.get_value()
            hh.master_amp = master_level_knob.get_value()
            cymbal.master_amp = master_level_knob.get_value()
            clap.master_amp = master_level_knob.get_value()

        screen.fill(background_color)

        for button in buttons:
            button.draw(screen)

        tempo_display.draw(screen)

        bpm_dial.draw(screen)
        kick_display.draw(screen)
        snare_display.draw(screen)
        hh_display.draw(screen)
        cymbal_display.draw(screen)
        clap_display.draw(screen)

        kick_attack_knob.draw(screen)
        kick_decay_knob.draw(screen)
        kick_time_knob.draw(screen)
        kick_freq_knob.draw(screen)
        kick_level_knob.draw(screen)
        kick_shape_button.draw(screen)
        kick_cutoff_knob.draw(screen)

        snare_attack_knob.draw(screen)
        snare_decay_knob.draw(screen)
        snare_freq_knob.draw(screen)
        snare_level_knob.draw(screen)
        snare_cutoff_knob.draw(screen)
        snare_echo_delay_knob.draw(screen)
        snare_echo_feedback_knob.draw(screen)
        snare_echo_button.draw(screen)

        hh_attack_knob.draw(screen)
        hh_decay_knob.draw(screen)
        hh_freq_knob.draw(screen)
        hh_level_knob.draw(screen)
        hh_echo_delay_knob.draw(screen)
        hh_echo_feedback_knob.draw(screen)
        hh_echo_button.draw(screen)

        cymbal_attack_knob.draw(screen)
        cymbal_decay_knob.draw(screen)
        cymbal_freq_knob.draw(screen)
        cymbal_level_knob.draw(screen)
        cymbal_echo_delay_knob.draw(screen)
        cymbal_echo_feedback_knob.draw(screen)
        cymbal_echo_button.draw(screen)

        clap_decay_knob.draw(screen)
        clap_delay_knob.draw(screen)
        clap_level_knob.draw(screen)
        clap_echo_delay_knob.draw(screen)
        clap_echo_feedback_knob.draw(screen)
        clap_echo_button.draw(screen)
        clap_cutoff_knob.draw(screen)

        master_level_knob.draw(screen)

        save_button.draw(screen)

        strip.draw(screen)

        for line in delimiters:
            line.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
