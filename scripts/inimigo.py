import pygame
import math


class Inimigo:
    """Inimigo simples com patrulha e perseguicao."""

    def __init__(self, x, y, patrol_range=100, velocidade=3, dano=10, chase_range=200):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidade = velocidade
        self.start_x = x
        self.patrol_range = patrol_range
        self.direcao = 1
        self.chase_range = chase_range
        self.dano = dano
        self.vida = 20
        self.morto = False
        # Posicao fracionaria para movimento suave
        self.float_x = float(x)
        self.float_y = float(y)

    def receber_dano(self, quantidade):
        self.vida -= quantidade
        if self.vida <= 0:
            self.morto = True

    def atualizar(self, jogador_rect, obstaculos=None):
        if obstaculos is None:
            obstaculos = []

        dx = jogador_rect.centerx - self.rect.centerx
        dy = jogador_rect.centery - self.rect.centery
        distancia = math.sqrt(dx * dx + dy * dy)

        mov_x = 0.0
        mov_y = 0.0

        if distancia < self.chase_range and distancia > 0:
            # Perseguir
            mov_x = self.velocidade * dx / distancia
            mov_y = self.velocidade * dy / distancia
        else:
            # Patrulhar
            mov_x = 1 * self.direcao
            if self.rect.x > self.start_x + self.patrol_range:
                self.direcao = -1
            elif self.rect.x < self.start_x - self.patrol_range:
                self.direcao = 1

        # Acumular movimento fracionario e converter para pixels inteiros
        self.float_x += mov_x
        self.float_y += mov_y
        pixel_mov_x = int(self.float_x) - self.rect.x
        pixel_mov_y = int(self.float_y) - self.rect.y

        # Movimento horizontal com colisao em obstaculos
        self.rect.x += pixel_mov_x
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if pixel_mov_x > 0:
                    self.rect.right = obs.rect.left
                elif pixel_mov_x < 0:
                    self.rect.left = obs.rect.right
                self.float_x = float(self.rect.x)

        # Movimento vertical com colisao em obstaculos
        self.rect.y += pixel_mov_y
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if pixel_mov_y > 0:
                    self.rect.bottom = obs.rect.top
                elif pixel_mov_y < 0:
                    self.rect.top = obs.rect.bottom
                self.float_y = float(self.rect.y)

        # Limitar a tela
        self.rect.clamp_ip(pygame.Rect(0, 70, 1000, 530))
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

    def desenhar(self, tela):
        # Corpo
        pygame.draw.rect(tela, (200, 30, 30), self.rect)
        pygame.draw.rect(tela, (150, 20, 20), self.rect, 2)

        # Olhos
        oy = self.rect.y + 10
        pygame.draw.circle(tela, (255, 255, 0), (self.rect.x + 8, oy), 5)
        pygame.draw.circle(tela, (255, 255, 0), (self.rect.x + 22, oy), 5)
        pygame.draw.circle(tela, (0, 0, 0), (self.rect.x + 8, oy), 2)
        pygame.draw.circle(tela, (0, 0, 0), (self.rect.x + 22, oy), 2)

        # Sobrancelhas
        pygame.draw.line(tela, (0, 0, 0),
            (self.rect.x + 3, oy - 6), (self.rect.x + 12, oy - 3), 2)
        pygame.draw.line(tela, (0, 0, 0),
            (self.rect.x + 27, oy - 6), (self.rect.x + 18, oy - 3), 2)
