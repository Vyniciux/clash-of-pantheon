import pygame
from audio import AudioManager
from src.game import Game

def main():
    pygame.init()

    audio = AudioManager()
    jogo = Game(audio)
    jogo.run()

if __name__ == "__main__":
    main()
