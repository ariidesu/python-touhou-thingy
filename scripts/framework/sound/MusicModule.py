from pygame import mixer

from os import listdir
from os.path import join as path_join

from scripts.framework.sound.Sound import Sound
from scripts.framework.environment import DEFAULT_GLOBAL_VOLUME, DEFAULT_MUSIC_VOLUME, PATH


class MusicModule:
    def __init__(self, volume: float = 1) -> None:
        mixer.init()

        self.sounds = [
            Sound(
                path_join(PATH, "assets", "sounds", filename),
                global_volume=DEFAULT_GLOBAL_VOLUME
            )

            for filename in filter(
                lambda x: x.endswith(".wav") or x.endswith(".ogg"),
                listdir(path_join(PATH, "assets", "sounds"))
            )
        ]

        self.sounds.sort(key=lambda sound: sound.name)
        self.bg_volume = volume

    def changeSoundConfig(self, index: int, duration: int = None, fade: int = None,
                          global_volume: float = None) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)

        if index in range(len(self.sounds)):
            self.sounds[index].changeConfig(duration, fade, global_volume)

    def setGlobalVolume(self, global_volume: float) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)
        for sound in self.sounds:
            sound.changeConfig(global_volume=global_volume)

    def __getitem__(self, index: int) -> Sound:
        if index in range(len(self.sounds)):
            return self.sounds[index]
        return None

    @staticmethod
    def playMusic(background: str, volume: float = DEFAULT_MUSIC_VOLUME) -> None:
        mixer.music.load(path_join(PATH, "assets", "music", background))
        mixer.music.set_volume(volume)
        mixer.music.play(-1)

    @staticmethod
    def stopMusic() -> None:
        mixer.music.unload()
