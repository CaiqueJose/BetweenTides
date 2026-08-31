import pygame


class Item:

    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.tipo = tipo
        self.coletado = False

    def desenhar(self, tela):
        if not self.coletado:
            pygame.draw.rect(
                tela,
                (120, 70, 30),
                self.rect
            )