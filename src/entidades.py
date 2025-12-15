import math
import random
import pygame
from src.settings import *

class Particula:
    def __init__(self, x, y, cor):
        self.x, self.y = x, y
        self.cor = cor
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.vida = 255
    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 10
    def desenhar(self, surface):
        if self.vida > 0:
            pygame.draw.circle(surface, self.cor, (int(self.x), int(self.y)), 4)

class Inimigo:
    def __init__(self, game, caminho, tipo, nivel_fantasma, drop):
        inimigo = INIMIGOS_DADOS[tipo]
        self.drop = drop
        self.CAMINHO = caminho
        self.x, self.y = caminho[0]
        self.indice = 0
        self.e_boss = inimigo["BOSS_FLAG"]
        self.vida = inimigo["VIDA_BASE"] + inimigo["VIDA_BASE"] * nivel_fantasma/10
        self.velocidade = inimigo["VELOCIDADE"] + inimigo["VELOCIDADE"] * nivel_fantasma / 20
        self.raio = 25 if self.e_boss else 12
        self.pass_cooldown = 0
        self.sprite = game.SPRITES[inimigo["SPRITE"]]

    def mover(self):
        if self.indice < len(self.CAMINHO) - 1:
            alvo = self.CAMINHO[self.indice + 1]
            dist = math.hypot(alvo[0] - self.x, alvo[1] - self.y)
            if dist > self.velocidade:
                self.x += (alvo[0] - self.x) / dist * self.velocidade
                self.y += (alvo[1] - self.y) / dist * self.velocidade
            else:
                self.indice += 1

class Torre:
    def __init__(self, x, y, tipo, sprites_dict):
        self.x, self.y = x, y
        self.tipo = tipo
        dados = sprites_dict.get("DADOS_DEUSES_OVERRIDE")
        if dados is None:
            self.custo, self.alcance, self.dano_base, self.cadencia_base, self.cor = sprites_dict.get("DADOS_DEUSES_BASE")[tipo]
        else:
            self.custo, self.alcance, self.dano_base, self.cadencia_base, self.cor = dados[tipo]
        self.timer = 0
        self.raio_torre = sprites_dict.get("TOWER_RADIO_OVERRIDE", {"Zeus":20,"Anubis":20,"Odin":24}).get(tipo, 20)
        if tipo == "Odin":
            self.sprite_normal = sprites_dict.get("SPRITE_ODIN_NORMAL")
            self.sprite_anim = sprites_dict.get("SPRITE_ODIN_ANIM")
        elif tipo == "Zeus":
            self.sprite_normal = sprites_dict.get("SPRITE_ZEUS_NORMAL")
            self.sprite_anim = sprites_dict.get("SPRITE_ZEUS_ANIM")
        elif tipo == "Anubis":
            self.sprite_normal = sprites_dict.get("SPRITE_ANUBIS_NORMAL")
            self.sprite_anim = sprites_dict.get("SPRITE_ANUBIS_ANIM")
        else:
            self.sprite_normal = None
            self.sprite_anim = None
        self.anim_timer = 0
        self.anim_duration = 12

    def atacar(self, inimigos, tela, multiplicador_dano, multiplicador_vel):
        if self.timer > 0:
            self.timer -= 1
        alvo = None
        min_dist = None
        for inimigo in inimigos:
            d = math.hypot(inimigo.x - self.x, inimigo.y - self.y)
            if d <= self.alcance:
                if min_dist is None or d < min_dist:
                    min_dist = d
                    alvo = inimigo
        if alvo is None:
            return
        if self.timer > 0:
            return
        alvo.vida -= self.dano_base * multiplicador_dano
        self.timer = int(self.cadencia_base / multiplicador_vel)
        if self.tipo == "Zeus":
            desenhar_raio(tela, (self.x, self.y), (alvo.x, alvo.y), self.cor, segmentos=10, max_offset=22, espessura=3)
        elif self.tipo == "Odin":
            desenhar_raio(tela, (self.x, self.y), (alvo.x, alvo.y), self.cor, segmentos=2, max_offset=22, espessura=3)
            pygame.draw.circle(tela, (20,20,20), (int(alvo.x - 5), int(alvo.y - 5)), 6)
            pygame.draw.circle(tela, (40,40,40), (int(alvo.x + 5), int(alvo.y + 5)), 6)
        else:
            desenhar_raio(tela, (self.x, self.y), (alvo.x, alvo.y), self.cor, segmentos=3, max_offset=22, espessura=5)
        self.anim_timer = self.anim_duration

class Drop:
    def __init__(self, x, y, rd, sprite=None):
        self.rect = pygame.Rect(x-20, y-20, 40, 40)
        self.rd = rd
        self.cor = {1:(255,215,0),2:(0,255,255),3:(128,0,128)}.get(rd)
        self.coletado = False
        self.sprite = sprite

# função auxiliar usada por Torre.atacar
from src.utils import desenhar_raio