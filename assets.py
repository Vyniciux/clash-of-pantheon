import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def carregar_sprite(nome_arquivo, scale_to_screen=False, largura=900, altura=650):
    caminho = os.path.join(ASSETS_DIR, nome_arquivo)
    if not os.path.isfile(caminho):
        raise FileNotFoundError(caminho)
    img = pygame.image.load(caminho).convert_alpha()
    if scale_to_screen:
        img = pygame.transform.smoothscale(img, (largura, altura))
    return img

def tentar_carregar(nome, scale_to_screen=False, largura=900, altura=650):
    caminho = os.path.join(ASSETS_DIR, nome)
    if not os.path.isfile(caminho):
        return None
    img = pygame.image.load(caminho).convert_alpha()
    if scale_to_screen:
        try:
            img = pygame.transform.smoothscale(img, (largura, altura))
        except:
            img = pygame.transform.scale(img, (largura, altura))
    return img

def carregar_todos_assets():
    SPRITE_ROUND1_FILENAME = "fantasmaazul.png"
    SPRITE_ROUND2_FILENAME = "fantasmalaranja.png"
    SPRITE_ROUND3_FILENAME = "fantasmapreto.png"
    SPRITE_ODIN_NORMAL_FILENAME = "odinpadrao.png"
    SPRITE_ODIN_ANIM_FILENAME = "odinlanca.png"
    SPRITE_ZEUS_NORMAL_FILENAME = "zeuspadrao.png"
    SPRITE_ZEUS_ANIM_FILENAME = "zeusanimado.png"
    SPRITE_ANUBIS_NORMAL_FILENAME = "anubispadrao.png"
    SPRITE_ANUBIS_ANIM_FILENAME = "anubisanimado.png"
    SPRITE_DROP_RAIO_FILENAME = "raiomestrezeus.png"
    SPRITE_DROP_HERMES_FILENAME = "botasdehermes.png"
    SPRITE_DROP_CHAVE_FILENAME = "chave.png"
    MENU_BG_FILENAME = "menu.png"
    VITORIA_BG_FILENAME = "vitoria.png"
    DERROTA_BG_FILENAME = "derrota.png"
    PERFIL_ZEUS_FILENAME = "zeusperfil.png"
    PERFIL_ODIN_FILENAME = "odinperfil.png"
    PERFIL_ANUBIS_FILENAME = "anubisperfil.png"
    BOSS1_FILENAME = "cerbero.png"
    BOSS2_FILENAME = "mumia.png"
    BOSS3_FILENAME = "jormungand.png"

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
    MENU_BG = tentar_carregar(MENU_BG_FILENAME, scale_to_screen=True)
    VITORIA_BG = tentar_carregar(VITORIA_BG_FILENAME, scale_to_screen=True)
    DERROTA_BG = tentar_carregar(DERROTA_BG_FILENAME, scale_to_screen=True)
    PERFIL_ZEUS = tentar_carregar(PERFIL_ZEUS_FILENAME)
    PERFIL_ODIN = tentar_carregar(PERFIL_ODIN_FILENAME)
    PERFIL_ANUBIS = tentar_carregar(PERFIL_ANUBIS_FILENAME)
    SPRITE_BOSS1 = tentar_carregar(BOSS1_FILENAME)
    SPRITE_BOSS2 = tentar_carregar(BOSS2_FILENAME)
    SPRITE_BOSS3 = tentar_carregar(BOSS3_FILENAME)

    SPRITES = {
        "SPRITE_ROUND1": SPRITE_ROUND1,
        "SPRITE_ROUND2": SPRITE_ROUND2,
        "SPRITE_ROUND3": SPRITE_ROUND3,
        "SPRITE_ODIN_NORMAL": SPRITE_ODIN_NORMAL,
        "SPRITE_ODIN_ANIM": SPRITE_ODIN_ANIM,
        "SPRITE_ZEUS_NORMAL": SPRITE_ZEUS_NORMAL,
        "SPRITE_ZEUS_ANIM": SPRITE_ZEUS_ANIM,
        "SPRITE_ANUBIS_NORMAL": SPRITE_ANUBIS_NORMAL,
        "SPRITE_ANUBIS_ANIM": SPRITE_ANUBIS_ANIM,
        "SPRITE_DROP_RAIO": SPRITE_DROP_RAIO,
        "SPRITE_DROP_HERMES": SPRITE_DROP_HERMES,
        "SPRITE_DROP_CHAVE": SPRITE_DROP_CHAVE,
        "MENU_BG": MENU_BG,
        "VITORIA_BG": VITORIA_BG,
        "DERROTA_BG": DERROTA_BG,
        "PERFIS": {"Zeus": PERFIL_ZEUS, "Odin": PERFIL_ODIN, "Anubis": PERFIL_ANUBIS},
        "SPRITE_BOSS1": SPRITE_BOSS1,
        "SPRITE_BOSS2": SPRITE_BOSS2,
        "SPRITE_BOSS3": SPRITE_BOSS3,
        "DADOS_DEUSES_BASE": {
            "Zeus":   [100, 200, 2, 15, (255, 215, 0)],
            "Anubis": [250, 260, 1, 20, (200, 180, 0)],
            "Odin":   [400, 230, 5, 20, (50, 50, 100)]
        },
        "TOWER_RADIO_OVERRIDE": {"Zeus":20,"Anubis":20,"Odin":24}
    }
    return SPRITES