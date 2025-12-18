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
PRETO = (0, 0, 0)
CINZA = (110, 110, 110)
AMARELO = (255, 215, 0)
CIANO = (0, 255, 255)
ROXO = (128, 0, 128)
AZUL_ESCURO = (10, 10, 50)
CORES_DROP = {1: AMARELO , 2: CIANO , 3: ROXO}

#Configurações das partidas
NUM_LEVELS = 3

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

INIMIGOS_DADOS = {
    # --- ROUND 1: Introdução ---
    "FANTASMA_1": {
        "SPRITE": "SPRITE_ROUND1", 
        "VIDA_BASE": 10,        # Vida baixa, morre com poucos tiros
        "VELOCIDADE": 2.0,      # Velocidade padrão
        "BOSS_FLAG": False
    },
    "BOSS_1": {
        "SPRITE": "SPRITE_BOSS1", 
        "VIDA_BASE": 150,       # Boss precisa aguentar o caminho todo
        "VELOCIDADE": 1.5,      # Bosses costumam ser um pouco mais lentos e pesados
        "BOSS_FLAG": True
    },

    # --- ROUND 2: Aceleração (Inimigos mais rápidos) ---
    "FANTASMA_2": {
        "SPRITE": "SPRITE_ROUND2", 
        "VIDA_BASE": 25,        # Um pouco mais de vida que o anterior
        "VELOCIDADE": 3.0,      # Mais rápido! Jogador precisa de torres de tiro rápido (Zeus)
        "BOSS_FLAG": False
    },
    "BOSS_2": {
        "SPRITE": "SPRITE_BOSS2", 
        "VIDA_BASE": 400,       # Vida escala bastante
        "VELOCIDADE": 2.0,      # O Boss 2 corre na velocidade de um inimigo normal
        "BOSS_FLAG": True
    },

    # --- ROUND 3: O Apocalipse (Tanques de Guerra) ---
    "FANTASMA_3": {
        "SPRITE": "SPRITE_ROUND3", 
        "VIDA_BASE": 60,        # Aguenta muita pancada
        "VELOCIDADE": 1.8,      # Ligeiramente mais lento por ser pesado
        "BOSS_FLAG": False
    },
    "BOSS_3": {
        "SPRITE": "SPRITE_BOSS3", 
        "VIDA_BASE": 1500,      # O Boss Final: Quase imortal
        "VELOCIDADE": 1.0,      # Muito lento, criando tensão enquanto se aproxima do final
        "BOSS_FLAG": True
    }
}

FASE_SCRIPT = [  
    #(Tipo do inimigo, nível, quantidade, drop,  tempo de espera, tempo de espera para a próxima orda)
    [
     
        ("FANTASMA_1", 3, 10, 0, 60, 180), 
        ("FANTASMA_1", 2, 20, 0, 30, 180), 
        ("BOSS_1", 1, 1, 1, 10, 700),
        ("FANTASMA_2", 2, 20, 0, 30, 250), 
        ("BOSS_2", 1, 1, 2, 0, 700),
        ("FANTASMA_1", 3, 20, 0, 40, 180),
        ("FANTASMA_2", 2, 10, 0, 10, 180),  
        ("BOSS_3", 2, 1, 3, 0, 0)
    ],

    [
        ("FANTASMA_1", 2, 15, 0, 30, 200),
        ("FANTASMA_3", 4, 5, 0, 120, 100),
        ("BOSS_1", 2, 1, 1, 0, 300),
        ("FANTASMA_3", 2, 5, 0, 70, 100),
        ("FANTASMA_2", 1, 10, 0, 15, 150),
        ("FANTASMA_3", 2, 5, 0, 70, 100),
        ("BOSS_2", 2, 1, 2, 0, 400),
        ("FANTASMA_1", 3, 20, 0, 15, 100),
        ("FANTASMA_2", 2, 10, 0, 20, 100),
        ("FANTASMA_1", 3, 20, 0, 15, 100),
        ("FANTASMA_1", 4, 40, 0, 5, 100),
        ("BOSS_3", 6, 1, 3, 0, 0)
    ],

[
    ("FANTASMA_1", 1, 15, 0, 60, 120), 
    ("FANTASMA_1", 2, 15, 0, 50, 180), 
    ("FANTASMA_2", 1, 10, 0, 40, 200), 
    ("FANTASMA_3", 1, 5, 0, 80, 150),   
    ("BOSS_1", 3, 1, 1, 0, 600), 
    ("FANTASMA_1", 5, 25, 0, 30, 200),
    ("FANTASMA_2", 4, 15, 0, 25, 150), 
    ("FANTASMA_1", 4, 40, 0, 15, 300),
    ("FANTASMA_3", 2, 8, 0, 70, 100),  
    ("FANTASMA_2", 4, 10, 0, 30, 150),  
    ("BOSS_2", 2, 1, 2, 0, 700),        
    ("FANTASMA_3", 3, 6, 0, 50, 100),
    ("FANTASMA_1", 5, 10, 0, 40, 120), 
    ("FANTASMA_2", 9, 15, 0, 20, 100),  
    ("FANTASMA_3", 4, 5, 0, 60, 50),
    ("FANTASMA_1", 8, 20, 0, 20, 200), 
    ("BOSS_3", 7, 1, 3, 0, 0)           
]

]