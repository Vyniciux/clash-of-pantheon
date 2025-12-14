import pygame
from src.game import *
from src.settings import *
from src.entidades import *

def Menu(game):
    bg = game.SPRITES.get("MENU_BG")
    if bg is not None:
        game.tela.blit(bg, (0,0))
    else:
        game.tela.fill(FUNDO_MENU)
        
    btn_iniciar = pygame.Rect(300, 400, 300, 50)
    btn_descricao = pygame.Rect(300, 470, 300, 50)
    
    btn_creditos = pygame.Rect(300, 540, 140, 50) 
    btn_sair = pygame.Rect(460, 540, 140, 50) 

    pos_mouse = pygame.mouse.get_pos()

    def desenhar_botao(retangulo, texto, cor_normal, cor_hover, fonte, cor_texto=PRETO, cor_borda=PRETO, espessura_borda=3):
        
        # 1. Desenha o Retângulo da Borda (ligeiramente maior)
        retangulo_borda = retangulo.inflate(espessura_borda * 2, espessura_borda * 2) 
        pygame.draw.rect(game.tela, cor_borda, retangulo_borda, 0)
        
        # 2. Desenha o Retângulo Interno 
        cor = cor_hover if retangulo.collidepoint(pos_mouse) else cor_normal
        pygame.draw.rect(game.tela, cor, retangulo, 0)
        

        txt = fonte.render(texto, True, cor_texto)
        game.tela.blit(txt, (retangulo.x + (retangulo.width - txt.get_width()) // 2, retangulo.y + (retangulo.height - txt.get_height()) // 2))

    # Desenho dos Botões
    desenhar_botao(btn_iniciar, "INICIAR DEFESA", OURO, OURO_HOVER, game.fonte_ui)
    desenhar_botao(btn_descricao, "DESCRIÇÃO", OURO, OURO_HOVER, game.fonte_ui)
    
    # Botões pequenos
    desenhar_botao(btn_creditos, "CRÉDITOS", CINZA, (150, 150, 150), game.fonte_pequena) 
    desenhar_botao(btn_sair, "SAIR", (200, 0, 0), (255, 60, 60), game.fonte_pequena) 

    if pygame.mouse.get_pressed()[0]:
        mx, my = pos_mouse
        
        # INICIAR DEFESA 
        if btn_iniciar.collidepoint(mx, my):
            game.reset_jogo() 
            
        # DESCRIÇÃO 
        elif btn_descricao.collidepoint(mx, my):
            game.estado_jogo = "DESCRIÇÃO"
            
        # CRÉDITOS 
        elif btn_creditos.collidepoint(mx, my):
            game.estado_jogo = "CREDITOS"
            
        # SAIR 
        elif btn_sair.collidepoint(mx, my):
            game.rodando = False

def Levels(game):

    bg = game.SPRITES.get("CAMPO")
    if bg is not None:
        game.tela.blit(bg, (0,0))
    else:
        game.tela.fill(FUNDO_MENU)

    pos_mouse = pygame.mouse.get_pos()
    for i in range(NUM_LEVELS):
        btn = game.level_buttons[i]
        if(i > game.last_level):
            pygame.draw.rect(game.tela, CINZA, btn, 0)
        elif btn.collidepoint(pos_mouse):
            pygame.draw.rect(game.tela, OURO_HOVER, btn, 0)
        else:
            pygame.draw.rect(game.tela, OURO, btn, 0)
        txt = game.fonte_titulo.render(str(i+1), True, BRANCO)
        game.tela.blit(txt, (btn.x+45, btn.y+35))
    
def Jogando(game):
    game.tela.fill(GRAMA)
    pygame.draw.lines(game.tela, ESTRADA, False, CAMINHO[game.actual_level], 50)
    dt = game.relogio.tick(60)

    # A fase agora é comandada por uma lista que funciona como um script 
    # dos montros que devem ser espawnados
    game.spawn_timer += 1
    if game.alminhas_restantes > 0 and game.spawn_timer > game.espera:
        game.lista_inimigos.append(Inimigo(game, CAMINHO[game.actual_level], game.inimigo_atual, game.nivel_fantasma))
        game.spawn_count += 1
        game.alminhas_restantes -= 1
        game.spawn_timer = 0
    elif game.spawn_timer > game.espera_orda:
        if(game.round_atual != len(FASE_SCRIPT[game.actual_level])): #Se ainda não acabou
            game.inimigo_atual = FASE_SCRIPT[game.actual_level][game.round_atual][0]
            game.alminhas_restantes = FASE_SCRIPT[game.actual_level][game.round_atual][1]
            game.espera = FASE_SCRIPT[game.actual_level][game.round_atual][2]
            game.espera_orda = FASE_SCRIPT[game.actual_level][game.round_atual][3]
            game.round_atual += 1
        elif (len(game.lista_inimigos) == 0):
            game.estado_jogo = "EPILOGO"

        

    for t in list(game.lista_torres):
        t.atacar(game.lista_inimigos, game.tela, game.multiplicador_dano, game.multiplicador_vel)
        if t.anim_timer > 0:
            t.anim_timer -= 1
        base_size = max(8, int(t.raio_torre * 2))
        if t.tipo == "Odin":
            size = max(8, int(base_size * ODIN_SCALE))
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
            game.tela.blit(img, (int(t.x - size/2), int(t.y - size/2)))
        else:
            pygame.draw.circle(game.tela, t.cor, (int(t.x), int(t.y)), t.raio_torre)

    for i in list(game.lista_inimigos):
        i.mover()
        if getattr(i, "sprite", None) is not None:
            size = max(8, int(i.raio * 2.4)) if i.e_boss else max(4, int(i.raio * 2))
            img = pygame.transform.smoothscale(i.sprite, (size, size))
            game.tela.blit(img, (int(i.x - size/2), int(i.y - size/2)))
        else:
            cor_i = (200,0,0) if not i.e_boss else (100,0,0)
            pygame.draw.circle(game.tela, cor_i, (int(i.x), int(i.y)), i.raio)

        if i.vida <= 0:
            if not i.e_boss:
                game.ouro += 25
                game.inimigos_mortos_total += 1
                if game.inimigos_mortos_total % 20 == 0:
                    game.nivel_fantasma += 0.15
                    game.set_popup("Fantasmas mais fortes!", (150,0,0))
            else:
                for _ in range(30): #Argumento "game.round_atual" foi trocado por 1, no caso o contexto de rounds mudou
                    game.lista_particulas.append(Particula(i.x, i.y, CORES_DROP[1]))
                if game.round_atual == 1 and game.SPRITES["SPRITE_DROP_RAIO"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_RAIO"]))
                elif game.round_atual == 2 and game.SPRITES["SPRITE_DROP_HERMES"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_HERMES"]))
                elif game.round_atual == 3 and game.SPRITES["SPRITE_DROP_CHAVE"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_CHAVE"]))
                else:
                    game.lista_drops.append(Drop(i.x, i.y, 1))
                if game.round_atual < 3:
                    game.round_atual += 1
                    game.alminhas_restantes = 30
            try:
                game.lista_inimigos.remove(i)
            except:
                pass

        elif i.indice >= len(CAMINHO[game.actual_level]) - 1:
            dano = 5 if i.e_boss else 1
            if i.e_boss:
                if i.pass_cooldown == 0:
                    game.vidas -= dano
                    i.pass_cooldown = 180
                    game.set_popup("O Chefe feriu o portal!", (150,0,0))
                i.x, i.y = CAMINHO[game.actual_level][0]
                i.indice = 0
            else:
                game.vidas -= dano
                try:
                    game.lista_inimigos.remove(i)
                except:
                    pass

    for d in game.lista_drops:
        if not d.coletado:
            if getattr(d, "sprite", None) is not None:
                size = 40
                img = pygame.transform.smoothscale(d.sprite, (size, size))
                game.tela.blit(img, (d.rect.x, d.rect.y))
            else:
                pygame.draw.circle(game.tela, d.cor, d.rect.center, 15)

    for p in list(game.lista_particulas):
        p.atualizar()
        p.desenhar(game.tela)
        if p.vida <= 0:
            try:
                game.lista_particulas.remove(p)
            except:
                pass

    pygame.draw.rect(game.tela, (30,30,30), (0,550, LARGURA, 100))
    info = game.fonte_ui.render(f"Round: {game.round_atual}  Ouro: {game.ouro}  Vidas: {game.vidas}", True, BRANCO)
    game.tela.blit(info, (20,570))
    drops_text = game.fonte_ui.render(f"Itens Divinos: {game.drops_coletados}/3", True, OURO)
    game.tela.blit(drops_text, (20,600))
    setas = game.fonte_ui.render("(          )", True, BRANCO)
    game.tela.blit(setas, (767, 580))

    if game.switch_anim_timer > 0:
        progress = game.switch_anim_timer / float(game.switch_anim_duration)
        scale = 1.0 + 0.35 * progress
        game.switch_anim_timer -= dt
        if game.switch_anim_timer < 0:
            game.switch_anim_timer = 0
    else:
        scale = 1.0

    cx = LARGURA - 80
    cy = 585
    game.desenhar_icone_deus(cx, cy, game.selecionado, scale)
    raio_base = TOWER_RADIO.get(game.selecionado, 20)
    raio = max(6, int(raio_base * scale))
    nome = game.fonte_pequena.render(game.selecionado, True, BRANCO)
    game.tela.blit(nome, (cx - nome.get_width()//2, cy + raio + 6))

    if game.vidas <= 0:
        game.estado_jogo = "DERROTA"

    game.desenhar_popup()

def Epilogo(game):
    game.tela.fill((20,20,50))
    msg = game.fonte_titulo.render("ARTEFATO FINAL COLETADO!", True, OURO)
    game.tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 80))
    sub = game.fonte_ui.render("Os Panteões despertam seu poder final...", True, BRANCO)
    game.tela.blit(sub, (LARGURA//2 - sub.get_width()//2, ALTURA//2 - 10))
    info_drops_big = game.fonte_titulo.render(f"{game.drops_coletados} / 3", True, OURO)
    game.tela.blit(info_drops_big, (LARGURA - info_drops_big.get_width() - 30, 560))
    game.desenhar_popup()
    if game.tempo_epilogo is not None and pygame.time.get_ticks() - game.tempo_epilogo >= 3000:
        game.estado_jogo = "VITORIA_EPICA"

def Vitoria_Epica(game):
    bg = game.SPRITES.get("VITORIA_BG")
    if bg is not None:
        game.tela.blit(bg, (0,0))
    else:
        game.tela.fill((10,10,50))
    #msg = game.fonte_titulo.render("VITÓRIA DOS PANTEÕES!", True, OURO)
    #game.tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 100))
    #msg2 = game.fonte_ui.render("VOCÊ SALVOU O UNIVERSO!", True, BRANCO)
    #game.tela.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 - 40))
    btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
    pos_mouse = pygame.mouse.get_pos()
    if btn.collidepoint(pos_mouse):
        pygame.draw.rect(game.tela, OURO_HOVER, btn, 0)
    else:
        pygame.draw.rect(game.tela, OURO, btn, 0)
    txt = game.fonte_ui.render("CONTINUAR", True, BRANCO)
    game.tela.blit(txt, (btn.x+85, btn.y+15))
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
        game.estado_jogo = "LEVEL_MENU"

        if game.actual_level == game.last_level:
           game.last_level += 1 
        game.reset_jogo()

def Derrota(game):
    bg = game.SPRITES.get("DERROTA_BG")
    if bg is not None:
        game.tela.blit(bg, (0,0))
    else:
        game.tela.fill((40,0,0))
    msg = game.fonte_titulo.render("DERROTA CATASTRÓFICA", True, (255,60,60))
    game.tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 100))
    msg2 = game.fonte_ui.render("Os demônios dominaram o universo e você não foi capaz de para-los", True, BRANCO)
    game.tela.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 - 40))
    btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
    pos_mouse = pygame.mouse.get_pos()
    if btn.collidepoint(pos_mouse):
        pygame.draw.rect(game.tela, OURO_HOVER, btn, 0)
    else:
        pygame.draw.rect(game.tela, OURO, btn, 0)

    txt = game.fonte_ui.render("TENTAR NOVAMENTE", True, BRANCO)
    game.tela.blit(txt, (btn.x+40, btn.y+15))
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
        game.estado_jogo = "MENU"

