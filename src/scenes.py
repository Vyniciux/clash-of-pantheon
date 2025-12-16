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
    
    btn_descricao = pygame.Rect(300, 470, 145, 50)
    btn_tutorial = pygame.Rect(455, 470, 145, 50) 
    
    btn_creditos = pygame.Rect(300, 540, 140, 50) 
    btn_sair = pygame.Rect(460, 540, 140, 50) 

    pos_mouse = pygame.mouse.get_pos()

    def desenhar_botao(retangulo, texto, cor_normal, cor_hover, fonte, cor_texto=PRETO, cor_borda=PRETO):
        retangulo_borda = retangulo.inflate(6, 6) 
        pygame.draw.rect(game.tela, cor_borda, retangulo_borda, 0)
        cor = cor_hover if retangulo.collidepoint(pos_mouse) else cor_normal
        pygame.draw.rect(game.tela, cor, retangulo, 0)
        
        # Centralizar texto
        txt = fonte.render(texto, True, cor_texto)
        escala = 1.0
        
        if txt.get_width() > retangulo.width - 10:
            txt = pygame.transform.smoothscale(txt, (int(retangulo.width - 10), int(txt.get_height() * 0.8)))
            
        game.tela.blit(txt, (retangulo.x + (retangulo.width - txt.get_width()) // 2, retangulo.y + (retangulo.height - txt.get_height()) // 2))

    # Botões
    desenhar_botao(btn_iniciar, "INICIAR DEFESA", OURO, OURO_HOVER, game.fonte_ui)
    desenhar_botao(btn_descricao, "DESCRIÇÃO", OURO, OURO_HOVER, game.fonte_pequena)
    desenhar_botao(btn_tutorial, "TUTORIAL", OURO, OURO_HOVER, game.fonte_pequena) 
    desenhar_botao(btn_creditos, "CRÉDITOS", CINZA, (150, 150, 150), game.fonte_pequena) 
    desenhar_botao(btn_sair, "SAIR", (200, 0, 0), (255, 60, 60), game.fonte_pequena) 

    if pygame.mouse.get_pressed()[0]:
        mx, my = pos_mouse
        if btn_iniciar.collidepoint(mx, my):
            if(game.last_level == 0):
                game.estado_jogo = "JOGANDO"
            else:    
                game.estado_jogo = "LEVEL_MENU"

        elif btn_descricao.collidepoint(mx, my):
            game.estado_jogo = "DESCRIÇÃO"
        elif btn_tutorial.collidepoint(mx, my): 
            game.estado_jogo = "TUTORIAL"
            game.tutorial_step = 0 
        elif btn_creditos.collidepoint(mx, my):
            game.estado_jogo = "CREDITOS"
        elif btn_sair.collidepoint(mx, my):
            game.rodando = False

def Descricao(game):
    game.tela.fill((10, 10, 50)) 
    
    # Título
    titulo = "CLASH OF PANTHEONS: THE GATE GUARDIANS"
    msg_titulo = game.fonte_titulo.render(titulo, True, OURO)
    game.tela.blit(msg_titulo, (LARGURA//2 - msg_titulo.get_width()//2, 40))
    
    y_pos = 120
    
    # Subtítulo Sinopse
    sub_sinopse = game.fonte_ui.render("SINOPSE", True, BRANCO)
    pygame.draw.line(game.tela, OURO, (LARGURA//2 - sub_sinopse.get_width()//2, y_pos + sub_sinopse.get_height()), (LARGURA//2 + sub_sinopse.get_width()//2, y_pos + sub_sinopse.get_height()), 2)
    game.tela.blit(sub_sinopse, (LARGURA//2 - sub_sinopse.get_width()//2, y_pos))
    y_pos += 50
    
    linhas_sinopse = [
        "O equilíbrio entre os mundos foi rompido. O Portal Ancestral, única barreira",
        "que separa os mortos dos vivos, está sob ataque de hordas de fantasmas, demônios",
        "e entidades esquecidas. Em um pacto sem precedentes, os grandes Deuses da",
        "mitologia grega, egípcia e nórdica se uniram para guardar a passagem e evitar o apocalipse.",
    ]
    
    for linha in linhas_sinopse:
        txt = game.fonte_pequena.render(linha, True, CINZA)
        game.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, y_pos))
        y_pos += 30

    # --- Mecânica e Progressão ---
    y_pos += 40
    sub_mecanica = game.fonte_ui.render("MECÂNICA E PROGRESSÃO", True, BRANCO)
    pygame.draw.line(game.tela, OURO, (LARGURA//2 - sub_mecanica.get_width()//2, y_pos + sub_mecanica.get_height()), (LARGURA//2 + sub_mecanica.get_width()//2, y_pos + sub_mecanica.get_height()), 2)
    game.tela.blit(sub_mecanica, (LARGURA//2 - sub_mecanica.get_width()//2, y_pos))
    y_pos += 50

    linhas_mecanica = [
        "Jogue em estilo Tower Defense: invoque Deuses ao longo do caminho que leva ao Portal.",
        "Cada divindade (Zeus, Anubis, Odin) tem custos e poderes únicos baseados em suas lendas.",
        "A cada inimigo derrotado,",
        " colete Ouro Divino para invocar novas sentinelas ou aprimorar as existentes.",
        "A sinergia entre os Panteões e o posicionamento são a chave para selar a fenda para sempre.",
    ]
    
    for linha in linhas_mecanica:
        txt = game.fonte_pequena.render(linha, True, CINZA)
        game.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, y_pos))
        y_pos += 30

    # Botão Voltar
    btn = pygame.Rect(LARGURA//2 - 150, 580, 300, 50)
    pos_mouse = pygame.mouse.get_pos()
    
    cor_btn = OURO_HOVER if btn.collidepoint(pos_mouse) else OURO
    espessura_borda = 3
    
    # 1. Borda BRANCA 
    btn_borda = btn.inflate(espessura_borda * 2, espessura_borda * 2) 
    pygame.draw.rect(game.tela, BRANCO, btn_borda, 0)

    # 2. botão interno colorido
    pygame.draw.rect(game.tela, cor_btn, btn, 0)

    txt = game.fonte_ui.render("VOLTAR", True, BRANCO)
    game.tela.blit(txt, (btn.x + (btn.width - txt.get_width()) // 2, btn.y + (btn.height - txt.get_height()) // 2))
    
    # Lógica do clique
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
         game.estado_jogo = "MENU"

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
        game.lista_inimigos.append(Inimigo(game, CAMINHO[game.actual_level], game.script_inimigo[0], game.script_inimigo[1], game.script_inimigo[3]))
        game.spawn_count += 1
        game.alminhas_restantes -= 1
        game.spawn_timer = 0
    elif game.spawn_timer > game.espera_orda and game.drops_coletados == len(game.lista_drops):
        if(game.round_atual != len(FASE_SCRIPT[game.actual_level])): #Se ainda não acabou
            game.script_inimigo = FASE_SCRIPT[game.actual_level][game.round_atual]
            game.alminhas_restantes = FASE_SCRIPT[game.actual_level][game.round_atual][2]
            game.espera = FASE_SCRIPT[game.actual_level][game.round_atual][4]
            game.espera_orda = FASE_SCRIPT[game.actual_level][game.round_atual][5]
            game.spawn_timer = 0
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
                game.ouro += 5
                game.inimigos_mortos_total += 1
                if game.round_atual > len(FASE_SCRIPT[game.actual_level])/2:
                    game.set_popup("Inimigos mais fortes!", (150,0,0))
            else:
                game.ouro += 20
                for _ in range(30): #Argumento "game.round_atual" foi trocado por 1, no caso o contexto de rounds mudou
                    game.lista_particulas.append(Particula(i.x, i.y, CORES_DROP[1]))
                if i.drop == 1 and game.SPRITES["SPRITE_DROP_RAIO"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_RAIO"]))
                elif i.drop == 2 and game.SPRITES["SPRITE_DROP_HERMES"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_HERMES"]))
                elif i.drop == 3 and game.SPRITES["SPRITE_DROP_CHAVE"] is not None:
                    game.lista_drops.append(Drop(i.x, i.y, 1, sprite=game.SPRITES["SPRITE_DROP_CHAVE"]))
                else:
                    game.lista_drops.append(Drop(i.x, i.y, 1))

            try:
                game.lista_inimigos.remove(i)
            except:
                pass

        elif i.indice >= len(CAMINHO[game.actual_level]) - 1:
            dano = 5 if i.e_boss else 1
            if i.e_boss:
                #if i.pass_cooldown == 0: #Nãe entendi
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
    drops_text = game.fonte_ui.render(f"Itens Divinos: {game.drops_coletados}/{game.total_itens}", True, OURO)
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
    info_drops_big = game.fonte_titulo.render(f"{game.drops_coletados} / {game.total_itens}", True, OURO)
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
        game.reset_jogo()

def Creditos(game):
    game.tela.fill((10, 10, 50)) 

    # --- Título ---
    texto_titulo = "OS ARQUITETOS DO DESTINO"
    img_titulo = game.fonte_titulo.render(texto_titulo, True, OURO)
    game.tela.blit(img_titulo, (LARGURA//2 - img_titulo.get_width()//2, 40))

    y_pos = 120

    # --- Seção: Desenvolvedores ---
    sub_devs = game.fonte_ui.render("DESENVOLVEDORES", True, BRANCO)
    # Linha decorativa abaixo do subtítulo
    pygame.draw.line(game.tela, OURO, 
                     (LARGURA//2 - sub_devs.get_width()//2, y_pos + sub_devs.get_height()), 
                     (LARGURA//2 + sub_devs.get_width()//2, y_pos + sub_devs.get_height()), 2)
    game.tela.blit(sub_devs, (LARGURA//2 - sub_devs.get_width()//2, y_pos))
    
    y_pos += 50

    # LISTA DE NOMES
    lista_devs = [
        "Giovanna de Cassia Silva",
        "Leandro Vynicius Ramos da Silva",
        "Pedro Henrique de Souza Bezerra Faustino",
        "Samuel Elias de Souza",        
        "Thales Afonso Dornelas Gomes"
    ]

    for nome in lista_devs:
        txt = game.fonte_pequena.render(nome, True, CINZA)
        game.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, y_pos))
        y_pos += 30

    # --- Seção: Agradecimentos / Recursos ---
    y_pos += 40
    sub_assets = game.fonte_ui.render("AGRADECIMENTOS & ASSETS", True, BRANCO)
    pygame.draw.line(game.tela, OURO, 
                     (LARGURA//2 - sub_assets.get_width()//2, y_pos + sub_assets.get_height()), 
                     (LARGURA//2 + sub_assets.get_width()//2, y_pos + sub_assets.get_height()), 2)
    game.tela.blit(sub_assets, (LARGURA//2 - sub_assets.get_width()//2, y_pos))
    
    y_pos += 50

    lista_assets = [
        "CIn - UFPE",
        "Professore & Monitores",
        "Música: [Fonte dos Áudios]",
        "Engine: Python + Pygame"
    ]

    for item in lista_assets:
        txt = game.fonte_pequena.render(item, True, CINZA)
        game.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, y_pos))
        y_pos += 30

    # --- Botão Voltar ---
    btn = pygame.Rect(LARGURA//2 - 150, 580, 300, 50)
    pos_mouse = pygame.mouse.get_pos()
    
    cor_btn = OURO_HOVER if btn.collidepoint(pos_mouse) else OURO
    
    # Borda Branca
    espessura_borda = 3
    btn_borda = btn.inflate(espessura_borda * 2, espessura_borda * 2) 
    pygame.draw.rect(game.tela, BRANCO, btn_borda, 0)

    # Botão interno
    pygame.draw.rect(game.tela, cor_btn, btn, 0)

    txt_btn = game.fonte_ui.render("VOLTAR AO MENU", True, BRANCO)
    game.tela.blit(txt_btn, (btn.x + (btn.width - txt_btn.get_width()) // 2, 
                             btn.y + (btn.height - txt_btn.get_height()) // 2))
    
    # Lógica do clique
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
         game.estado_jogo = "MENU"

def Tutorial(game):
    # Fundo
    game.tela.fill((10, 10, 50)) 

    # --- Título Principal ---
    titulo = game.fonte_titulo.render("MANUAL DE DEFESA", True, OURO)
    game.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 30))
    
    # Linha divisória horizontal superior
    pygame.draw.line(game.tela, OURO, (50, 85), (LARGURA - 50, 85), 2)

    # --- Configuração das Colunas ---
    coluna1_x = 60
    coluna2_x = 480 # Metade da tela + margem
    y_inicial = 110
    
    # ================= COLUNA 1: BÁSICO =================
    y = y_inicial
    
    # Seção 1: Objetivo
    lbl = game.fonte_ui.render("OBJETIVO", True, BRANCO)
    game.tela.blit(lbl, (coluna1_x, y))
    y += 40
    
    textos_obj = [
        "O Portal Ancestral está sob ataque.",
        "Impedir que inimigos cruzem o caminho.",
        "Se as vidas chegarem a 0, Game Over."
    ]
    for linha in textos_obj:
        txt = game.fonte_pequena.render(f"- {linha}", True, CINZA)
        game.tela.blit(txt, (coluna1_x, y))
        y += 30

    y += 20 # Espaço extra

    # Seção 2: Controles
    lbl = game.fonte_ui.render("CONTROLES", True, BRANCO)
    game.tela.blit(lbl, (coluna1_x, y))
    y += 40
    
    textos_ctrl = [
        "Teclas 1, 2, 3: Selecionar Deus.",
        "Confira a seleção na barra abaixo.",
        "Clique na grama para criar torres.",
        "Clique nos itens para pegar."
    ]
    for linha in textos_ctrl:
        txt = game.fonte_pequena.render(f"- {linha}", True, CINZA)
        game.tela.blit(txt, (coluna1_x, y))
        y += 30

    # ================= COLUNA 2: ESTRATÉGIA =================
    y = y_inicial
    
    # Linha vertical separando colunas
    pygame.draw.line(game.tela, (50, 50, 100), (LARGURA//2, 100), (LARGURA//2, 500), 2)

    # Seção 3: Os Deuses
    lbl = game.fonte_ui.render("OS GUARDIÕES", True, BRANCO)
    game.tela.blit(lbl, (coluna2_x, y))
    y += 40
    
    # Zeus
    game.tela.blit(game.fonte_pequena.render("ZEUS (Tecla 1):", True, (255, 215, 0)), (coluna2_x, y))
    game.tela.blit(game.fonte_pequena.render("Tiro rápido, alvo único.", True, CINZA), (coluna2_x + 180, y))
    y += 30
    
    # Anubis
    game.tela.blit(game.fonte_pequena.render("ANUBIS (Tecla 2):", True, (200, 0, 200)), (coluna2_x, y))
    game.tela.blit(game.fonte_pequena.render("Veneno e lentidão.", True, CINZA), (coluna2_x + 180, y))
    y += 30
    
    # Odin
    game.tela.blit(game.fonte_pequena.render("ODIN (Tecla 3):", True, (0, 150, 255)), (coluna2_x, y))
    game.tela.blit(game.fonte_pequena.render("Corvos de longo alcance.", True, CINZA), (coluna2_x + 180, y))
    y += 45 # Espaço maior

    # Seção 4: Economia
    lbl = game.fonte_ui.render("ECONOMIA", True, BRANCO)
    game.tela.blit(lbl, (coluna2_x, y))
    y += 40
    
    textos_eco = [
        "Inimigos derrotados dão Ouro.",
        "Bosses dão itens raros (clique!).",
        "Gerencie seu ouro com sabedoria."
    ]
    for linha in textos_eco:
        txt = game.fonte_pequena.render(f"- {linha}", True, CINZA)
        game.tela.blit(txt, (coluna2_x, y))
        y += 30

    # --- Botão Voltar ---
    btn_voltar = pygame.Rect(LARGURA//2 - 150, 560, 300, 60)
    pos_mouse = pygame.mouse.get_pos()
    
    # Hover effect
    if btn_voltar.collidepoint(pos_mouse):
        pygame.draw.rect(game.tela, OURO_HOVER, btn_voltar, 0)
    else:
        pygame.draw.rect(game.tela, OURO, btn_voltar, 0)
        
    # Borda branca simples
    pygame.draw.rect(game.tela, BRANCO, btn_voltar, 3)

    txt_btn = game.fonte_ui.render("VOLTAR AO MENU", True, BRANCO)
    game.tela.blit(txt_btn, (btn_voltar.centerx - txt_btn.get_width()//2, btn_voltar.centery - txt_btn.get_height()//2))

    # --- Lógica de Clique ---
    if pygame.mouse.get_pressed()[0]:
        mx, my = pos_mouse
        
        # Verifica cooldown
        if not hasattr(game, 'click_cooldown') or game.click_cooldown == 0:
            if btn_voltar.collidepoint(mx, my):
                game.estado_jogo = "MENU"
                game.click_cooldown = 15

    # Atualiza cooldown
    if hasattr(game, 'click_cooldown') and game.click_cooldown > 0:
        game.click_cooldown -= 1