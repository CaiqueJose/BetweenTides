import pygame


def mostrar_madeiras(tela, quantidade):

    fonte = pygame.font.Font(None, 32)

    texto = fonte.render(
        f"Madeira: {quantidade}/5",
        True,
        (255, 255, 255)
    )

    tela.blit(texto, (20, 20))