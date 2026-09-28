import pygame


CORES_ITENS = {
    "madeira": (139, 90, 43),
    "cipo": (34, 139, 34),
    "pedra": (150, 150, 150),
    "corda": (210, 180, 100),
    "chave": (255, 215, 0),
    "espada": (192, 192, 192),
}


class Item:
    """Itens coletaveis do jogo."""

    def __init__(self, x, y, tipo):
        self.tipo = tipo
        self.coletado = False
        self.rect = pygame.Rect(x, y, 22, 22)
        self.cor = CORES_ITENS.get(tipo, (255, 255, 255))

    def desenhar(self, tela):
        if self.coletado:
            return

        if self.tipo == "madeira":
            pygame.draw.rect(tela, self.cor, self.rect)
            for i in range(3):
                y = self.rect.y + 5 + i * 6
                pygame.draw.line(tela, (100, 60, 20),
                    (self.rect.x + 2, y), (self.rect.right - 2, y), 1)

        elif self.tipo == "cipo":
            pygame.draw.rect(tela, self.cor, self.rect)
            pygame.draw.rect(tela, (20, 100, 20), self.rect, 2)

        elif self.tipo == "pedra":
            centro = self.rect.center
            pygame.draw.circle(tela, self.cor, centro, 11)
            pygame.draw.circle(tela, (100, 100, 100), centro, 11, 2)

        elif self.tipo == "corda":
            pygame.draw.rect(tela, self.cor, self.rect)
            pygame.draw.rect(tela, (180, 150, 70), self.rect, 2)

        elif self.tipo == "chave":
            cx, cy = self.rect.center
            pygame.draw.circle(tela, self.cor, (cx, cy - 4), 7)
            pygame.draw.circle(tela, (200, 170, 0), (cx, cy - 4), 7, 2)
            pygame.draw.rect(tela, self.cor, (cx - 2, cy + 1, 4, 12))
            pygame.draw.rect(tela, self.cor, (cx, cy + 9, 5, 3))

        elif self.tipo == "espada":
            cx, cy = self.rect.center
            pygame.draw.rect(tela, (139, 69, 19), (cx - 2, cy + 2, 4, 8)) # cabo
            pygame.draw.rect(tela, (100, 100, 100), (cx - 6, cy, 12, 2)) # guarda
            pygame.draw.polygon(tela, self.cor, [(cx - 3, cy), (cx + 3, cy), (cx, cy - 12)]) # lamina