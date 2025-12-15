import os
import pygame
import math
import random
from src.assets import carregar_todos_assets
from src.entidades import Inimigo, Torre, Drop, Particula
from src.utils import circular_crop, desenhar_raio, esta_no_caminho, pode_construir_torre
from src.scenes import *
from src.settings import *

class Game:
    def __init__(self):
        pygame.init()
     
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Clash of Pantheons: The Gate Guardians")
        self.relogio = pygame.time.Clock()

        self.fonte_titulo = pygame.font.Font("assets/fonts/Semper Invicta.ttf", 50)
        self.fonte_ui = pygame.font.Font("assets/fonts/Semper Invicta.ttf", 30)
        self.fonte_pequena = pygame.font.Font("assets/fonts/Semper Invicta.ttf", 22)

        self.lista_tipos = ["Zeus", "Anubis", "Odin"]
        self.indice_tipo = 0
        self.selecionado = self.lista_tipos[self.indice_tipo]
        self.switch_anim_timer = 0
        self.switch_anim_duration = 300

        self.estado_jogo = "MENU"
        self.round_atual = 1
        self.alminhas_restantes = 30
        self.ouro = 400
        self.vidas = 20
        self.multiplicador_dano = 1.0
        self.multiplicador_vel = 1.0

        self.inimigos_mortos_total = 0
        self.nivel_fantasma = 1.0
        self.drops_coletados = 0

        self.mensagem_popup = None
        self.tempo_epilogo = None
        self.DURACAO_POPUP_MS = 2000

        assets = carregar_todos_assets()
        self.SPRITES = assets

        self.lista_inimigos = []
        self.lista_torres = []
        self.lista_particulas = []
        self.lista_drops = []
        self.spawn_timer = 0
        self.spawn_count = 0

        #Botões de mapa
        self.level_buttons = []
        for i in range(NUM_LEVELS):
            self.level_buttons.append(
                pygame.Rect(
                    120+ 140*i - (i//5)*140*5, #PosX
                    100 + (i//5)*140, #PosY
                    110,110))
        self.last_level = 0
        self.actual_level = 0

        self.reset_jogo()

    def set_popup(self, texto, cor):
        self.mensagem_popup = (texto, cor, pygame.time.get_ticks())

    def desenhar_popup(self):
        if self.mensagem_popup is None:
            return
        texto, cor, tempo_inicio = self.mensagem_popup
        if pygame.time.get_ticks() - tempo_inicio > self.DURACAO_POPUP_MS:
            self.mensagem_popup = None
            return
        txt_render = self.fonte_ui.render(texto, True, BRANCO)
        fundo = pygame.Surface((txt_render.get_width() + 20, txt_render.get_height() + 10))
        fundo.set_alpha(180)
        fundo.fill(cor)
        self.tela.blit(fundo, (10, 10))
        self.tela.blit(txt_render, (20, 15))

    def reset_jogo(self):
        self.round_atual = 0
        self.script_inimigo = None
        self.alminhas_restantes = 0
        self.espera = 0
        self.espera_orda = 0
        self.ouro = 400
        self.vidas = 20
        self.multiplicador_dano = 1.0
        self.multiplicador_vel = 1.0
        self.inimigos_mortos_total = 0
        self.nivel_fantasma = 1.0
        self.drops_coletados = 0
        self.lista_inimigos.clear()
        self.lista_torres.clear()
        self.lista_particulas.clear()
        self.lista_drops.clear()
        self.tempo_epilogo = None
        self.spawn_count = 0

        self.total_itens = 0 
        for i in FASE_SCRIPT[self.actual_level]:
            if(i[3] != 0):
                self.total_itens += 1

    def desenhar_icone_deus(self, cx, cy, tipo, scale=1.0):
        cor = DADOS_DEUSES[tipo][4]
        raio_base = TOWER_RADIO.get(tipo, 20)
        raio = max(6, int(raio_base * scale))
        perfil = self.SPRITES["PERFIS"].get(tipo)
        if perfil is not None:
            size = max(12, int(raio * 2.2))
            perfil_circ = circular_crop(perfil, size)
            self.tela.blit(perfil_circ, (int(cx - size/2), int(cy - size/2)))
        else:
            pygame.draw.circle(self.tela, cor, (int(cx), int(cy)), raio)
            pygame.draw.circle(self.tela, (0,0,0), (int(cx), int(cy)), raio, 2)
            letra = self.fonte_pequena.render(tipo[0], True, BRANCO)
            self.tela.blit(letra, (cx - letra.get_width()//2, cy - letra.get_height()//2))
        if tipo == "Zeus":
            pygame.draw.line(self.tela, BRANCO, (cx - raio//2, cy - 2), (cx + raio//8, cy + raio//3), 2)
            pygame.draw.line(self.tela, BRANCO, (cx + raio//8, cy + raio//3), (cx - raio//4, cy + raio//3), 2)
        elif tipo == "Odin":
            pygame.draw.circle(self.tela, (20,20,20), (cx - raio//3, cy - raio//3), max(1, raio//6))
            pygame.draw.circle(self.tela, (40,40,40), (cx + raio//3, cy - raio//3), max(1, raio//6))

    def treat_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.rodando = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if self.estado_jogo == "LEVEL_MENU":
                    for i in range(self.last_level+1):
                        if self.level_buttons[i].collidepoint(ev.pos):
                            self.actual_level = i
                            self.reset_jogo()
                            self.estado_jogo = "JOGANDO"
                elif self.estado_jogo == "JOGANDO":
                    mx, my = pygame.mouse.get_pos()
                    for d in self.lista_drops[:]:
                        if not d.coletado and d.rect.collidepoint(ev.pos):
                            d.coletado = True
                            self.drops_coletados += 1
                            if d.rd == 1:
                                self.multiplicador_dano += 0.25
                                self.set_popup("Raio Mestre de ZEUS coletado!: Dano de ataque aumentado", CORES_DROP[1])
                            elif d.rd == 2:
                                self.multiplicador_vel += 0.25
                                self.set_popup("Botas de HERMES coletadas!: Atack speed aumentado", CORES_DROP[2])
                            elif d.rd == 3:
                                self.set_popup("Chave do Portal coletada!: Agora podemos fechar o portal", CORES_DROP[3])
                    else:
                        custo = DADOS_DEUSES[self.selecionado][0]
                        if self.ouro >= custo and my < 550:
                            if esta_no_caminho(mx, my, CAMINHO[self.actual_level]):
                                self.set_popup("Não pode construir no caminho!", (150,0,0))
                            elif not pode_construir_torre(mx, my, self.selecionado, self.lista_torres, TOWER_RADIO, MIN_DIST_MARGIN):
                                self.set_popup("Torre muito próxima!", (150,0,0))
                            else:
                                self.lista_torres.append(Torre(mx, my, self.selecionado, self.SPRITES))
                                self.ouro -= custo
            if ev.type == pygame.KEYDOWN and self.estado_jogo == "JOGANDO":
                mudou = False
                if ev.key == pygame.K_1:
                    self.indice_tipo = 0; mudou = True
                if ev.key == pygame.K_2:
                    self.indice_tipo = 1; mudou = True
                if ev.key == pygame.K_3:
                    self.indice_tipo = 2; mudou = True
                if ev.key == pygame.K_LEFT:
                    self.indice_tipo = (self.indice_tipo - 1) % 3; mudou = True
                if ev.key == pygame.K_RIGHT:
                    self.indice_tipo = (self.indice_tipo + 1) % 3; mudou = True
                if mudou:
                    self.selecionado = self.lista_tipos[self.indice_tipo]
                    self.switch_anim_timer = self.switch_anim_duration

    def run(self):
        self.rodando = True
        while self.rodando:

            self.treat_events()

            if self.estado_jogo == "MENU": Menu(self)
            elif self.estado_jogo == "DESCRIÇÃO": Descricao(self)
            elif self.estado_jogo == "LEVEL_MENU": Levels(self)
            elif self.estado_jogo == "JOGANDO": Jogando(self)
            elif self.estado_jogo == "EPILOGO": Epilogo(self)
            elif self.estado_jogo == "VITORIA_EPICA": Vitoria_Epica(self)
            elif self.estado_jogo == "DERROTA": Derrota(self)

            if self.estado_jogo == "EPILOGO" and self.tempo_epilogo is None:
                self.tempo_epilogo = pygame.time.get_ticks()

            pygame.display.flip()

        pygame.quit()