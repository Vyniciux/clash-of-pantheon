import os
import pygame
import math
import random
from assets import carregar_todos_assets
from entidades import Inimigo, Torre, Drop, Particula
from utils import circular_crop, desenhar_raio, esta_no_caminho, pode_construir_torre

class Game:
    def __init__(self):
        pygame.init()
        self.LARGURA, self.ALTURA = 900, 650
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Clash of Pantheons: The Gate Guardians")
        self.relogio = pygame.time.Clock()

        self.FUNDO_MENU = (10, 10, 25)
        self.GRAMA = (34, 139, 34)
        self.ESTRADA = (100, 80, 60)
        self.OURO = (218, 165, 32)
        self.BRANCO = (255, 255, 255)
        self.CORES_DROP = {1: (255, 215, 0), 2: (0, 255, 255), 3: (128, 0, 128)}

        self.fonte_titulo = pygame.font.SysFont("serif", 60, bold=True)
        self.fonte_ui = pygame.font.SysFont("serif", 24)
        self.fonte_pequena = pygame.font.SysFont("serif", 18, bold=True)

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

        self.CAMINHO = [
            (0, 300), (250, 300), (250, 100),
            (550, 100), (550, 500), (900, 500)
        ]

        self.DADOS_DEUSES = {
            "Zeus":   [100, 200, 2, 15, (255, 215, 0)],
            "Anubis": [250, 260, 1, 20, (200, 180, 0)],
            "Odin":   [400, 230, 5, 20, (50, 50, 100)]
        }

        self.TOWER_RADIO = {"Zeus": 20, "Anubis": 20, "Odin": 24}
        self.MIN_DIST_MARGIN = 8
        self.lista_tipos = ["Zeus", "Anubis", "Odin"]
        self.indice_tipo = 0
        self.selecionado = self.lista_tipos[self.indice_tipo]
        self.switch_anim_timer = 0
        self.switch_anim_duration = 300
        self.ODIN_SCALE = 1.15

        assets = carregar_todos_assets()
        self.SPRITES = assets

        self.lista_inimigos = []
        self.lista_torres = []
        self.lista_particulas = []
        self.lista_drops = []
        self.spawn_timer = 0
        self.spawn_count = 0

    def set_popup(self, texto, cor):
        self.mensagem_popup = (texto, cor, pygame.time.get_ticks())

    def desenhar_popup(self):
        if self.mensagem_popup is None:
            return
        texto, cor, tempo_inicio = self.mensagem_popup
        if pygame.time.get_ticks() - tempo_inicio > self.DURACAO_POPUP_MS:
            self.mensagem_popup = None
            return
        txt_render = self.fonte_ui.render(texto, True, self.BRANCO)
        fundo = pygame.Surface((txt_render.get_width() + 20, txt_render.get_height() + 10))
        fundo.set_alpha(180)
        fundo.fill(cor)
        self.tela.blit(fundo, (10, 10))
        self.tela.blit(txt_render, (20, 15))

    def reset_jogo(self):
        self.round_atual = 1
        self.alminhas_restantes = 30
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
        self.estado_jogo = "JOGANDO"
        self.spawn_count = 0

    def desenhar_icone_deus(self, cx, cy, tipo, scale=1.0):
        cor = self.DADOS_DEUSES[tipo][4]
        raio_base = self.TOWER_RADIO.get(tipo, 20)
        raio = max(6, int(raio_base * scale))
        perfil = self.SPRITES["PERFIS"].get(tipo)
        if perfil is not None:
            size = max(12, int(raio * 2.2))
            perfil_circ = circular_crop(perfil, size)
            self.tela.blit(perfil_circ, (int(cx - size/2), int(cy - size/2)))
        else:
            pygame.draw.circle(self.tela, cor, (int(cx), int(cy)), raio)
            pygame.draw.circle(self.tela, (0,0,0), (int(cx), int(cy)), raio, 2)
            letra = self.fonte_pequena.render(tipo[0], True, self.BRANCO)
            self.tela.blit(letra, (cx - letra.get_width()//2, cy - letra.get_height()//2))
        if tipo == "Zeus":
            pygame.draw.line(self.tela, self.BRANCO, (cx - raio//2, cy - 2), (cx + raio//8, cy + raio//3), 2)
            pygame.draw.line(self.tela, self.BRANCO, (cx + raio//8, cy + raio//3), (cx - raio//4, cy + raio//3), 2)
        elif tipo == "Odin":
            pygame.draw.circle(self.tela, (20,20,20), (cx - raio//3, cy - raio//3), max(1, raio//6))
            pygame.draw.circle(self.tela, (40,40,40), (cx + raio//3, cy - raio//3), max(1, raio//6))

    def run(self):
        rodando = True
        while rodando:
            dt = self.relogio.tick(60)
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    rodando = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_jogo == "MENU":
                        if pygame.Rect(300,450,300,60).collidepoint(ev.pos):
                            self.reset_jogo()
                    elif self.estado_jogo == "JOGANDO":
                        coletou_drop = False
                        for d in self.lista_drops[:]:
                            if not d.coletado and d.rect.collidepoint(ev.pos):
                                d.coletado = True
                                self.drops_coletados += 1
                                coletou_drop = True
                                if d.rd == 1:
                                    self.multiplicador_dano += 0.25
                                    self.set_popup("Raio Mestre de ZEUS coletado!: Dano de ataque aumentado", self.CORES_DROP[1])
                                elif d.rd == 2:
                                    self.multiplicador_vel += 0.25
                                    self.set_popup("Botas de HERMES coletadas!: Atack speed aumentado", self.CORES_DROP[2])
                                elif d.rd == 3:
                                    self.set_popup("Chave do Portal coletada!: Agora podemos fechar o portal", self.CORES_DROP[3])
                        if coletou_drop:
                            if self.drops_coletados >= 3 and self.estado_jogo != "EPILOGO":
                                self.tempo_epilogo = pygame.time.get_ticks()
                                self.estado_jogo = "EPILOGO"
                        else:
                            custo = self.DADOS_DEUSES[self.selecionado][0]
                            if self.ouro >= custo and my < 550:
                                if esta_no_caminho(mx, my, self.CAMINHO):
                                    self.set_popup("Não pode construir no caminho!", (150,0,0))
                                elif not pode_construir_torre(mx, my, self.selecionado, self.lista_torres, self.TOWER_RADIO, self.MIN_DIST_MARGIN):
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

            if self.estado_jogo == "MENU":
                bg = self.SPRITES.get("MENU_BG")
                if bg is not None:
                    self.tela.blit(bg, (0,0))
                else:
                    self.tela.fill(self.FUNDO_MENU)
                t = self.fonte_titulo.render("CLASH OF PANTHEONS", True, self.OURO)
                self.tela.blit(t, (100,150))
                btn = pygame.Rect(300,450,300,60)
                pygame.draw.rect(self.tela, self.OURO, btn, 2)
                txt = self.fonte_ui.render("INICIAR DEFESA", True, self.BRANCO)
                self.tela.blit(txt, (btn.x+60, btn.y+15))

            elif self.estado_jogo == "JOGANDO":
                self.tela.fill(self.GRAMA)
                pygame.draw.lines(self.tela, self.ESTRADA, False, self.CAMINHO, 50)

                self.spawn_timer += 1
                if self.alminhas_restantes > 0 and self.spawn_timer > 40:
                    chosen_sprite = self.SPRITES["SPRITE_ROUND1"]
                    if self.round_atual == 2:
                        chosen_sprite = self.SPRITES["SPRITE_ROUND2"]
                    elif self.round_atual >= 3:
                        chosen_sprite = self.SPRITES["SPRITE_ROUND3"]
                    self.lista_inimigos.append(Inimigo(False, chosen_sprite, self.CAMINHO, self.round_atual, self.nivel_fantasma))
                    self.spawn_count += 1
                    self.alminhas_restantes -= 1
                    self.spawn_timer = 0
                elif self.alminhas_restantes == 0 and len(self.lista_inimigos) == 0 and self.round_atual <= 3:
                    boss_sprite = self.SPRITES["SPRITE_BOSS1"]
                    if self.round_atual == 2:
                        boss_sprite = self.SPRITES["SPRITE_BOSS2"]
                    elif self.round_atual == 3:
                        boss_sprite = self.SPRITES["SPRITE_BOSS3"]
                    self.lista_inimigos.append(Inimigo(True, boss_sprite, self.CAMINHO, self.round_atual, self.nivel_fantasma))
                    self.alminhas_restantes = -1

                for t in list(self.lista_torres):
                    t.atacar(self.lista_inimigos, self.tela, self.multiplicador_dano, self.multiplicador_vel)
                    if t.anim_timer > 0:
                        t.anim_timer -= 1
                    base_size = max(8, int(t.raio_torre * 2))
                    if t.tipo == "Odin":
                        size = max(8, int(base_size * self.ODIN_SCALE))
                    else:
                        size = max(8, int(base_size * 1.10))
                    mostrar_anim = False
                    if t.anim_timer > 0 and t.sprite_anim is not None:
                        mostrar_anim = (t.anim_timer % 6) < 3
                    sprite_to_draw = None
                    if mostrar_anim and t.sprite_anim is not None:
                        sprite_to_draw = t.sprite_anim
                    elif t.sprite_normal is not None:
                        sprite_to_draw = t.sprite_normal
                    if sprite_to_draw is not None:
                        img = pygame.transform.smoothscale(sprite_to_draw, (size, size))
                        self.tela.blit(img, (int(t.x - size/2), int(t.y - size/2)))
                    else:
                        pygame.draw.circle(self.tela, t.cor, (int(t.x), int(t.y)), t.raio_torre)

                for i in list(self.lista_inimigos):
                    i.mover()
                    if getattr(i, "sprite", None) is not None:
                        size = max(8, int(i.raio * 2.4)) if i.e_boss else max(4, int(i.raio * 2))
                        img = pygame.transform.smoothscale(i.sprite, (size, size))
                        self.tela.blit(img, (int(i.x - size/2), int(i.y - size/2)))
                    else:
                        cor_i = (200,0,0) if not i.e_boss else (100,0,0)
                        pygame.draw.circle(self.tela, cor_i, (int(i.x), int(i.y)), i.raio)

                    if i.vida <= 0:
                        if not i.e_boss:
                            self.ouro += 25
                            self.inimigos_mortos_total += 1
                            if self.inimigos_mortos_total % 20 == 0:
                                self.nivel_fantasma += 0.15
                                self.set_popup("Fantasmas mais fortes!", (150,0,0))
                        else:
                            for _ in range(30):
                                self.lista_particulas.append(Particula(i.x, i.y, self.CORES_DROP[self.round_atual]))
                            if self.round_atual == 1 and self.SPRITES["SPRITE_DROP_RAIO"] is not None:
                                self.lista_drops.append(Drop(i.x, i.y, self.round_atual, sprite=self.SPRITES["SPRITE_DROP_RAIO"]))
                            elif self.round_atual == 2 and self.SPRITES["SPRITE_DROP_HERMES"] is not None:
                                self.lista_drops.append(Drop(i.x, i.y, self.round_atual, sprite=self.SPRITES["SPRITE_DROP_HERMES"]))
                            elif self.round_atual == 3 and self.SPRITES["SPRITE_DROP_CHAVE"] is not None:
                                self.lista_drops.append(Drop(i.x, i.y, self.round_atual, sprite=self.SPRITES["SPRITE_DROP_CHAVE"]))
                            else:
                                self.lista_drops.append(Drop(i.x, i.y, self.round_atual))
                            if self.round_atual < 3:
                                self.round_atual += 1
                                self.alminhas_restantes = 30
                        try:
                            self.lista_inimigos.remove(i)
                        except:
                            pass

                    elif i.indice >= len(self.CAMINHO) - 1:
                        dano = 5 if i.e_boss else 1
                        if i.e_boss:
                            if i.pass_cooldown == 0:
                                self.vidas -= dano
                                i.pass_cooldown = 180
                                self.set_popup("O Chefe feriu o portal!", (150,0,0))
                            i.x, i.y = self.CAMINHO[0]
                            i.indice = 0
                        else:
                            self.vidas -= dano
                            try:
                                self.lista_inimigos.remove(i)
                            except:
                                pass

                for d in self.lista_drops:
                    if not d.coletado:
                        if getattr(d, "sprite", None) is not None:
                            size = 40
                            img = pygame.transform.smoothscale(d.sprite, (size, size))
                            self.tela.blit(img, (d.rect.x, d.rect.y))
                        else:
                            pygame.draw.circle(self.tela, d.cor, d.rect.center, 15)

                for p in list(self.lista_particulas):
                    p.atualizar()
                    p.desenhar(self.tela)
                    if p.vida <= 0:
                        try:
                            self.lista_particulas.remove(p)
                        except:
                            pass

                pygame.draw.rect(self.tela, (30,30,30), (0,550, self.LARGURA, 100))
                info = self.fonte_ui.render(f"Round: {self.round_atual}  Ouro: {self.ouro}  Vidas: {self.vidas}", True, self.BRANCO)
                self.tela.blit(info, (20,570))
                drops_text = self.fonte_ui.render(f"Itens Divinos: {self.drops_coletados}/3", True, self.OURO)
                self.tela.blit(drops_text, (20,600))

                if self.switch_anim_timer > 0:
                    progress = self.switch_anim_timer / float(self.switch_anim_duration)
                    scale = 1.0 + 0.35 * progress
                    self.switch_anim_timer -= dt
                    if self.switch_anim_timer < 0:
                        self.switch_anim_timer = 0
                else:
                    scale = 1.0

                cx = self.LARGURA - 80
                cy = 585
                self.desenhar_icone_deus(cx, cy, self.selecionado, scale)
                raio_base = self.TOWER_RADIO.get(self.selecionado, 20)
                raio = max(6, int(raio_base * scale))
                nome = self.fonte_pequena.render(self.selecionado, True, self.BRANCO)
                self.tela.blit(nome, (cx - nome.get_width()//2, cy + raio + 6))

                if self.vidas <= 0:
                    self.estado_jogo = "DERROTA"

                self.desenhar_popup()

            elif self.estado_jogo == "EPILOGO":
                self.tela.fill((20,20,50))
                msg = self.fonte_titulo.render("ARTEFATO FINAL COLETADO!", True, self.OURO)
                self.tela.blit(msg, (self.LARGURA//2 - msg.get_width()//2, self.ALTURA//2 - 80))
                sub = self.fonte_ui.render("Os Panteões despertam seu poder final...", True, self.BRANCO)
                self.tela.blit(sub, (self.LARGURA//2 - sub.get_width()//2, self.ALTURA//2 - 10))
                info_drops_big = self.fonte_titulo.render(f"{self.drops_coletados} / 3", True, self.OURO)
                self.tela.blit(info_drops_big, (self.LARGURA - info_drops_big.get_width() - 30, 560))
                self.desenhar_popup()
                if self.tempo_epilogo is not None and pygame.time.get_ticks() - self.tempo_epilogo >= 3000:
                    self.estado_jogo = "VITORIA_EPICA"

            elif self.estado_jogo == "VITORIA_EPICA":
                bg = self.SPRITES.get("VITORIA_BG")
                if bg is not None:
                    self.tela.blit(bg, (0,0))
                else:
                    self.tela.fill((10,10,50))
                msg = self.fonte_titulo.render("VITÓRIA DOS PANTEÕES!", True, self.OURO)
                self.tela.blit(msg, (self.LARGURA//2 - msg.get_width()//2, self.ALTURA//2 - 100))
                msg2 = self.fonte_ui.render("VOCÊ SALVOU O UNIVERSO!", True, self.BRANCO)
                self.tela.blit(msg2, (self.LARGURA//2 - msg2.get_width()//2, self.ALTURA//2 - 40))
                btn = pygame.Rect(self.LARGURA//2 - 150, 450, 300, 60)
                pygame.draw.rect(self.tela, self.OURO, btn, 2)
                txt = self.fonte_ui.render("VOLTAR AO MENU", True, self.BRANCO)
                self.tela.blit(txt, (btn.x+60, btn.y+15))
                if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
                    self.estado_jogo = "MENU"

            elif self.estado_jogo == "DERROTA":
                bg = self.SPRITES.get("DERROTA_BG")
                if bg is not None:
                    self.tela.blit(bg, (0,0))
                else:
                    self.tela.fill((40,0,0))
                msg = self.fonte_titulo.render("DERROTA CATASTRÓFICA", True, (255,60,60))
                self.tela.blit(msg, (self.LARGURA//2 - msg.get_width()//2, self.ALTURA//2 - 100))
                msg2 = self.fonte_ui.render("Os demônios dominaram o universo e você não foi capaz de para-los", True, self.BRANCO)
                self.tela.blit(msg2, (self.LARGURA//2 - msg2.get_width()//2, self.ALTURA//2 - 40))
                btn = pygame.Rect(self.LARGURA//2 - 150, 450, 300, 60)
                pygame.draw.rect(self.tela, (255,60,60), btn, 2)
                txt = self.fonte_ui.render("TENTAR NOVAMENTE", True, self.BRANCO)
                self.tela.blit(txt, (btn.x+40, btn.y+15))
                if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
                    self.estado_jogo = "MENU"

            if self.estado_jogo == "EPILOGO" and self.tempo_epilogo is None:
                self.tempo_epilogo = pygame.time.get_ticks()

            pygame.display.flip()

        pygame.quit()