import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        self.base_path = os.path.join("assets", "music")
        self.base_sfx_path = os.path.join("assets", "sfx")  # pasta para SFX
        self.musica_atual = None
        self.sons = {}  # dicionário para SFX

        self.carregar_sons()  # carregar SFX ao iniciar

    # ---------- MÚSICAS ----------
    def _tocar(self, nome_arquivo, loop):
        caminho = os.path.join(self.base_path, nome_arquivo)
        if self.musica_atual == caminho:
            return  
        self.musica_atual = caminho
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(loop)

    def menu(self):
        self._tocar("menu.mp3", -1)

    def gameplay(self):
        self._tocar("gameplay.mp3", -1)

    def vitoria(self):
        self._tocar("vitoria.mp3", 0)

    def derrota(self):
        self._tocar("derrota.mp3", 0)

    def parar(self):
        pygame.mixer.music.stop()
        self.musica_atual = None

    # ---------- SFX ----------
    def carregar_sons(self):
        self.sons['build'] = pygame.mixer.Sound(os.path.join(self.base_sfx_path, "build.wav"))
        self.sons['enemy_death'] = pygame.mixer.Sound(os.path.join(self.base_sfx_path, "enemy_death.wav"))
        self.sons['coleta'] = pygame.mixer.Sound(os.path.join(self.base_sfx_path, "coleta.wav"))

    def tocar(self, nome_som):
        if nome_som in self.sons:
            self.sons[nome_som].play()
        else:
            print(f"[AudioManager] Som '{nome_som}' não encontrado!")