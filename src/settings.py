# Definições do jogo

ALTURA = 650
LARGURA = 900

FUNDO_MENU = (10, 10, 25)
 
NUM_LEVELS = 3

GRAMA = (34, 139, 34)
ESTRADA = (100, 80, 60)
OURO = (218, 165, 32)
OURO_HOVER = (219, 206, 26)
BRANCO = (255, 255, 255)
CINZA = (110, 110, 110)
CORES_DROP = {1: (255, 215, 0), 2: (0, 255, 255), 3: (128, 0, 128)}

CAMINHO = [
    [(0, 300), (250, 300), (250, 100),
    (550, 100), (550, 500), (900, 500)]
]

DADOS_DEUSES = {
    "Zeus":   [100, 200, 2, 15, (255, 215, 0)],
    "Anubis": [250, 260, 1, 20, (200, 180, 0)],
    "Odin":   [400, 230, 5, 20, (50, 50, 100)]
}

TOWER_RADIO = {"Zeus": 20, "Anubis": 20, "Odin": 24}
MIN_DIST_MARGIN = 8
ODIN_SCALE = 1.15