# sound_handler.py handles all server-side sounds

import pygame

class Sound:
    def __init__(self, sound_key, sound, channel_num):
        self.sound_key = sound_key
        self.sound = sound
        self.channel = pygame.mixer.Channel(channel_num)
        self.is_played = False

pygame.mixer.init()
pygame.mixer.set_num_channels(100)
class SoundHandler:
    def __init__(self):
        self.sounds = {
            "menu": Sound("menu", pygame.mixer.Sound("sounds\\menu_screen_music.wav"), 1),
            "answer_melody1": Sound("answer_melody1", pygame.mixer.Sound("sounds\\answer_melody1.wav"), 2),
            "answer_melody2": Sound("answer_melody2", pygame.mixer.Sound("sounds\\answer_melody2.wav"), 3),
            "answer_melody3": Sound("answer_melody3", pygame.mixer.Sound("sounds\\answer_melody3.wav"), 4),
            "answer_melody4": Sound("answer_melody4", pygame.mixer.Sound("sounds\\answer_melody4.wav"), 5),
            "is_answer_correct": Sound("is_answer_correct", pygame.mixer.Sound("sounds\\is_answer_correct.wav"), 6),
            "results_music": Sound("results_music", pygame.mixer.Sound("sounds\\results_music.wav"), 7)
        }
        self.current_sound_playing = None

    def play_sound(self, sound_key, loops=0):
        sound = self.sounds[sound_key]
        if not sound.channel.get_busy():
            sound.channel.play(sound.sound, loops=loops)
            self.current_sound_playing = sound
            sound.is_played = True

    def stop_sound(self, sound_key):
        sound = self.sounds[sound_key]
        if sound.channel.get_busy():
            sound.channel.stop()
            self.current_sound_playing = None

    def get_sound_playing(self):
        for sound in self.sounds.values():
            if sound.channel.get_busy():
                return sound

    def reset_is_played(self):
        for sound in self.sounds.values():
            sound.is_played = False