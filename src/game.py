import pygame # Importa a biblioteca para criação do jogo
import math   # Importa funções matemáticas (seno, cosseno, hipotenusa)
import random # Importa gerador de números aleatórios (para as partículas)

class Game:

    def __init__(self):
            
        # --- 1. CONFIGURAÇÕES E INICIALIZAÇÃO ---
        pygame.init() # Inicializa todos os módulos do Pygame
        self.LARGURA, self.ALTURA = 900, 650 # Define o tamanho da janela do jogo
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA)) # Cria a janela propriamente dita
        pygame.display.set_caption("Clash of Pantheons: The Gate Guardians") # Define o título da janela
        self.relogio = pygame.time.Clock() # Cria um objeto para controlar o FPS (velocidade do jogo)

        # Definição das Cores (Sistema RGB)
        self.FUNDO_MENU = (10, 10, 25) # Azul escuro quase preto
        self.GRAMA = (34, 139, 34)      # Verde floresta
        self.ESTRADA = (100, 80, 60)    # Marrom para o caminho
        self.OURO = (218, 165, 32)      # Cor dourada para títulos e moedas
        self.BRANCO = (255, 255, 255)   # Branco puro
        self.CORES_DROP = {1: (255, 215, 0), 2: (0, 255, 255), 3: (128, 0, 128)}

        # Cores dos itens que o Boss solta por round
 
        # Definição de Fontes para os textos
        self.fonte_titulo = pygame.font.SysFont("serif", 60, bold=True)
        self.fonte_ui = pygame.font.SysFont("serif", 24)

        # --- 2. DADOS E ESTADOS GLOBAIS ---
        self.estado_jogo = "MENU" # Controla se estamos no MENU, JOGANDO ou VITORIA
        self.round_atual = 1      # Começa no round 1
        self.alminhas_restantes = 30 # Quantos inimigos normais faltam por round
        self.ouro = 400           # Dinheiro inicial para comprar deuses
        self.vidas = 20           # Vidas do portal (se chegar a 0, fim de jogo)
        self.multiplicador_dano = 1.0 # Buff de dano (aumenta ao coletar item do boss 1)
        self.multiplicador_vel = 1.0  # Buff de velocidade (aumenta ao coletar item do boss 2)

        # NOVO: Sistema de Mensagem Temporária
        self.mensagem_popup = None    # Armazena a tupla (texto, cor, tempo_inicio)
        self.DURACAO_POPUP = 120      # Duração da mensagem em frames (2 segundos a 60 FPS)

        # Pontos de destino que o inimigo segue (X, Y)
        self.CAMINHO = [(0, 300), (250, 300), (250, 100), (550, 100), (550, 500), (900, 500)]

        # Atributos dos Deuses: [Custo, Alcance, Dano, Tempo entre tiros, Cor]
        self.DADOS_DEUSES = {
            "Zeus": [100, 100, 2, 15, (0, 200, 255)],
            "Anubis": [250, 200, 1, 20, (200, 180, 0)],
            "Odin": [400, 150, 5, 40, (50, 50, 100)]
        }

        self.lista_inimigos = [] # Guarda alminhas e bosses ativos
        self.lista_torres = []   # Guarda os deuses posicionados
        self.lista_particulas = [] # Guarda os efeitos de explosão
        self.lista_drops = []      # Guarda itens no chão
        self.spawn_timer = 0       # Tempo entre o nascimento de cada inimigo
        self.selecionado = "Zeus"  # Qual deus está selecionado no menu de compra

    def run(self):

        # --- 5. LOOP PRINCIPAL ---
        rodando = True
        while rodando:
            self.relogio.tick(60) # Mantém o jogo a 60 frames por segundo
            mx, my = pygame.mouse.get_pos() # Pega a posição do mouse

            # Escuta o que o jogador faz (cliques e teclado)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: rodando = False # Fecha o jogo no X
                
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_jogo == "MENU":
                        # Se clicar na área do botão iniciar
                        if pygame.Rect(300, 450, 300, 60).collidepoint(ev.pos): self.reset_jogo()
                    
                    elif self.estado_jogo == "JOGANDO":
                        # Lógica de Coleta: Clica no drop para ganhar Buff
                        for d in self.lista_drops:
                            if not d.coletado and d.rect.collidepoint(ev.pos):
                                d.coletado = True
                                if d.rd == 1: 
                                    self.multiplicador_dano += 0.25 
                                    self.set_popup("Dano de Ataque Aumentado!", self.CORES_DROP[1]) # Feedback 1
                                if d.rd == 2: 
                                    self.multiplicador_vel += 0.25 
                                    self.set_popup("Velocidade de Ataque Aumentada!", self.CORES_DROP[2]) # Feedback 2
                                if d.rd == 3: 
                                    self.estado_jogo = "VITORIA_EPICA" 
                                    self.set_popup("Selador de Portal Coletado!", self.CORES_DROP[3]) # Feedback 3 (Vitória)
                        
                        # Lógica de Compra: Coloca deus no mapa
                        custo = self.DADOS_DEUSES[self.selecionado][0]
                        if self.ouro >= custo and my < 550: # Só constrói fora da barra de UI
                            # --- NOVO BLOQUEIO DE CONSTRUÇÃO ---
                            if not self.esta_no_caminho(mx, my): 
                                self.lista_torres.append(Torre(mx, my, self.selecionado, self.DADOS_DEUSES))
                                self.ouro -= custo # Gasta ouro
                            else:
                                print("🚫 Não é permitido construir sobre o caminho dos inimigos!")
                            # --- FIM NOVO BLOQUEIO ---

                # Teclado para trocar de Deus (1, 2, 3)
                if ev.type == pygame.KEYDOWN and self.estado_jogo == "JOGANDO":
                    if ev.key == pygame.K_1: self.selecionado = "Zeus"
                    if ev.key == pygame.K_2: self.selecionado = "Anubis"
                    if ev.key == pygame.K_3: self.selecionado = "Odin"

            # --- DESENHO E PROCESSAMENTO POR ESTADO ---
            
            if self.estado_jogo == "MENU":
                self.tela.fill(self.FUNDO_MENU) # Fundo azul marinho
                t = self.fonte_titulo.render("CLASH OF PANTHEONS", True, self.OURO)
                self.tela.blit(t, (self.LARGURA//2 - 350, 150))
                btn = pygame.Rect(self.LARGURA//2 - 150, 450, 300, 60)
                # Se mouse em cima, borda branca, senão amarela
                pygame.draw.rect(self.tela, self.BRANCO if btn.collidepoint(mx,my) else self.OURO, btn, 2)
                txt = self.fonte_ui.render("INICIAR DEFESA", True, self.BRANCO)
                self.tela.blit(txt, (btn.x + 60, btn.y + 15))

            elif self.estado_jogo == "JOGANDO":
                self.tela.fill(self.GRAMA) # Fundo verde
                pygame.draw.lines(self.tela, self.ESTRADA, False, self.CAMINHO, 50) # Desenha o caminho marrom
                
                # Lógica de Nascimento (Spawn)
                self.spawn_timer += 1
                if self.alminhas_restantes > 0 and self.spawn_timer > 40: # Nasce inimigo a cada 40 frames
                    self.lista_inimigos.append(Inimigo(self.round_atual, self.CAMINHO))
                    self.alminhas_restantes -= 1
                    self.spawn_timer = 0
                elif self.alminhas_restantes == 0 and len(self.lista_inimigos) == 0:
                    # Se acabaram as alminhas, nasce o Boss
                    self.lista_inimigos.append(Inimigo(self.round_atual, self.CAMINHO, e_boss=True))
                    self.alminhas_restantes = -1 # Trava spawn para não repetir

                # Deuses (Torres)
                for t in self.lista_torres:
                    pygame.draw.circle(self.tela, t.cor, (t.x, t.y), 20) # Desenha o Deus
                    t.atacar(self.lista_inimigos, self.tela, self.multiplicador_dano, self.multiplicador_vel) # Faz o deus tentar atirar
                    
                # Inimigos
                for i in self.lista_inimigos[:]:
                    i.mover() # Faz andar
                    cor_i = (200, 0, 0) if not i.e_boss else (100, 0, 0) # Chefe é mais escuro
                    pygame.draw.circle(self.tela, cor_i, (int(i.x), int(i.y)), i.raio)
                    # Se a vida zerar (morreu)
                    if i.vida <= 0:
                        if i.e_boss: # Se for boss, gera explosão e drop
                            for _ in range(30): self.lista_particulas.append(Particula(i.x, i.y, self.CORES_DROP[self.round_atual]))
                            self.lista_drops.append(Drop(i.x, i.y, self.round_atual, self.CORES_DROP))
                            if self.round_atual < 3: self.round_atual += 1; self.alminhas_restantes = 30 # Prepara próximo round
                        self.ouro += 25 # Recompensa em ouro
                        self.lista_inimigos.remove(i)
                    # Se o inimigo chegou no final (atravessou o portal)
                    elif i.indice >= len(self.CAMINHO)-1:
                        self.vidas -= 1; self.lista_inimigos.remove(i)

                # Desenha Drops (Itens no chão)
                for d in self.lista_drops:
                    if not d.coletado: pygame.draw.circle(self.tela, d.cor, d.rect.center, 15)
                # Desenha e Atualiza Partículas da Explosão
                for p in self.lista_particulas[:]:
                    p.atualizar(); p.desenhar(self.tela)
                    if p.vida <= 0: self.lista_particulas.remove(p)

                # Barra de Interface Inferior (UI)
                pygame.draw.rect(self.tela, (30,30,30), (0, 550, self.LARGURA, 100)) # Fundo cinza escuro
                info = f"Round: {self.round_atual} | Ouro: {self.ouro} | Vidas: {self.vidas} | Selec: {self.selecionado}"
                self.tela.blit(self.fonte_ui.render(info, True, self.BRANCO), (20, 570))
                if self.vidas <= 0: self.estado_jogo = "MENU" # Game Over
                
                # --- DESENHA O POPUP ---
                self.desenhar_popup()

            # --- ESTADO DE VITÓRIA PADRÃO (SE POR ALGUM MOTIVO OCORRER) ---
            elif self.estado_jogo == "VITORIA":
                self.tela.fill((0, 50, 0)) # Fundo verde escuro
                msg = self.fonte_titulo.render("PORTAL SELADO!", True, self.OURO)
                self.tela.blit(msg, (self.LARGURA//2 - 250, self.ALTURA//2 - 50))
                self.tela.blit(self.fonte_ui.render("Clique para voltar ao menu", True, self.BRANCO), (320, 400))
                if pygame.mouse.get_pressed()[0]: self.estado_jogo = "MENU" # Volta ao menu se clicar

            # --- NOVO ESTADO DE VITÓRIA ÉPICA (FINAL DO JOGO) ---
            elif self.estado_jogo == "VITORIA_EPICA":
                self.tela.fill((10, 10, 50)) # Fundo azul muito escuro para dar contraste
                
                # Título principal
                msg_titulo = self.fonte_titulo.render("VITÓRIA DOS PANTEÕES!", True, self.OURO)
                self.tela.blit(msg_titulo, (self.LARGURA//2 - msg_titulo.get_width()//2, self.ALTURA//2 - 100))
                
                # Mensagem épica
                msg_sub = self.fonte_ui.render("VOCÊ SALVOU O UNIVERSO!", True, self.BRANCO)
                self.tela.blit(msg_sub, (self.LARGURA//2 - msg_sub.get_width()//2, self.ALTURA//2 - 30))
                
                msg_final = self.fonte_ui.render("O Portal Ancestral está selado.", True, (200, 200, 200))
                self.tela.blit(msg_final, (self.LARGURA//2 - msg_final.get_width()//2, self.ALTURA//2 + 20))

                # Botão/Instrução para voltar
                btn = pygame.Rect(self.LARGURA//2 - 150, 450, 300, 60)
                pygame.draw.rect(self.tela, self.OURO, btn, 2)
                txt = self.fonte_ui.render("VOLTAR AO MENU", True, self.BRANCO)
                self.tela.blit(txt, (btn.x + 60, btn.y + 15))
                
                # Lógica para voltar ao menu
                if pygame.mouse.get_pressed()[0] and btn.collidepoint(mx, my): 
                    self.estado_jogo = "MENU"
                
            pygame.display.flip() # Atualiza a tela com tudo o que desenhamos

        pygame.quit() # Finaliza o Pygame ao sair do loop  tela.fill(GRAMA) # Fundo verde
              
    # NOVO: Função para definir a mensagem
    def set_popup(self, texto, cor):
        mensagem_popup = (texto, cor, pygame.time.get_ticks()) # Guarda texto, cor e tempo atual

    # NOVO: Função para desenhar a mensagem temporária
    def desenhar_popup(self):
        if self.mensagem_popup is not None:
            texto, cor, tempo_inicio = self.mensagem_popup
            
            # Verifica se o tempo limite de exibição foi atingido
            # 1000/60 é o tempo em milissegundos de um frame a 60 FPS
            if pygame.time.get_ticks() - tempo_inicio > self.DURACAO_POPUP * (1000/60):
                mensagem_popup = None
                return

            # Renderiza e desenha a caixa de mensagem
            txt_render = self.fonte_ui.render(texto, True, self.BRANCO)
            
            # Cria um fundo semi-transparente para a mensagem
            fundo = pygame.Surface((txt_render.get_width() + 20, txt_render.get_height() + 10))
            fundo.set_alpha(180) # Transparência
            fundo.fill(cor)      # Cor baseada no buff
            
            # Posição (canto superior esquerdo)
            self.tela.blit(fundo, (10, 10))
            self.tela.blit(txt_render, (20, 15))

    # --- VERIFICAÇÃO DE CAMINHO ---
    def esta_no_caminho(self, x, y):
        """Verifica se as coordenadas (x, y) estão muito perto da estrada (50px de largura)."""
        raio_proibido = 25 
        
        for i in range(len(self.CAMINHO) - 1):
            p1 = self.CAMINHO[i]
            p2 = self.CAMINHO[i+1]
            
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
    def reset_jogo(self):
        self.round_atual = 1
        self.alminhas_restantes = 30
        self.ouro = 400
        self.vidas = 20
        self.multiplicador_dano = 1.0
        self.multiplicador_vel = 1.0
        self.lista_inimigos.clear()
        self.lista_torres.clear()
        self.lista_drops.clear()
        self.estado_jogo = "JOGANDO"

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
    def __init__(self, round_atual=None, CAMINHO=None, e_boss=False):
        self.CAMINHO = CAMINHO
        self.x, self.y = self.CAMINHO[0] # Começa no primeiro ponto do caminho
        self.indice = 0 # Qual ponto do caminho está buscando agora
        self.e_boss = e_boss # Define se é uma alminha ou o Chefe
        # Status mudam se for boss
        self.vida = 150 * round_atual if e_boss else 10 + (round_atual * 5)
        self.velocidade = 1.2 if e_boss else 2.0
        self.raio = 25 if e_boss else 12

    def mover(self):
        if self.indice < len(self.CAMINHO) - 1: # Se não chegou no final
            alvo = self.CAMINHO[self.indice + 1] # Próximo ponto
            dist = math.hypot(alvo[0] - self.x, alvo[1] - self.y) # Distância até o ponto
            if dist > self.velocidade: # Se está longe, continua andando
                self.x += (alvo[0] - self.x) / dist * self.velocidade
                self.y += (alvo[1] - self.y) / dist * self.velocidade
            else: self.indice += 1 # Se chegou perto, foca no próximo ponto

# Deuses que defendem o portalatacar
class Torre:
    def __init__(self, x, y, tipo, DADOS_DEUSES):
        self.x, self.y, self.tipo = x, y, tipo # Posição e quem é o deus
        # Carrega os dados fixos do dicionário DADOS_DEUSES
        self.custo, self.alcance, self.dano_base, self.cadencia_base, self.cor = DADOS_DEUSES[tipo]
        self.timer = 0 # Cronômetro para controlar a velocidade do tiro

    def atacar(self, inimigos, tela, multiplicador_dano, multiplicador_vel):
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
    def __init__(self, x, y, rd, CORES_DROP):
        self.rect = pygame.Rect(x-20, y-20, 40, 40) # Área de clique
        self.rd = rd # De qual round veio
        self.cor = CORES_DROP[rd] # Cor do item
        self.coletado = False # Se o jogador já clicou
