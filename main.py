import pygame

# pyrefly: ignore [missing-import]
from scripts.cenas import Cena


pygame.init()

LARGURA = 1000
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Between Tidesw  ")

clock = pygame.time.Clock()

cena_atual = Cena(tela)

rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        cena_atual.eventos(evento)

    cena_atual.atualizar()
    cena_atual.desenhar()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()