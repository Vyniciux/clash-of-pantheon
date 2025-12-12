import pygame
import math
import random

def circular_crop(surface, size):
    try:
        img = pygame.transform.smoothscale(surface, (size, size))
    except:
        img = pygame.transform.scale(surface, (size, size))
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    mask.fill((0,0,0,0))
    pygame.draw.circle(mask, (255,255,255,255), (size//2, size//2), size//2)
    result = img.copy()
    result.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return result

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

def esta_no_caminho(x, y, CAMINHO, raio_proibido=25):
    for i in range(len(CAMINHO) - 1):
        p1 = CAMINHO[i]
        p2 = CAMINHO[i+1]
        dist_p1 = math.hypot(p1[0] - x, p1[1] - y)
        dist_p2 = math.hypot(p2[0] - x, p2[1] - y)
        if dist_p1 < raio_proibido or dist_p2 < raio_proibido:
            return True
        if p1[1] == p2[1]:
            if abs(p1[1] - y) < raio_proibido:
                if min(p1[0], p2[0]) < x < max(p1[0], p2[0]):
                    return True
        elif p1[0] == p2[0]:
            if abs(p1[0] - x) < raio_proibido:
                if min(p1[1], p2[1]) < y < max(p1[1], p2[1]):
                    return True
    return False

def pode_construir_torre(x, y, tipo, lista_torres, TOWER_RADIO, MIN_DIST_MARGIN):
    novo = TOWER_RADIO[tipo]
    for t in lista_torres:
        if math.hypot(t.x - x, t.y - y) <= (t.raio_torre + novo + MIN_DIST_MARGIN):
            return False
    return True