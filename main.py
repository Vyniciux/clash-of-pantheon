import os
import pygame
import math
import random

# Inicializa o pygame
pygame.init()

# Dimensões da tela
LARGURA, ALTURA = 900, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Clash of Pantheons: The Gate Guardians")

# Controlador de FPS
relogio = pygame.time.Clock()

# -----------------------------
# CORES E FONTES
# -----------------------------
FUNDO_MENU = (10, 10, 25)  # usado quando não houver menu.png
GRAMA = (34, 139, 34)
ESTRADA = (100, 80, 60)
OURO = (218, 165, 32)
BRANCO = (255, 255, 255)

# Cores usadas para os drops especiais
CORES_DROP = {
    1: (255, 215, 0),   # Drop de Zeus
    2: (0, 255, 255),   # Drop de Hermes
    3: (128, 0, 128)    # Drop final
}

# Fontes usadas na UI
fonte_titulo = pygame.font.SysFont("serif", 60, bold=True)
fonte_ui = pygame.font.SysFont("serif", 24)
fonte_pequena = pygame.font.SysFont("serif", 18, bold=True)

# -----------------------------
# VARIÁVEIS DO JOGO (ESTADO GLOBAL)
# -----------------------------
estado_jogo = "MENU"           # Estados possíveis: MENU, JOGANDO, EPILOGO, VITORIA_EPICA, DERROTA
round_atual = 1                # Round atual
alminhas_restantes = 30        # Quantidade de inimigos normais a spawnar neste round
ouro = 400                     # Moeda para construir torres
vidas = 20                     # Vida do portal

# Multiplicadores vindos de drops
multiplicador_dano = 1.0
multiplicador_vel = 1.0

# Progressão e rastreio de drops
inimigos_mortos_total = 0
nivel_fantasma = 1.0           # Dificuldade escalada
drops_coletados = 0            # Contador: necessário coletar 3 para zerar

# Popups e epilogo
mensagem_popup = None
tempo_epilogo = None           # momento em que epilogo foi iniciado (ms)

# Caminho que os inimigos percorrem (lista de waypoints)
CAMINHO = [
    (0, 300), (250, 300), (250, 100),
    (550, 100), (550, 500), (900, 500)
]

# Dados base para cada deus/tower: custo, alcance, dano, cadência, cor
DADOS_DEUSES = {
    # custo, alcance, dano, cadência, cor
    "Zeus":   [100, 200, 2, 15, (255, 215, 0)],
    "Anubis": [250, 260, 1, 20, (200, 180, 0)],
    # Odin cadência reduzida levemente (mais rápido do que 40)
    "Odin":   [400, 230, 5, 20, (50, 50, 100)]
}

# Raio usado para colisão de construção e margem mínima entre torres
TOWER_RADIO = {"Zeus": 20, "Anubis": 20, "Odin": 24}
MIN_DIST_MARGIN = 8

# Lista de tipos disponíveis para construção / seleção
lista_tipos = ["Zeus", "Anubis", "Odin"]
indice_tipo = 0
selecionado = lista_tipos[indice_tipo]

# Timer para animação ao trocar de deus
switch_anim_timer = 0
switch_anim_duration = 300

# -----------------------------------------------
# SPRITES E ASSETS (assets/)
# -----------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# nomes dos arquivos de sprite (ajuste conforme necessário)
SPRITE_ROUND1_FILENAME = "fantasmaazul.png"
SPRITE_ROUND2_FILENAME = "fantasmalaranja.png"
SPRITE_ROUND3_FILENAME = "fantasmapreto.png"

# sprites das torres/deuses (normal + animado)
SPRITE_ODIN_NORMAL_FILENAME = "odinpadrao.png"
SPRITE_ODIN_ANIM_FILENAME = "odinlanca.png"

SPRITE_ZEUS_NORMAL_FILENAME = "zeuspadrao.png"
SPRITE_ZEUS_ANIM_FILENAME = "zeusanimado.png"

SPRITE_ANUBIS_NORMAL_FILENAME = "anubispadrao.png"
SPRITE_ANUBIS_ANIM_FILENAME = "anubisanimado.png"

# sprites dos drops
SPRITE_DROP_RAIO_FILENAME = "raiomestrezeus.png"   # round 1
SPRITE_DROP_HERMES_FILENAME = "botasdehermes.png" # round 2
SPRITE_DROP_CHAVE_FILENAME = "chave.png"          # round 3

# imagens de tela (menu / vitória / derrota)
MENU_BG_FILENAME = "menu.png"
VITORIA_BG_FILENAME = "vitoria.png"
DERROTA_BG_FILENAME = "derrota.png"

# ---- perfis solicitados (opcional) ----
PERFIL_ZEUS_FILENAME = "zeusperfil.png"
PERFIL_ODIN_FILENAME = "odinperfil.png"
PERFIL_ANUBIS_FILENAME = "anubisperfil.png"

# -------------------
# Boss sprites (novos)
# -------------------
BOSS1_FILENAME = "cerbero.png"        # boss do round 1
BOSS2_FILENAME = "mumia.png"          # boss do round 2
BOSS3_FILENAME = "jormungand.png"     # boss do round 3

# variáveis que armazenam as Surfaces carregadas (ou None)
SPRITE_ROUND1 = None
SPRITE_ROUND2 = None
SPRITE_ROUND3 = None

SPRITE_ODIN_NORMAL = None
SPRITE_ODIN_ANIM = None

SPRITE_ZEUS_NORMAL = None
SPRITE_ZEUS_ANIM = None

SPRITE_ANUBIS_NORMAL = None
SPRITE_ANUBIS_ANIM = None

SPRITE_DROP_RAIO = None
SPRITE_DROP_HERMES = None
SPRITE_DROP_CHAVE = None

# Boss sprite surfaces
SPRITE_BOSS1 = None
SPRITE_BOSS2 = None
SPRITE_BOSS3 = None

MENU_BG = None
VITORIA_BG = None
DERROTA_BG = None

# perfis (dict tipo -> Surface ou None)
PERFIS = {"Zeus": None, "Odin": None, "Anubis": None}

# Escala do Odin (mantive um valor moderado)
ODIN_SCALE = 1.15

def carregar_sprite(nome_arquivo, scale_to_screen=False):
    caminho = os.path.join(ASSETS_DIR, nome_arquivo)
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    img = pygame.image.load(caminho).convert_alpha()
    if scale_to_screen:
        try:
            img = pygame.transform.smoothscale(img, (LARGURA, ALTURA))
        except Exception:
            img = pygame.transform.scale(img, (LARGURA, ALTURA))
    return img

# tenta carregar sprites; em caso de falha, mantêm None (fallback: círculos)
def tentar_carregar(nome, scale_to_screen=False):
    try:
        return carregar_sprite(nome, scale_to_screen=scale_to_screen)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar '{nome}': {e}")
        return None

# carrega assets principais
SPRITE_ROUND1 = tentar_carregar(SPRITE_ROUND1_FILENAME)
SPRITE_ROUND2 = tentar_carregar(SPRITE_ROUND2_FILENAME)
SPRITE_ROUND3 = tentar_carregar(SPRITE_ROUND3_FILENAME)

SPRITE_ODIN_NORMAL = tentar_carregar(SPRITE_ODIN_NORMAL_FILENAME)
SPRITE_ODIN_ANIM = tentar_carregar(SPRITE_ODIN_ANIM_FILENAME)

SPRITE_ZEUS_NORMAL = tentar_carregar(SPRITE_ZEUS_NORMAL_FILENAME)
SPRITE_ZEUS_ANIM = tentar_carregar(SPRITE_ZEUS_ANIM_FILENAME)

SPRITE_ANUBIS_NORMAL = tentar_carregar(SPRITE_ANUBIS_NORMAL_FILENAME)
SPRITE_ANUBIS_ANIM = tentar_carregar(SPRITE_ANUBIS_ANIM_FILENAME)

SPRITE_DROP_RAIO = tentar_carregar(SPRITE_DROP_RAIO_FILENAME)
SPRITE_DROP_HERMES = tentar_carregar(SPRITE_DROP_HERMES_FILENAME)
SPRITE_DROP_CHAVE = tentar_carregar(SPRITE_DROP_CHAVE_FILENAME)

# carregar boss sprites
SPRITE_BOSS1 = tentar_carregar(BOSS1_FILENAME)
SPRITE_BOSS2 = tentar_carregar(BOSS2_FILENAME)
SPRITE_BOSS3 = tentar_carregar(BOSS3_FILENAME)

# carregar backgrounds das telas, escalados para a resolução do jogo
MENU_BG = tentar_carregar(MENU_BG_FILENAME, scale_to_screen=True)
VITORIA_BG = tentar_carregar(VITORIA_BG_FILENAME, scale_to_screen=True)
DERROTA_BG = tentar_carregar(DERROTA_BG_FILENAME, scale_to_screen=True)

# carregar perfis (não escalados aqui; serão redimensionados ao desenhar)
PERFIS["Zeus"] = tentar_carregar(PERFIL_ZEUS_FILENAME)
PERFIS["Odin"] = tentar_carregar(PERFIL_ODIN_FILENAME)
PERFIS["Anubis"] = tentar_carregar(PERFIL_ANUBIS_FILENAME)

# -----------------------------------------------
# UTIL: RECORTE CIRCULAR
# -----------------------------------------------
def circular_crop(surface, size):
    """
    Retorna uma Surface quadrada (size x size) que contém a 'surface'
    recortada em forma circular (transparência fora do círculo).
    """
    # escala a imagem para o tamanho pedido
    try:
        img = pygame.transform.smoothscale(surface, (size, size))
    except Exception:
        img = pygame.transform.scale(surface, (size, size))

    # cria máscara circular (superfície com alpha)
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.circle(mask, (255, 255, 255, 255), (size // 2, size // 2), size // 2)

    # aplica máscara multiplicando alfa (BLEND_RGBA_MULT)
    result = img.copy()
    result.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return result

# -----------------------------------------------
# FUNÇÃO DO RAIO DO ZEUS (efeito visual zig-zag)
# -----------------------------------------------
def desenhar_raio(surface, inicio, fim, cor, segmentos=8, max_offset=18, espessura=3):
    x1, y1 = inicio
    x2, y2 = fim
    pontos = []

    for i in range(segmentos + 1):
        t = i / float(segmentos)
        px = x1 + (x2 - x1) * t
        py = y1 + (y2 - y1) * t
        fator = math.sin(math.pi * t)
        offset = random.uniform(-max_offset, max_offset) * fator
        dx = x2 - x1
        dy = y2 - y1
        comprimento = math.hypot(dx, dy) or 1
        nx = -dy / comprimento
        ny = dx / comprimento
        px += nx * offset
        py += ny * offset
        pontos.append((int(px), int(py)))

    for esp, alpha_mul in ((espessura+3, 0.12), (espessura+1, 0.25), (espessura, 1.0)):
        cor_cam = (
            min(255, int(cor[0] + 80 * alpha_mul)),
            min(255, int(cor[1] + 80 * alpha_mul)),
            min(255, int(cor[2] + 80 * alpha_mul))
        )
        for a, b in zip(pontos[:-1], pontos[1:]):
            pygame.draw.line(surface, cor_cam, a, b, int(esp))

# -----------------------------------------------
# PARTÍCULAS (EFEITO VISUAL QUANDO BOSS MORRE)
# -----------------------------------------------
class Particula:
    def __init__(self, x, y, cor):
        self.x, self.y = x, y
        self.cor = cor
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.vida = 255  # fade-out

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 10

    def desenhar(self, surface):
        if self.vida > 0:
            pygame.draw.circle(surface, self.cor, (int(self.x), int(self.y)), 4)

# -----------------------------------------------
# INIMIGOS
# -----------------------------------------------
class Inimigo:
    def __init__(self, e_boss=False, sprite=None):
        self.x, self.y = CAMINHO[0]
        self.indice = 0
        self.e_boss = e_boss
        self.vida = (10 + (round_atual * 5)) * nivel_fantasma if not e_boss else 150 * round_atual
        self.velocidade = 1.2 if e_boss else 2.0
        self.raio = 25 if e_boss else 12
        self.pass_cooldown = 0
        self.sprite = sprite

    def mover(self):
        if self.indice < len(CAMINHO) - 1:
            alvo = CAMINHO[self.indice + 1]
            dist = math.hypot(alvo[0] - self.x, alvo[1] - self.y)
            if dist > self.velocidade:
                self.x += (alvo[0] - self.x) / dist * self.velocidade
                self.y += (alvo[1] - self.y) / dist * self.velocidade
            else:
                self.indice += 1

# -----------------------------------------------
# TORRES (DEUSES) - agora com sprites anim/normais
# -----------------------------------------------
class Torre:
    def __init__(self, x, y, tipo):
        self.x, self.y = x, y
        self.tipo = tipo
        self.custo, self.alcance, self.dano_base, self.cadencia_base, self.cor = DADOS_DEUSES[tipo]
        self.timer = 0
        self.raio_torre = TOWER_RADIO[tipo]

        # referência a sprites: normal + anim (pode ser None)
        if tipo == "Odin":
            self.sprite_normal = SPRITE_ODIN_NORMAL
            self.sprite_anim = SPRITE_ODIN_ANIM
        elif tipo == "Zeus":
            self.sprite_normal = SPRITE_ZEUS_NORMAL
            self.sprite_anim = SPRITE_ZEUS_ANIM
        elif tipo == "Anubis":
            self.sprite_normal = SPRITE_ANUBIS_NORMAL
            self.sprite_anim = SPRITE_ANUBIS_ANIM
        else:
            self.sprite_normal = None
            self.sprite_anim = None

        # animação de ataque: contador de frames restantes
        self.anim_timer = 0
        self.anim_duration = 12  # frames totais da animação (ajustável)

    def atacar(self, inimigos):
        """
        Decrementa o cooldown todo frame; procura alvo mais próximo; quando atira,
        reinicia cooldown e começar a animação (set anim_timer).
        """
        if self.timer > 0:
            self.timer -= 1

        # procura inimigo mais próximo dentro do alcance
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

        # ataca
        alvo.vida -= self.dano_base * multiplicador_dano
        self.timer = int(self.cadencia_base / multiplicador_vel)

        # dispara efeitos visuais (línea/raio/impact)
        if self.tipo == "Zeus":
            desenhar_raio(tela, (self.x, self.y), (alvo.x, alvo.y), self.cor,
                          segmentos=10, max_offset=22, espessura=3)
        elif self.tipo == "Odin":
            # efeito de impacto pequeno (apenas indicador)
            pygame.draw.circle(tela, (20,20,20), (int(alvo.x - 5), int(alvo.y - 5)), 6)
            pygame.draw.circle(tela, (40,40,40), (int(alvo.x + 5), int(alvo.y + 5)), 6)
        else:
            pygame.draw.line(tela, self.cor, (self.x, self.y), (alvo.x, alvo.y), 3)

        # inicia a animação de ataque
        self.anim_timer = self.anim_duration

# -----------------------------------------------
# DROPS (ITENS DIVINOS)
# -----------------------------------------------
class Drop:
    def __init__(self, x, y, rd, sprite=None):
        self.rect = pygame.Rect(x-20, y-20, 40, 40)
        self.rd = rd
        self.cor = CORES_DROP[rd]
        self.coletado = False
        self.sprite = sprite

# Listas globais do jogo
lista_inimigos = []
lista_torres = []
lista_particulas = []
lista_drops = []
spawn_timer = 0
spawn_count = 0

# -----------------------------------------------
# SISTEMA DE POPUP (MENSAGENS TEMPORÁRIAS)
# -----------------------------------------------
def set_popup(texto, cor):
    global mensagem_popup
    mensagem_popup = (texto, cor, pygame.time.get_ticks())

def desenhar_popup():
    global mensagem_popup
    if mensagem_popup is not None:
        texto, cor, tempo_inicio = mensagem_popup
        if pygame.time.get_ticks() - tempo_inicio > 2000:
            mensagem_popup = None
            return
        txt_render = fonte_ui.render(texto, True, BRANCO)
        fundo = pygame.Surface((txt_render.get_width() + 20, txt_render.get_height() + 10))
        fundo.set_alpha(180)
        fundo.fill(cor)
        tela.blit(fundo, (10, 10))
        tela.blit(txt_render, (20, 15))

# -----------------------------------------------
# CHECAGENS DE CONSTRUÇÃO
# -----------------------------------------------
def esta_no_caminho(x, y):
    raio = 25
    for i in range(len(CAMINHO)-1):
        p1 = CAMINHO[i]
        p2 = CAMINHO[i+1]
        if math.hypot(p1[0]-x, p1[1]-y) < raio: return True
        if math.hypot(p2[0]-x, p2[1]-y) < raio: return True
        if p1[1] == p2[1]:
            if abs(p1[1]-y) < raio and min(p1[0], p2[0]) < x < max(p1[0], p2[0]):
                return True
        if p1[0] == p2[0]:
            if abs(p1[0]-x) < raio and min(p1[1], p2[1]) < y < max(p1[1], p2[1]):
                return True
    return False

def pode_construir_torre(x, y, tipo):
    novo = TOWER_RADIO[tipo]
    for t in lista_torres:
        if math.hypot(t.x - x, t.y - y) <= (t.raio_torre + novo + MIN_DIST_MARGIN):
            return False
    return True

# -----------------------------------------------
# RESET DO JOGO
# -----------------------------------------------
def reset_jogo():
    global round_atual, alminhas_restantes, ouro, vidas
    global multiplicador_dano, multiplicador_vel
    global inimigos_mortos_total, nivel_fantasma
    global drops_coletados, tempo_epilogo, estado_jogo
    global lista_inimigos, lista_torres, lista_particulas, lista_drops
    global spawn_count

    round_atual = 1
    alminhas_restantes = 30
    ouro = 400
    vidas = 20

    multiplicador_dano = 1.0
    multiplicador_vel = 1.0

    inimigos_mortos_total = 0
    nivel_fantasma = 1.0
    drops_coletados = 0

    lista_inimigos.clear()
    lista_torres.clear()
    lista_particulas.clear()
    lista_drops.clear()

    tempo_epilogo = None
    estado_jogo = "JOGANDO"

    spawn_count = 0

# -----------------------------------------------
# ÍCONE DO DEUS ATUAL (pequeno avatar mostrado na UI)
# -----------------------------------------------
def desenhar_icone_deus(cx, cy, tipo, scale=1.0):
    cor = DADOS_DEUSES[tipo][4]
    raio_base = TOWER_RADIO.get(tipo, 20)
    raio = max(6, int(raio_base * scale))

    perfil = PERFIS.get(tipo)

    if perfil is not None:
        size = max(12, int(raio * 2.2))
        perfil_circ = circular_crop(perfil, size)
        tela.blit(perfil_circ, (int(cx - size/2), int(cy - size/2)))
    else:
        pygame.draw.circle(tela, cor, (int(cx), int(cy)), raio)
        pygame.draw.circle(tela, (0,0,0), (int(cx), int(cy)), raio, 2)
        letra = fonte_pequena.render(tipo[0], True, BRANCO)
        tela.blit(letra, (cx - letra.get_width()//2, cy - letra.get_height()//2))

    if tipo == "Zeus":
        pygame.draw.line(tela, BRANCO, (cx - raio//2, cy - 2), (cx + raio//8, cy + raio//3), 2)
        pygame.draw.line(tela, BRANCO, (cx + raio//8, cy + raio//3), (cx - raio//4, cy + raio//3), 2)
    elif tipo == "Odin":
        pygame.draw.circle(tela, (20,20,20), (cx - raio//3, cy - raio//3), max(1, raio//6))
        pygame.draw.circle(tela, (40,40,40), (cx + raio//3, cy - raio//3), max(1, raio//6))

# -----------------------------------------------
# LOOP PRINCIPAL DO JOGO
# -----------------------------------------------
rodando = True
while rodando:

    dt = relogio.tick(60)  # limita a ~60 FPS
    mx, my = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            rodando = False

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if estado_jogo == "MENU":
                if pygame.Rect(300,450,300,60).collidepoint(ev.pos):
                    reset_jogo()

            elif estado_jogo == "JOGANDO":
                coletou_drop = False
                for d in lista_drops[:]:
                    if not d.coletado and d.rect.collidepoint(ev.pos):
                        d.coletado = True
                        drops_coletados += 1
                        coletou_drop = True
                        if d.rd == 1:
                            multiplicador_dano += 0.25
                            set_popup("Raio Mestre de ZEUS coletado!: Dano de ataque aumentado", CORES_DROP[1])
                        elif d.rd == 2:
                            multiplicador_vel += 0.25
                            set_popup("Botas de HERMES coletadas!: Atack speed aumentado", CORES_DROP[2])
                        elif d.rd == 3:
                            set_popup("Chave do Portal coletada!: Agora podemos fechar o portal", CORES_DROP[3])

                if coletou_drop:
                    if drops_coletados >= 3 and estado_jogo != "EPILOGO":
                        tempo_epilogo = pygame.time.get_ticks()
                        estado_jogo = "EPILOGO"
                    pass
                else:
                    custo = DADOS_DEUSES[selecionado][0]
                    if ouro >= custo and my < 550:
                        if esta_no_caminho(mx, my):
                            set_popup("Não pode construir no caminho!", (150,0,0))
                        elif not pode_construir_torre(mx, my, selecionado):
                            set_popup("Torre muito próxima!", (150,0,0))
                        else:
                            lista_torres.append(Torre(mx, my, selecionado))
                            ouro -= custo

        if ev.type == pygame.KEYDOWN and estado_jogo == "JOGANDO":
            mudou = False
            if ev.key == pygame.K_1:
                indice_tipo = 0; mudou = True
            if ev.key == pygame.K_2:
                indice_tipo = 1; mudou = True
            if ev.key == pygame.K_3:
                indice_tipo = 2; mudou = True
            if ev.key == pygame.K_LEFT:
                indice_tipo = (indice_tipo - 1) % 3; mudou = True
            if ev.key == pygame.K_RIGHT:
                indice_tipo = (indice_tipo + 1) % 3; mudou = True
            if mudou:
                selecionado = lista_tipos[indice_tipo]
                switch_anim_timer = switch_anim_duration

    # -----------------------------------------------
    # LÓGICA E RENDER POR ESTADO
    # -----------------------------------------------
    if estado_jogo == "MENU":
        if MENU_BG is not None:
            tela.blit(MENU_BG, (0,0))
        else:
            tela.fill(FUNDO_MENU)
        t = fonte_titulo.render("CLASH OF PANTHEONS", True, OURO)
        tela.blit(t, (100,150))
        btn = pygame.Rect(300,450,300,60)
        pygame.draw.rect(tela, OURO, btn, 2)
        txt = fonte_ui.render("INICIAR DEFESA", True, BRANCO)
        tela.blit(txt, (btn.x+60, btn.y+15))

    elif estado_jogo == "JOGANDO":
        tela.fill(GRAMA)
        pygame.draw.lines(tela, ESTRADA, False, CAMINHO, 50)

        # Spawn
        spawn_timer += 1
        if alminhas_restantes > 0 and spawn_timer > 40:
            if round_atual == 1:
                chosen_sprite = SPRITE_ROUND1
            elif round_atual == 2:
                chosen_sprite = SPRITE_ROUND2
            else:
                chosen_sprite = SPRITE_ROUND3
            lista_inimigos.append(Inimigo(e_boss=False, sprite=chosen_sprite))
            spawn_count += 1
            alminhas_restantes -= 1
            spawn_timer = 0
        elif alminhas_restantes == 0 and len(lista_inimigos) == 0 and round_atual <= 3:
            # spawn do boss com sprite correspondente ao round
            if round_atual == 1:
                boss_sprite = SPRITE_BOSS1
            elif round_atual == 2:
                boss_sprite = SPRITE_BOSS2
            else:
                boss_sprite = SPRITE_BOSS3
            lista_inimigos.append(Inimigo(e_boss=True, sprite=boss_sprite))
            alminhas_restantes = -1

        # Desenhar torres e disparar ataques
        for t in lista_torres:
            # 1) ataque (efeitos são desenhados aqui)
            t.atacar(lista_inimigos)

            # 2) atualizar contador de animação (decrementa por frame)
            if t.anim_timer > 0:
                t.anim_timer -= 1

            # 3) desenhar sprite apropriado (alternância durante anim_timer)
            # calcula tamanho base
            base_size = max(8, int(t.raio_torre * 2))
            if t.tipo == "Odin":
                size = max(8, int(base_size * ODIN_SCALE))
            else:
                size = max(8, int(base_size * 1.10))

            # decide qual sprite mostrar:
            # enquanto anim_timer > 0, alterna rapidamente entre anim e normal para dar "movimento"
            mostrar_anim = False
            if t.anim_timer > 0 and t.sprite_anim is not None:
                # alterna a cada 3 frames: isso cria um piscar anim/normal enquanto anim_timer>0
                mostrar_anim = (t.anim_timer % 6) < 3

            sprite_to_draw = None
            if mostrar_anim and t.sprite_anim is not None:
                sprite_to_draw = t.sprite_anim
            elif t.sprite_normal is not None:
                sprite_to_draw = t.sprite_normal

            if sprite_to_draw is not None:
                try:
                    img = pygame.transform.smoothscale(sprite_to_draw, (size, size))
                except Exception:
                    img = pygame.transform.scale(sprite_to_draw, (size, size))
                tela.blit(img, (int(t.x - size/2), int(t.y - size/2)))
            else:
                pygame.draw.circle(tela, t.cor, (int(t.x), int(t.y)), t.raio_torre)

        # Atualizar inimigos
        for i in lista_inimigos[:]:
            i.mover()

            # agora desenhamos sprite se houver, inclusive para bosses
            if getattr(i, "sprite", None) is not None:
                # bosses tendem a ser maiores; usa raio para escalar
                size = max(8, int(i.raio * 2.4)) if i.e_boss else max(4, int(i.raio * 2))
                try:
                    img = pygame.transform.smoothscale(i.sprite, (size, size))
                except Exception:
                    img = pygame.transform.scale(i.sprite, (size, size))
                tela.blit(img, (int(i.x - size/2), int(i.y - size/2)))
            else:
                cor_i = (200,0,0) if not i.e_boss else (100,0,0)
                pygame.draw.circle(tela, cor_i, (int(i.x), int(i.y)), i.raio)

            if i.vida <= 0:
                if not i.e_boss:
                    ouro += 25
                    inimigos_mortos_total += 1
                    if inimigos_mortos_total % 20 == 0:
                        nivel_fantasma += 0.15
                        set_popup("Fantasmas mais fortes!", (150,0,0))
                else:
                    for _ in range(30):
                        lista_particulas.append(Particula(i.x, i.y, CORES_DROP[round_atual]))
                    if round_atual == 1 and SPRITE_DROP_RAIO is not None:
                        lista_drops.append(Drop(i.x, i.y, round_atual, sprite=SPRITE_DROP_RAIO))
                    elif round_atual == 2 and SPRITE_DROP_HERMES is not None:
                        lista_drops.append(Drop(i.x, i.y, round_atual, sprite=SPRITE_DROP_HERMES))
                    elif round_atual == 3 and SPRITE_DROP_CHAVE is not None:
                        lista_drops.append(Drop(i.x, i.y, round_atual, sprite=SPRITE_DROP_CHAVE))
                    else:
                        lista_drops.append(Drop(i.x, i.y, round_atual))
                    if round_atual < 3:
                        round_atual += 1
                        alminhas_restantes = 30
                lista_inimigos.remove(i)

            elif i.indice >= len(CAMINHO) - 1:
                dano = 5 if i.e_boss else 1
                if i.e_boss:
                    if i.pass_cooldown == 0:
                        vidas -= dano
                        i.pass_cooldown = 180
                        set_popup("O Chefe feriu o portal!", (150,0,0))
                    i.x, i.y = CAMINHO[0]
                    i.indice = 0
                else:
                    vidas -= dano
                    lista_inimigos.remove(i)

        # Desenhar drops (visuais)
        for d in lista_drops:
            if not d.coletado:
                if getattr(d, "sprite", None) is not None:
                    size = 40
                    try:
                        img = pygame.transform.smoothscale(d.sprite, (size, size))
                    except Exception:
                        img = pygame.transform.scale(d.sprite, (size, size))
                    tela.blit(img, (d.rect.x, d.rect.y))
                else:
                    pygame.draw.circle(tela, d.cor, d.rect.center, 15)

        # Atualizar e desenhar partículas
        for p in lista_particulas[:]:
            p.atualizar()
            p.desenhar(tela)
            if p.vida <= 0:
                lista_particulas.remove(p)

        # Barra inferior de UI
        pygame.draw.rect(tela, (30,30,30), (0,550, LARGURA, 100))
        info = fonte_ui.render(f"Round: {round_atual}  Ouro: {ouro}  Vidas: {vidas}", True, BRANCO)
        tela.blit(info, (20,570))
        drops_text = fonte_ui.render(f"Itens Divinos: {drops_coletados}/3", True, OURO)
        tela.blit(drops_text, (20,600))

        # Animação de switch (pulso)
        if switch_anim_timer > 0:
            progress = switch_anim_timer / float(switch_anim_duration)
            scale = 1.0 + 0.35 * progress
            switch_anim_timer -= dt
            if switch_anim_timer < 0:
                switch_anim_timer = 0
        else:
            scale = 1.0

        # Desenhar avatar do deus selecionado e nome
        cx = LARGURA - 80
        cy = 585
        desenhar_icone_deus(cx, cy, selecionado, scale)
        raio_base = TOWER_RADIO.get(selecionado, 20)
        raio = max(6, int(raio_base * scale))
        nome = fonte_pequena.render(selecionado, True, BRANCO)
        tela.blit(nome, (cx - nome.get_width()//2, cy + raio + 6))

        if vidas <= 0:
            estado_jogo = "DERROTA"

        desenhar_popup()

    elif estado_jogo == "EPILOGO":
        tela.fill((20,20,50))
        msg = fonte_titulo.render("ARTEFATO FINAL COLETADO!", True, OURO)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 80))
        sub = fonte_ui.render("Os Panteões despertam seu poder final...", True, BRANCO)
        tela.blit(sub, (LARGURA//2 - sub.get_width()//2, ALTURA//2 - 10))
        info_drops_big = fonte_titulo.render(f"{drops_coletados} / 3", True, OURO)
        tela.blit(info_drops_big, (LARGURA - info_drops_big.get_width() - 30, 560))
        desenhar_popup()
        if tempo_epilogo is not None and pygame.time.get_ticks() - tempo_epilogo >= 3000:
            estado_jogo = "VITORIA_EPICA"

    elif estado_jogo == "VITORIA_EPICA":
        if VITORIA_BG is not None:
            tela.blit(VITORIA_BG, (0,0))
        else:
            tela.fill((10,10,50))
        msg = fonte_titulo.render("VITÓRIA DOS PANTEÕES!", True, OURO)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 100))
        msg2 = fonte_ui.render("VOCÊ SALVOU O UNIVERSO!", True, BRANCO)
        tela.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 - 40))
        btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
        pygame.draw.rect(tela, OURO, btn, 2)
        txt = fonte_ui.render("VOLTAR AO MENU", True, BRANCO)
        tela.blit(txt, (btn.x+60, btn.y+15))
        if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
            estado_jogo = "MENU"

    elif estado_jogo == "DERROTA":
        if DERROTA_BG is not None:
            tela.blit(DERROTA_BG, (0,0))
        else:
            tela.fill((40,0,0))
        msg = fonte_titulo.render("DERROTA CATASTRÓFICA", True, (255,60,60))
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 100))
        msg2 = fonte_ui.render("Os demônios dominaram o universo e você não foi capaz de para-los", True, BRANCO)
        tela.blit(msg2, (LARGURA//2 - msg2.get_width()//2, ALTURA//2 - 40))
        btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
        pygame.draw.rect(tela, (255,60,60), btn, 2)
        txt = fonte_ui.render("TENTAR NOVAMENTE", True, BRANCO)
        tela.blit(txt, (btn.x+40, btn.y+15))
        if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my):
            estado_jogo = "MENU"

    if estado_jogo == "EPILOGO" and tempo_epilogo is None:
        tempo_epilogo = pygame.time.get_ticks()

    pygame.display.flip()

pygame.quit()
