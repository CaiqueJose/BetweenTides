import pygame


class Jogador:
    """Classe do jogador (naufrago)."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocidade = 4
        self.vida = 100
        self.vida_max = 100
        self.dano_cooldown = 0
        self.cooldown_ataque = 0
        self.animacao_ataque = 0
        self.area_ataque = None
        self.direcao = "baixo"

    def receber_dano(self, quantidade):
        if self.dano_cooldown <= 0:
            self.vida -= quantidade
            self.dano_cooldown = 60
            if self.vida < 0:
                self.vida = 0

    def atacar(self):
        if self.cooldown_ataque <= 0:
            self.cooldown_ataque = 40
            self.animacao_ataque = 15
            self.atualizar_area_ataque()
            return self.area_ataque
        return None

    def atualizar_area_ataque(self):
        # Cria um retangulo de ataque na direcao que o jogador esta olhando
        alcance = 55
        largura_ataque = 80
        if self.direcao == "cima":
            self.area_ataque = pygame.Rect(self.rect.centerx - largura_ataque//2, self.rect.top - alcance, largura_ataque, alcance)
        elif self.direcao == "baixo":
            self.area_ataque = pygame.Rect(self.rect.centerx - largura_ataque//2, self.rect.bottom, largura_ataque, alcance)
        elif self.direcao == "esquerda":
            self.area_ataque = pygame.Rect(self.rect.left - alcance, self.rect.centery - largura_ataque//2, alcance, largura_ataque)
        elif self.direcao == "direita":
            self.area_ataque = pygame.Rect(self.rect.right, self.rect.centery - largura_ataque//2, alcance, largura_ataque)

    def atualizar(self, obstaculos, largura, altura, hud_altura=70):
        teclas = pygame.key.get_pressed()

        mov_x = 0
        mov_y = 0

        if teclas[pygame.K_w]:
            mov_y = -self.velocidade
            self.direcao = "cima"
        elif teclas[pygame.K_s]:
            mov_y = self.velocidade
            self.direcao = "baixo"
        elif teclas[pygame.K_a]:
            mov_x = -self.velocidade
            self.direcao = "esquerda"
        elif teclas[pygame.K_d]:
            mov_x = self.velocidade
            self.direcao = "direita"

        # Movimento horizontal com colisao
        self.rect.x += mov_x
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if mov_x > 0:
                    self.rect.right = obs.rect.left
                elif mov_x < 0:
                    self.rect.left = obs.rect.right

        # Movimento vertical com colisao
        self.rect.y += mov_y
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if mov_y > 0:
                    self.rect.bottom = obs.rect.top
                elif mov_y < 0:
                    self.rect.top = obs.rect.bottom

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.top < hud_altura:
            self.rect.top = hud_altura
        if self.rect.bottom > altura:
            self.rect.bottom = altura

        # Cooldown de dano e ataque
        if self.dano_cooldown > 0:
            self.dano_cooldown -= 1
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1
        if self.animacao_ataque > 0:
            self.animacao_ataque -= 1
            self.atualizar_area_ataque()
        else:
            self.area_ataque = None

    def desenhar(self, tela):
        # Piscar quando invencivel
        if self.dano_cooldown > 0 and (self.dano_cooldown // 5) % 2 == 0:
            return

        # Corpo
        pygame.draw.rect(tela, (30, 120, 200), self.rect)
        pygame.draw.rect(tela, (20, 80, 160), self.rect, 2)

        # Olhos (ajustados pela direcao)
        ox1, ox2 = 10, 22
        oy = 10
        if self.direcao == "cima":
            oy = 4
        elif self.direcao == "baixo":
            oy = 16
        elif self.direcao == "esquerda":
            ox1, ox2 = 4, 10
            oy = 12
        elif self.direcao == "direita":
            ox1, ox2 = 22, 28
            oy = 12
            
        olho_y = self.rect.y + oy
        pygame.draw.circle(tela, (255, 255, 255), (self.rect.x + ox1, olho_y), 4)
        pygame.draw.circle(tela, (255, 255, 255), (self.rect.x + ox2, olho_y), 4)
        pygame.draw.circle(tela, (0, 0, 0), (self.rect.x + ox1, olho_y), 2)
        pygame.draw.circle(tela, (0, 0, 0), (self.rect.x + ox2, olho_y), 2)

        # Ataque
        if self.area_ataque and self.animacao_ataque > 0:
            import math
            centro = self.rect.center
            raio = 55
            start_angle = 0
            end_angle = 0
            if self.direcao == "direita":
                start_angle, end_angle = -math.pi/3, math.pi/3
            elif self.direcao == "cima":
                start_angle, end_angle = math.pi/2 - math.pi/3, math.pi/2 + math.pi/3
            elif self.direcao == "esquerda":
                start_angle, end_angle = math.pi - math.pi/3, math.pi + math.pi/3
            elif self.direcao == "baixo":
                start_angle, end_angle = 3*math.pi/2 - math.pi/3, 3*math.pi/2 + math.pi/3
            
            # Draw an arc
            rect_arc = pygame.Rect(centro[0] - raio, centro[1] - raio, raio*2, raio*2)
            pygame.draw.arc(tela, (200, 200, 200), rect_arc, start_angle, end_angle, 4)
            pygame.draw.arc(tela, (255, 255, 255), rect_arc.inflate(-10, -10), start_angle, end_angle, 2)
