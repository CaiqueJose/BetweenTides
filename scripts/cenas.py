from scripts.itens import Item
from scripts.interfaces import mostrar_madeiras
import pygame
from scripts.jogador import Jogador


class Cena:

    def __init__(self, tela):

        self.itens = [
            Item(150, 150, "madeira"),
            Item(300, 400, "madeira"),
            Item(500, 180, "madeira"),
            Item(700, 350, "madeira"),
            Item(850, 150, "madeira")
        ]

        self.madeiras = 0

        self.tela = tela

        self.jogador = Jogador(480, 280)

    def eventos(self, evento):
        pass

    def atualizar(self):

        self.jogador.atualizar(1000, 600)

        for item in self.itens:

            if not item.coletado:

                if self.jogador.rect.colliderect(item.rect):

                    item.coletado = True

                    if item.tipo == "madeira":
                        self.madeiras += 1

    def desenhar(self):

        self.tela.fill((50, 150, 200))

        self.jogador.desenhar(self.tela)

        for item in self.itens:
            item.desenhar(self.tela)

        mostrar_madeiras(self.tela, self.madeiras)
            