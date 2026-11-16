import pygame
from scripts.sprites import carregar_sprite


class Obstaculo:
    """Obstaculos do cenario (arvores, pedras, paredes, porta)."""

    def __init__(self, x, y, largura, altura, tipo="pedra", cor=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.tipo = tipo

        if cor:
            self.cor = cor
        else:
            cores = {
                "arvore": (20, 100, 20),
                "pedra": (120, 110, 100),
                "parede": (55, 55, 65),
                "porta": (140, 90, 40),
                "armadilha": (60, 60, 60),
            }
            self.cor = cores.get(tipo, (100, 100, 100))

    def desenhar(self, tela):
        nome_sprite = "pedra_obs" if self.tipo == "pedra" else self.tipo
        sprite = carregar_sprite(nome_sprite, self.rect.width, self.rect.height)
        if sprite:
            tela.blit(sprite, self.rect)
            return

        if self.tipo == "arvore":
            # Tronco
            tronco_w = min(14, self.rect.width // 3)
            tronco_h = min(18, self.rect.height // 3)
            tronco = pygame.Rect(
                self.rect.centerx - tronco_w // 2,
                self.rect.bottom - tronco_h,
                tronco_w, tronco_h,
            )
            pygame.draw.rect(tela, (100, 60, 20), tronco)
            # Copa
            raio = min(self.rect.width, self.rect.height) // 2
            centro = (self.rect.centerx, self.rect.centery - 5)
            pygame.draw.circle(tela, self.cor, centro, raio)
            pygame.draw.circle(tela, (10, 70, 10), centro, raio, 2)

        elif self.tipo == "porta":
            pygame.draw.rect(tela, self.cor, self.rect)
            pygame.draw.rect(tela, (100, 60, 20), self.rect, 3)
            # Fechadura
            cx = self.rect.centerx
            cy = self.rect.centery
            pygame.draw.circle(tela, (60, 40, 10), (cx, cy - 3), 5)
            pygame.draw.polygon(tela, (60, 40, 10), [
                (cx - 3, cy + 2), (cx + 3, cy + 2), (cx, cy + 10)
            ])

        elif self.tipo == "armadilha":
            pygame.draw.rect(tela, self.cor, self.rect)
            # Desenha espinhos
            for i in range(3):
                for j in range(3):
                    px = self.rect.x + 5 + i * 10
                    py = self.rect.y + 5 + j * 10
                    pygame.draw.polygon(tela, (150, 150, 150), [
                        (px, py + 8), (px + 8, py + 8), (px + 4, py)
                    ])

        else:
            pygame.draw.rect(tela, self.cor, self.rect)
            borda = (
                max(0, self.cor[0] - 30),
                max(0, self.cor[1] - 30),
                max(0, self.cor[2] - 30),
            )
            pygame.draw.rect(tela, borda, self.rect, 2)
