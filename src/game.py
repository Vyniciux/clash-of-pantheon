import pygame # Importa a biblioteca para criação do jogo
import math   # Importa funções matemáticas (seno, cosseno, hipotenusa)
import random # Importa gerador de números aleatórios (para as partículas)

# --- 1. CONFIGURAÇÕES E INICIALIZAÇÃO ---
pygame.init() # Inicializa todos os módulos do Pygame
LARGURA, ALTURA = 900, 650 # Define o tamanho da janela do jogo
tela = pygame.display.set_mode((LARGURA, ALTURA)) # Cria a janela propriamente dita
pygame.display.set_caption("Clash of Pantheons: The Gate Guardians") # Define o título da janela
relogio = pygame.time.Clock() # Cria um objeto para controlar o FPS (velocidade do jogo)

# Definição das Cores (Sistema RGB)
FUNDO_MENU = (10, 10, 25) # Azul escuro quase preto
GRAMA = (34, 139, 34)      # Verde floresta
ESTRADA = (100, 80, 60)    # Marrom para o caminho
OURO = (218, 165, 32)      # Cor dourada para títulos e moedas
BRANCO = (255, 255, 255)   # Branco puro
# Cores dos itens que o Boss solta por round
CORES_DROP = {1: (255, 215, 0), 2: (0, 255, 255), 3: (128, 0, 128)}

# Definição de Fontes para os textos
fonte_titulo = pygame.font.SysFont("serif", 60, bold=True)
fonte_ui = pygame.font.SysFont("serif", 24)

# --- 2. DADOS E ESTADOS GLOBAIS ---
estado_jogo = "MENU" # Controla se estamos no MENU, JOGANDO ou VITORIA
round_atual = 1      # Começa no round 1
alminhas_restantes = 30 # Quantos inimigos normais faltam por round
ouro = 400           # Dinheiro inicial para comprar deuses
vidas = 20           # Vidas do portal (se chegar a 0, fim de jogo)
multiplicador_dano = 1.0 # Buff de dano (aumenta ao coletar item do boss 1)
multiplicador_vel = 1.0  # Buff de velocidade (aumenta ao coletar item do boss 2)

# NOVO: Sistema de Mensagem Temporária
mensagem_popup = None    # Armazena a tupla (texto, cor, tempo_inicio)
DURACAO_POPUP = 120      # Duração da mensagem em frames (2 segundos a 60 FPS)

# Pontos de destino que o inimigo segue (X, Y)
CAMINHO = [(0, 300), (250, 300), (250, 100), (550, 100), (550, 500), (900, 500)]

# Atributos dos Deuses: [Custo, Alcance, Dano, Tempo entre tiros, Cor]
DADOS_DEUSES = {
    "Zeus": [100, 100, 2, 15, (0, 200, 255)],
    "Anubis": [250, 200, 1, 20, (200, 180, 0)],
    "Odin": [400, 150, 5, 40, (50, 50, 100)]
}

# --- 3. CLASSES ---

# Partícula visual para a explosão divina quando o Boss morre
class Particula:
    def __init__(self, x, y, cor):
        self.x, self.y = x, y # Posição inicial
        self.cor = cor # Cor baseada no round
        self.vx, self.vy = random.uniform(-4, 4), random.uniform(-4, 4) # Velocidade aleatória para os lados
        self.vida = 255 # Opacidade inicial (brilho)
    def atualizar(self):
        self.x += self.vx # Move em X
        self.y += self.vy # Move em Y
        self.vida -= 10   # Vai sumindo aos poucos
    def desenhar(self, surface):
        if self.vida > 0: # Desenha apenas se ainda for visível
            pygame.draw.circle(surface, self.cor, (int(self.x), int(self.y)), 4)

# Criaturas que tentam invadir o portal
class Inimigo:
    def __init__(self, e_boss=False):
        self.x, self.y = CAMINHO[0] # Começa no primeiro ponto do caminho
        self.indice = 0 # Qual ponto do caminho está buscando agora
        self.e_boss = e_boss # Define se é uma alminha ou o Chefe
        # Status mudam se for boss
        self.vida = 150 * round_atual if e_boss else 10 + (round_atual * 5)
        self.velocidade = 1.2 if e_boss else 2.0
        self.raio = 25 if e_boss else 12

    def mover(self):
        if self.indice < len(CAMINHO) - 1: # Se não chegou no final
            alvo = CAMINHO[self.indice + 1] # Próximo ponto
            dist = math.hypot(alvo[0] - self.x, alvo[1] - self.y) # Distância até o ponto
            if dist > self.velocidade: # Se está longe, continua andando
                self.x += (alvo[0] - self.x) / dist * self.velocidade
                self.y += (alvo[1] - self.y) / dist * self.velocidade
            else: self.indice += 1 # Se chegou perto, foca no próximo ponto

# Deuses que defendem o portal
class Torre:
    def __init__(self, x, y, tipo):
        self.x, self.y, self.tipo = x, y, tipo # Posição e quem é o deus
        # Carrega os dados fixos do dicionário DADOS_DEUSES
        self.custo, self.alcance, self.dano_base, self.cadencia_base, self.cor = DADOS_DEUSES[tipo]
        self.timer = 0 # Cronômetro para controlar a velocidade do tiro

    def atacar(self, inimigos):
        if self.timer > 0: self.timer -= 1 # Espera para poder atirar de novo
        else:
            for i in inimigos: # Procura inimigos no mapa
                # Calcula distância usando Pitágoras
                if math.hypot(i.x - self.x, i.y - self.y) <= self.alcance:
                    i.vida -= self.dano_base * multiplicador_dano # Tira vida (com buff)
                    self.timer = self.cadencia_base / multiplicador_vel # Reinicia espera (com buff)
                    
                    # Desenha o ataque (Visual do deus)
                    if self.tipo == "Odin":
                         # Visual dos corvos Huginn e Muninn
                        pygame.draw.circle(tela, (20, 20, 20), (int(i.x - 5), int(i.y - 5)), 6)
                        pygame.draw.circle(tela, (40, 40, 40), (int(i.x + 5), int(i.y + 5)), 6)
                        pygame.draw.line(tela, (0, 0, 0), (self.x, self.y), (i.x, i.y), 1)
                    else:
                        # Ataque padrão (Raio/Magia)
                        pygame.draw.line(tela, self.cor, (self.x, self.y), (i.x, i.y), 3)
                        
                    break # Ataca apenas um por vez

# Itens que o Boss deixa no chão ao morrer
class Drop:
    def __init__(self, x, y, rd):
        self.rect = pygame.Rect(x-20, y-20, 40, 40) # Área de clique
        self.rd = rd # De qual round veio
        self.cor = CORES_DROP[rd] # Cor do item
        self.coletado = False # Se o jogador já clicou

# --- 4. FUNÇÕES DE SUPORTE ---

lista_inimigos = [] # Guarda alminhas e bosses ativos
lista_torres = []   # Guarda os deuses posicionados
lista_particulas = [] # Guarda os efeitos de explosão
lista_drops = []      # Guarda itens no chão
spawn_timer = 0       # Tempo entre o nascimento de cada inimigo
selecionado = "Zeus"  # Qual deus está selecionado no menu de compra

# NOVO: Função para definir a mensagem
def set_popup(texto, cor):
    global mensagem_popup
    mensagem_popup = (texto, cor, pygame.time.get_ticks()) # Guarda texto, cor e tempo atual

# NOVO: Função para desenhar a mensagem temporária
def desenhar_popup():
    global mensagem_popup
    if mensagem_popup is not None:
        texto, cor, tempo_inicio = mensagem_popup
        
        # Verifica se o tempo limite de exibição foi atingido
        # 1000/60 é o tempo em milissegundos de um frame a 60 FPS
        if pygame.time.get_ticks() - tempo_inicio > DURACAO_POPUP * (1000/60):
            mensagem_popup = None
            return

        # Renderiza e desenha a caixa de mensagem
        txt_render = fonte_ui.render(texto, True, BRANCO)
        
        # Cria um fundo semi-transparente para a mensagem
        fundo = pygame.Surface((txt_render.get_width() + 20, txt_render.get_height() + 10))
        fundo.set_alpha(180) # Transparência
        fundo.fill(cor)      # Cor baseada no buff
        
        # Posição (canto superior esquerdo)
        tela.blit(fundo, (10, 10))
        tela.blit(txt_render, (20, 15))


# --- VERIFICAÇÃO DE CAMINHO ---
def esta_no_caminho(x, y):
    """Verifica se as coordenadas (x, y) estão muito perto da estrada (50px de largura)."""
    raio_proibido = 25 
    
    for i in range(len(CAMINHO) - 1):
        p1 = CAMINHO[i]
        p2 = CAMINHO[i+1]
        
        # 1. Checagem dos Pontos de Virada (Círculos)
        dist_p1 = math.hypot(p1[0] - x, p1[1] - y)
        dist_p2 = math.hypot(p2[0] - x, p2[1] - y)
        if dist_p1 < raio_proibido or dist_p2 < raio_proibido:
            return True

        # 2. Checagem dos Segmentos de Linha (Retângulos)
        
        # Segmento horizontal
        if p1[1] == p2[1]:
            if abs(p1[1] - y) < raio_proibido:
                if min(p1[0], p2[0]) < x < max(p1[0], p2[0]):
                    return True
        
        # Segmento vertical
        elif p1[0] == p2[0]:
            if abs(p1[0] - x) < raio_proibido:
                if min(p1[1], p2[1]) < y < max(p1[1], p2[1]):
                    return True
        
    return False

# Reseta todas as variáveis para começar um jogo novo
def reset_jogo():
    global round_atual, alminhas_restantes, ouro, vidas, multiplicador_dano, multiplicador_vel, estado_jogo
    round_atual = 1; alminhas_restantes = 30; ouro = 400; vidas = 20
    multiplicador_dano = 1.0; multiplicador_vel = 1.0
    lista_inimigos.clear(); lista_torres.clear(); lista_drops.clear()
    estado_jogo = "JOGANDO"

# --- 5. LOOP PRINCIPAL ---

rodando = True
while rodando:
    relogio.tick(60) # Mantém o jogo a 60 frames por segundo
    mx, my = pygame.mouse.get_pos() # Pega a posição do mouse

    # Escuta o que o jogador faz (cliques e teclado)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: rodando = False # Fecha o jogo no X
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if estado_jogo == "MENU":
                # Se clicar na área do botão iniciar
                if pygame.Rect(300, 450, 300, 60).collidepoint(ev.pos): reset_jogo()
            
            elif estado_jogo == "JOGANDO":
                # Lógica de Coleta: Clica no drop para ganhar Buff
                for d in lista_drops:
                    if not d.coletado and d.rect.collidepoint(ev.pos):
                        d.coletado = True
                        if d.rd == 1: 
                            multiplicador_dano += 0.25 
                            set_popup("Dano de Ataque Aumentado!", CORES_DROP[1]) # Feedback 1
                        if d.rd == 2: 
                            multiplicador_vel += 0.25 
                            set_popup("Velocidade de Ataque Aumentada!", CORES_DROP[2]) # Feedback 2
                        if d.rd == 3: 
                            estado_jogo = "VITORIA_EPICA" 
                            set_popup("Selador de Portal Coletado!", CORES_DROP[3]) # Feedback 3 (Vitória)
                
                # Lógica de Compra: Coloca deus no mapa
                custo = DADOS_DEUSES[selecionado][0]
                if ouro >= custo and my < 550: # Só constrói fora da barra de UI
                    # --- NOVO BLOQUEIO DE CONSTRUÇÃO ---
                    if not esta_no_caminho(mx, my): 
                        lista_torres.append(Torre(mx, my, selecionado))
                        ouro -= custo # Gasta ouro
                    else:
                        print("🚫 Não é permitido construir sobre o caminho dos inimigos!")
                    # --- FIM NOVO BLOQUEIO ---

        # Teclado para trocar de Deus (1, 2, 3)
        if ev.type == pygame.KEYDOWN and estado_jogo == "JOGANDO":
            if ev.key == pygame.K_1: selecionado = "Zeus"
            if ev.key == pygame.K_2: selecionado = "Anubis"
            if ev.key == pygame.K_3: selecionado = "Odin"

    # --- DESENHO E PROCESSAMENTO POR ESTADO ---
    
    if estado_jogo == "MENU":
        tela.fill(FUNDO_MENU) # Fundo azul marinho
        t = fonte_titulo.render("CLASH OF PANTHEONS", True, OURO)
        tela.blit(t, (LARGURA//2 - 350, 150))
        btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
        # Se mouse em cima, borda branca, senão amarela
        pygame.draw.rect(tela, BRANCO if btn.collidepoint(mx,my) else OURO, btn, 2)
        txt = fonte_ui.render("INICIAR DEFESA", True, BRANCO)
        tela.blit(txt, (btn.x + 60, btn.y + 15))

    elif estado_jogo == "JOGANDO":
        tela.fill(GRAMA) # Fundo verde
        pygame.draw.lines(tela, ESTRADA, False, CAMINHO, 50) # Desenha o caminho marrom
        
        # Lógica de Nascimento (Spawn)
        spawn_timer += 1
        if alminhas_restantes > 0 and spawn_timer > 40: # Nasce inimigo a cada 40 frames
            lista_inimigos.append(Inimigo())
            alminhas_restantes -= 1
            spawn_timer = 0
        elif alminhas_restantes == 0 and len(lista_inimigos) == 0:
            # Se acabaram as alminhas, nasce o Boss
            lista_inimigos.append(Inimigo(e_boss=True))
            alminhas_restantes = -1 # Trava spawn para não repetir

        # Deuses (Torres)
        for t in lista_torres:
            pygame.draw.circle(tela, t.cor, (t.x, t.y), 20) # Desenha o Deus
            t.atacar(lista_inimigos) # Faz o deus tentar atirar
            
        # Inimigos
        for i in lista_inimigos[:]:
            i.mover() # Faz andar
            cor_i = (200, 0, 0) if not i.e_boss else (100, 0, 0) # Chefe é mais escuro
            pygame.draw.circle(tela, cor_i, (int(i.x), int(i.y)), i.raio)
            # Se a vida zerar (morreu)
            if i.vida <= 0:
                if i.e_boss: # Se for boss, gera explosão e drop
                    for _ in range(30): lista_particulas.append(Particula(i.x, i.y, CORES_DROP[round_atual]))
                    lista_drops.append(Drop(i.x, i.y, round_atual))
                    if round_atual < 3: round_atual += 1; alminhas_restantes = 30 # Prepara próximo round
                ouro += 25 # Recompensa em ouro
                lista_inimigos.remove(i)
            # Se o inimigo chegou no final (atravessou o portal)
            elif i.indice >= len(CAMINHO)-1:
                vidas -= 1; lista_inimigos.remove(i)

        # Desenha Drops (Itens no chão)
        for d in lista_drops:
            if not d.coletado: pygame.draw.circle(tela, d.cor, d.rect.center, 15)
        # Desenha e Atualiza Partículas da Explosão
        for p in lista_particulas[:]:
            p.atualizar(); p.desenhar(tela)
            if p.vida <= 0: lista_particulas.remove(p)

        # Barra de Interface Inferior (UI)
        pygame.draw.rect(tela, (30,30,30), (0, 550, LARGURA, 100)) # Fundo cinza escuro
        info = f"Round: {round_atual} | Ouro: {ouro} | Vidas: {vidas} | Selec: {selecionado}"
        tela.blit(fonte_ui.render(info, True, BRANCO), (20, 570))
        if vidas <= 0: estado_jogo = "MENU" # Game Over
        
        # --- DESENHA O POPUP ---
        desenhar_popup()

    # --- ESTADO DE VITÓRIA PADRÃO (SE POR ALGUM MOTIVO OCORRER) ---
    elif estado_jogo == "VITORIA":
        tela.fill((0, 50, 0)) # Fundo verde escuro
        msg = fonte_titulo.render("PORTAL SELADO!", True, OURO)
        tela.blit(msg, (LARGURA//2 - 250, ALTURA//2 - 50))
        tela.blit(fonte_ui.render("Clique para voltar ao menu", True, BRANCO), (320, 400))
        if pygame.mouse.get_pressed()[0]: estado_jogo = "MENU" # Volta ao menu se clicar

    # --- NOVO ESTADO DE VITÓRIA ÉPICA (FINAL DO JOGO) ---
    elif estado_jogo == "VITORIA_EPICA":
        tela.fill((10, 10, 50)) # Fundo azul muito escuro para dar contraste
        
        # Título principal
        msg_titulo = fonte_titulo.render("VITÓRIA DOS PANTEÕES!", True, OURO)
        tela.blit(msg_titulo, (LARGURA//2 - msg_titulo.get_width()//2, ALTURA//2 - 100))
        
        # Mensagem épica
        msg_sub = fonte_ui.render("VOCÊ SALVOU O UNIVERSO!", True, BRANCO)
        tela.blit(msg_sub, (LARGURA//2 - msg_sub.get_width()//2, ALTURA//2 - 30))
        
        msg_final = fonte_ui.render("O Portal Ancestral está selado.", True, (200, 200, 200))
        tela.blit(msg_final, (LARGURA//2 - msg_final.get_width()//2, ALTURA//2 + 20))

        # Botão/Instrução para voltar
        btn = pygame.Rect(LARGURA//2 - 150, 450, 300, 60)
        pygame.draw.rect(tela, OURO, btn, 2)
        txt = fonte_ui.render("VOLTAR AO MENU", True, BRANCO)
        tela.blit(txt, (btn.x + 60, btn.y + 15))
        
        # Lógica para voltar ao menu
        if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my): 
            estado_jogo = "MENU"
        
    pygame.display.flip() # Atualiza a tela com tudo o que desenhamos

pygame.quit() # Finaliza o Pygame ao sair do loop