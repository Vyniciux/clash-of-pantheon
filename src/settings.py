# Definições do jogo

ALTURA = 650
LARGURA = 900

# Cores
FUNDO_MENU = (10, 10, 25)
GRAMA = (34, 139, 34)
ESTRADA = (100, 80, 60)
OURO = (218, 165, 32)
OURO_HOVER = (219, 206, 26)
BRANCO = (255, 255, 255)
CINZA = (110, 110, 110)
AMARELO = (255, 215, 0)
CIANO = (0, 255, 255)
ROXO = (128, 0, 128)
CORES_DROP = {1: AMARELO , 2: CIANO , 3: ROXO}

#Configurações das partidas
NUM_LEVELS = 7

CAMINHO = [
    # FASE 1: "A Reta Final" (Simples e direto, bom para tutorial)
    [
        (0, 325), (200, 325), (200, 200), (700, 200), (700, 450), (900, 450)
    ],

    # FASE 2: "O Zig-Zag Clássico" (Cobre bem o centro)
    [
        (0, 500), (150, 500), (150, 100), (450, 100), (450, 500), 
        (750, 500), (750, 100), (900, 100)
    ],

    # FASE 3: "A Ferradura" (Dá a volta pela borda)
    [
        (0, 100), (800, 100), (800, 500), (100, 500), (100, 325), (900, 325)
    ],

    # FASE 4: "A Escadaria" (Muitas curvas curtas)
    [
        (0, 600), (100, 600), (100, 500), (250, 500), (250, 400), 
        (400, 400), (400, 300), (500, 300), (500, 200), (700, 200), 
        (700, 100), (900, 100)
    ],

    # FASE 5: "O Cruzamento" (Parece um X ou Ampulheta)
    [
        (0, 50), (200, 50), (450, 325), (200, 600), (600, 600), 
        (450, 325), (700, 50), (900, 50)
    ],

    # FASE 6: "A Serpente Longa" (Caminho horizontalizado)
    [
        (0, 150), (750, 150), (750, 300), (150, 300), (150, 450), 
        (750, 450), (750, 600), (900, 600)
    ],

    # FASE 7: "O Labirinto dos Deuses" (Complexo e irregular)
    [
        (0, 325), (100, 325), (100, 100), (300, 100), (300, 500), 
        (500, 500), (500, 200), (700, 200), (700, 400), (800, 400), 
        (800, 100), (900, 100)
    ]
]

DADOS_DEUSES = {
    "Zeus":   [100, 200, 2, 15, (255, 215, 0)],
    "Anubis": [250, 260, 1, 20, (200, 180, 0)],
    "Odin":   [400, 230, 5, 20, (50, 50, 100)]
}

TOWER_RADIO = {"Zeus": 20, "Anubis": 20, "Odin": 24}
MIN_DIST_MARGIN = 8
ODIN_SCALE = 1.15