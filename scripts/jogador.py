import pygame


class Jogador:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 40, 40)

        self.velocidade = 5

    def atualizar(self, largura, altura):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w]:
            self.rect.y -= self.velocidade

        if teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        if teclas[pygame.K_a]:
            self.rect.x -= self.velocidade

        if teclas[pygame.K_d]:
            self.rect.x += self.velocidade

        self.limitar_tela(largura, altura)
    
    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            (200, 100, 50),
            self.rect
        )


    def limitar_tela(self, largura, altura):

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > largura:
            self.rect.right = largura

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > altura:
            self.rect.bottom = altura
