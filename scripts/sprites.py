import os
import pygame

_CACHE = {}
_SPRITES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")

def carregar_sprite(nome, largura=None, altura=None, espelhar_h=False):
    """Carrega um sprite PNG com suporte a transparencia, redimensionamento e cache."""
    chave = (nome, largura, altura, espelhar_h)
    if chave in _CACHE:
        return _CACHE[chave]

    caminho = os.path.join(_SPRITES_DIR, f"{nome}.png")
    if not os.path.exists(caminho):
        return None

    try:
        surf = pygame.image.load(caminho).convert_alpha()
        if espelhar_h:
            surf = pygame.transform.flip(surf, True, False)
        if largura and altura:
            surf = pygame.transform.smoothscale(surf, (largura, altura))
        _CACHE[chave] = surf
        return surf
    except Exception as e:
        print(f"Erro ao carregar sprite {nome}: {e}")
        return None

