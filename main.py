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
    kick_attack_knob = widgets.dial.Dial(115, 120, 20, 0.1, 10, "Attack", 10)
    kick_decay_knob = widgets.dial.Dial(170, 120, 20, 0.1, 10, "Decay", 10)
    kick_time_knob = widgets.dial.Dial(115, 180, 20, 0.04, 5, "Time", 10)
    kick_freq_knob = widgets.dial.Dial(170, 180, 20, 0.2, 30, "Tone", 10)
    kick_shape_button = widgets.shape_button.ShapeButton(210, 110, 20, 20, "Shape")
    kick_display = widgets.sound_display.SoundDisplay(kick, "Bass Drum", 95, 50, 150, 30)

    snare = core.snare.Snare(44100, 1)
    snare_attack_knob = widgets.dial.Dial(320, 120, 20, 0.1, 10, "Attack", 10)
    snare_decay_knob = widgets.dial.Dial(375, 120, 20, 0.1, 10, "Decay", 10)
    snare_freq_knob = widgets.dial.Dial(320, 180, 20, 0.3, 80, "Tone", 10)
    snare_display = widgets.sound_display.SoundDisplay(snare, "Snare Drum", 300, 50, 150, 30)

    hh = core.cymbal.Cymbal(44100, 1)
    hh_attack_knob = widgets.dial.Dial(525, 120, 20, 0.1, 10, "Attack", 10)
    hh_decay_knob = widgets.dial.Dial(580, 120, 20, 0.04, 15, "Decay", 10)
    hh_freq_knob = widgets.dial.Dial(525, 180, 20, 11, 2000, "Tone", 10)
    hh_display = widgets.sound_display.SoundDisplay(hh, "Hi Hat", 505, 50, 150, 30)

    cymbal = core.cymbal.Cymbal(44100, 1)
    cymbal.decay = 10
    cymbal.attack = 30
    cymbal_display = widgets.sound_display.SoundDisplay(cymbal, "Cymbal", 710, 50, 150, 30)

    clap = core.clap.Clap(44100, 1)
    clap_display = widgets.sound_display.SoundDisplay(clap, "Clap", 915, 50, 150, 30)

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

                if snare_attack_knob.check_clicked(event.pos):
                    snare_attack_knob.dragging = True
                    snare_attack_knob.prev_angle = snare_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_decay_knob.check_clicked(event.pos):
                    snare_decay_knob.dragging = True
                    snare_decay_knob.prev_angle = snare_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if snare_freq_knob.check_clicked(event.pos):
                    snare_freq_knob.dragging = True
                    snare_freq_knob.prev_angle = snare_freq_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_attack_knob.check_clicked(event.pos):
                    hh_attack_knob.dragging = True
                    hh_attack_knob.prev_angle = hh_attack_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_decay_knob.check_clicked(event.pos):
                    hh_decay_knob.dragging = True
                    hh_decay_knob.prev_angle = hh_decay_knob.calculate_angle(event.pos[0], event.pos[1])

                if hh_freq_knob.check_clicked(event.pos):
                    hh_freq_knob.dragging = True
                    hh_freq_knob.prev_angle = hh_freq_knob.calculate_angle(event.pos[0], event.pos[1])

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

                snare_attack_knob.dragging = False
                snare_decay_knob.dragging = False
                snare_freq_knob.dragging = False

                hh_attack_knob.dragging = False
                hh_decay_knob.dragging = False
                hh_freq_knob.dragging = False

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

        if snare_attack_knob.dragging:
            snare_attack_knob.drag()
            snare.attack = snare_attack_knob.get_value()

        if snare_decay_knob.dragging:
            snare_decay_knob.drag()
            snare.decay = snare_decay_knob.get_value()

        if snare_freq_knob.dragging:
            snare_freq_knob.drag()
            snare.freq = snare_freq_knob.get_value()

        if hh_attack_knob.dragging:
            hh_attack_knob.drag()
            hh.attack = hh_attack_knob.get_value()

        if hh_decay_knob.dragging:
            hh_decay_knob.drag()
            hh.decay = hh_decay_knob.get_value()

        if hh_freq_knob.dragging:
            hh_freq_knob.drag()
            hh.freq = hh_freq_knob.get_value()

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
        kick_shape_button.draw(screen)

        snare_attack_knob.draw(screen)
        snare_decay_knob.draw(screen)
        snare_freq_knob.draw(screen)

        hh_attack_knob.draw(screen)
        hh_decay_knob.draw(screen)
        hh_freq_knob.draw(screen)

        save_button.draw(screen)

        strip.draw(screen)

        for line in delimiters:
            line.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
