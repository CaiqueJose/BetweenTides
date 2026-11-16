import pygame
import math
import random
from scripts.jogador import Jogador
from scripts.obstaculo import Obstaculo
from scripts.itens import Item
from scripts.inimigo import (
    Inimigo, Tubarao, EspectroTempestade, TentaculoLeviata, LeviataChefe
)


class Cena:
    """Classe base para todas as cenas/niveis."""

    def __init__(self, tela, inventario, mensagens):
        self.tela = tela
        self.inventario = inventario
        self.mensagens = mensagens
        self.jogador = None
        self.obstaculos = []
        self.itens = []
        self.inimigos = []
        self.saida = None
        self.saida_liberada = False
        self.objetivo_concluido = False
        self.concluido = False
        self.voltou = False
        self.nivel = 0
        self.objetivo_texto = ""
        self.entrada = None

    def verificar_objetivo(self):
        pass

    def get_progresso(self):
        return ""

    def atualizar(self):
        self.jogador.atualizar(self.obstaculos, 1000, 600, 70)

        # Coleta de itens
        for item in self.itens:
            if not item.coletado and self.jogador.rect.colliderect(item.rect):
                item.coletado = True
                self.inventario.adicionar(item.tipo)
                
                # Pontuacao
                pontos = 50 if item.tipo in ["espada", "chave"] else 10
                self.inventario.pontuacao += pontos
                
                nomes = {
                    "madeira": "Madeira coletada! (+10)",
                    "cipo": "Cipo coletado! (+10)",
                    "pedra": "Pedra coletada! (+10)",
                    "corda": "Corda encontrada! (+10)",
                    "chave": "Voce encontrou uma chave! (+50)",
                    "espada": "Voce pegou a espada! (+50)",
                }
                self.mensagens.adicionar(nomes.get(item.tipo, f"Item coletado! (+{pontos})"))

        # Inimigos
        for inimigo in self.inimigos[:]:
            if inimigo.morto:
                self.inimigos.remove(inimigo)
                continue

            inimigo.atualizar(self.jogador.rect, self.obstaculos)
            if self.jogador.rect.colliderect(inimigo.rect):
                vida_antes = self.jogador.vida
                self.jogador.receber_dano(inimigo.dano)
                if self.jogador.vida < vida_antes:
                    self.mensagens.adicionar("Dano recebido!", 40, (255, 80, 80))

        # Dano por armadilha
        for obs in self.obstaculos:
            if obs.tipo == "armadilha" and self.jogador.rect.colliderect(obs.rect):
                vida_antes = self.jogador.vida
                self.jogador.receber_dano(10)
                if self.jogador.vida < vida_antes:
                    self.mensagens.adicionar("Cuidado com a armadilha!", 40, (255, 80, 80))

        # Ataque do jogador: apenas 1 hit por inimigo em cada espadada
        if self.jogador.area_ataque:
            for inimigo in self.inimigos:
                if inimigo not in self.jogador.inimigos_atingidos:
                    if self.jogador.area_ataque.colliderect(inimigo.rect) and not inimigo.morto:
                        self.jogador.inimigos_atingidos.add(inimigo)
                        inimigo.receber_dano(25)
                        if inimigo.morto:
                            self.inventario.pontuacao += 100
                            self.mensagens.adicionar("+100 Pontos!", 40, (255, 255, 0))

        # Verificar objetivo
        if not self.objetivo_concluido:
            self.verificar_objetivo()

        # Verificar saida
        if self.saida_liberada and self.saida:
            if self.jogador.rect.colliderect(self.saida):
                self.concluido = True

        # Verificar entrada (voltar nivel)
        if self.entrada and self.jogador.rect.colliderect(self.entrada):
            self.voltou = True

    def desenhar_saida(self):
        if not self.saida:
            return
        if self.saida_liberada:
            pygame.draw.rect(self.tela, (0, 180, 0), self.saida)
            pygame.draw.rect(self.tela, (0, 255, 0), self.saida, 3)
            f = pygame.font.Font(None, 20)
            t = f.render("SAIDA", True, (255, 255, 255))
            self.tela.blit(t, t.get_rect(center=self.saida.center))
        else:
            pygame.draw.rect(self.tela, (80, 20, 20), self.saida)
            pygame.draw.rect(self.tela, (120, 30, 30), self.saida, 3)
            f = pygame.font.Font(None, 16)
            t = f.render("BLOQUEADA", True, (180, 180, 180))
            self.tela.blit(t, t.get_rect(center=self.saida.center))

    def desenhar_entrada(self):
        if not self.entrada:
            return
        pygame.draw.rect(self.tela, (0, 180, 0), self.entrada)
        pygame.draw.rect(self.tela, (0, 255, 0), self.entrada, 3)
        f = pygame.font.Font(None, 20)
        t = f.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(t, t.get_rect(center=self.entrada.center))

    def desenhar_fundo(self):
        self.tela.fill((100, 100, 100))

    def desenhar(self):
        self.desenhar_fundo()
        self.desenhar_saida()
        self.desenhar_entrada()
        for obs in self.obstaculos:
            obs.desenhar(self.tela)
        for item in self.itens:
            item.desenhar(self.tela)
        for inimigo in self.inimigos:
            inimigo.desenhar(self.tela)
        self.jogador.desenhar(self.tela)


# ============================================================
# NIVEL 1 - PRAIA
# ============================================================

class CenaPraia(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 1
        self.objetivo_texto = "Colete 5 madeiras (e procure a caverna secreta)"

        self.jogador = Jogador(80, 400)
        self.saida = pygame.Rect(950, 350, 50, 80)
        
        # Entrada secreta para a fase bonus
        self.entrada_bonus = pygame.Rect(80, 150, 40, 40)
        self.foi_para_bonus = False

        self.obstaculos = [
            Obstaculo(250, 130, 50, 60, "arvore"),
            Obstaculo(450, 200, 50, 60, "arvore"),
            Obstaculo(350, 420, 60, 40, "pedra"),
            Obstaculo(650, 150, 50, 60, "arvore"),
            Obstaculo(800, 380, 50, 40, "pedra"),
            Obstaculo(150, 330, 50, 60, "arvore"),
        ]

        self.itens = [
            Item(300, 300, "madeira"),
            Item(500, 400, "madeira"),
            Item(600, 250, "madeira"),
            Item(750, 150, "madeira"),
            Item(880, 480, "madeira"),
        ]

    def verificar_objetivo(self):
        if self.inventario.quantidade("madeira") >= 5:
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Objetivo concluido! Saida desbloqueada!", 120, (0, 255, 0))

    def atualizar(self):
        super().atualizar()
        if self.jogador.rect.colliderect(self.entrada_bonus):
            self.foi_para_bonus = True
            self.concluido = True

    def get_progresso(self):
        return f"Madeira: {self.inventario.quantidade('madeira')}/5"

    def desenhar_fundo(self):
        self.tela.fill((210, 190, 140))
        # Agua no fundo
        pygame.draw.rect(self.tela, (40, 120, 200), (0, 540, 1000, 60))
        for i in range(15):
            pygame.draw.ellipse(self.tela, (60, 150, 220), (i * 70, 534, 80, 16))
        # Detalhes decorativos
        for px, py in [(150, 510), (400, 495), (700, 520), (900, 505)]:
            pygame.draw.circle(self.tela, (220, 200, 160), (px, py), 4)
            
        # Desenhar entrada bonus
        pygame.draw.ellipse(self.tela, (50, 40, 30), self.entrada_bonus)
        pygame.draw.ellipse(self.tela, (30, 20, 10), self.entrada_bonus.inflate(-10, -10))


# ============================================================
# NIVEL 1.5 - BONUS (CAVERNA SECRETA)
# ============================================================

class CenaBonus(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 1.5
        self.objetivo_texto = "Sobreviva as armadilhas e pegue a espada"

        self.jogador = Jogador(60, 320)
        self.saida = pygame.Rect(915, 290, 50, 80)

        self.obstaculos = [
            # Bordas da caverna
            Obstaculo(0, 70, 1000, 20, "parede"),
            Obstaculo(0, 580, 1000, 20, "parede"),
            Obstaculo(0, 70, 20, 530, "parede"),
            Obstaculo(980, 70, 20, 530, "parede"),

            # Paredes internas espacadas (corredores largos de 220px a 240px)
            Obstaculo(260, 220, 20, 360, "parede"),  # Passagem superior livre (y: 90 a 220)
            Obstaculo(500, 90, 20, 360, "parede"),   # Passagem inferior livre (y: 450 a 580)
            Obstaculo(740, 220, 20, 360, "parede"),  # Passagem superior livre (y: 90 a 220)

            # Armadilhas estrategicamente distribuidas com espaco de desvio
            Obstaculo(110, 180, 45, 35, "armadilha"),
            Obstaculo(180, 460, 45, 35, "armadilha"),
            Obstaculo(420, 180, 45, 35, "armadilha"),
            Obstaculo(350, 480, 45, 35, "armadilha"),
            Obstaculo(650, 180, 45, 35, "armadilha"),
            Obstaculo(580, 460, 45, 35, "armadilha"),
            Obstaculo(830, 420, 45, 35, "armadilha"),
        ]

        self.itens = [
            Item(870, 330, "espada"),
        ]

        # Inimigos (gnomos da caverna) com velocidade reduzida e patrulha distribuida
        self.inimigos = [
            Inimigo(140, 320, patrol_range=110, velocidade=0.8, dano=8, chase_range=85, eixo_patrulha="y"),
            Inimigo(390, 270, patrol_range=110, velocidade=0.8, dano=8, chase_range=85, eixo_patrulha="y"),
            Inimigo(630, 320, patrol_range=110, velocidade=0.8, dano=8, chase_range=85, eixo_patrulha="y"),
            Inimigo(860, 200, patrol_range=80, velocidade=0.8, dano=8, chase_range=80, eixo_patrulha="y"),
        ]

    def verificar_objetivo(self):
        if self.inventario.quantidade("espada") >= 1:
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Voce pegou a espada! Saida desbloqueada!", 120, (0, 255, 0))

    def get_progresso(self):
        return "Espada encontrada!" if self.inventario.quantidade("espada") >= 1 else "Encontre a espada"

    def desenhar_fundo(self):
        self.tela.fill((20, 15, 30))
        for x in range(0, 1000, 100):
            for y in range(70, 600, 100):
                pygame.draw.rect(self.tela, (25, 20, 35), (x, y, 50, 50))
                pygame.draw.rect(self.tela, (15, 10, 25), (x+50, y+50, 50, 50))


# ============================================================
# NIVEL 2 - FLORESTA
# ============================================================

class CenaFloresta(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 2
        self.objetivo_texto = "Colete 3 cipos"

        self.jogador = Jogador(50, 300)
        self.saida = pygame.Rect(950, 300, 50, 80)
        self.entrada = pygame.Rect(0, 300, 50, 80)

        self.obstaculos = [
            Obstaculo(150, 100, 50, 60, "arvore"),
            Obstaculo(300, 200, 50, 60, "arvore"),
            Obstaculo(200, 420, 50, 60, "arvore"),
            Obstaculo(450, 120, 50, 60, "arvore"),
            Obstaculo(500, 380, 50, 60, "arvore"),
            Obstaculo(350, 520, 50, 60, "arvore"),
            Obstaculo(650, 200, 50, 60, "arvore"),
            Obstaculo(700, 420, 50, 60, "arvore"),
            Obstaculo(800, 150, 50, 60, "arvore"),
            Obstaculo(860, 500, 50, 60, "arvore"),
        ]

        self.itens = [
            Item(250, 310, "cipo"),
            Item(550, 250, "cipo"),
            Item(760, 480, "cipo"),
        ]

        self.inimigos = [
            Inimigo(400, 300, 80, 2, 15, 250),
            Inimigo(700, 300, 100, 2, 15, 250),
            Inimigo(500, 150, 60, 2, 10, 200),
        ]

    def verificar_objetivo(self):
        if self.inventario.quantidade("cipo") >= 3:
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Objetivo concluido! Saida desbloqueada!", 120, (0, 255, 0))

    def get_progresso(self):
        return f"Cipo: {self.inventario.quantidade('cipo')}/3"

    def desenhar_fundo(self):
        self.tela.fill((35, 100, 35))
        for px, py in [(100, 200), (300, 500), (600, 300), (800, 450), (500, 100)]:
            pygame.draw.ellipse(self.tela, (45, 120, 45), (px, py, 80, 40))
        for px, py in [(180, 280), (420, 450), (550, 350), (700, 150), (850, 380)]:
            pygame.draw.circle(self.tela, (200, 50, 50), (px, py), 3)


# ============================================================
# NIVEL 3 - CAVERNA
# ============================================================

class CenaCaverna(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 3
        self.objetivo_texto = "Encontre pedras e a chave"

        self.jogador = Jogador(50, 300)
        self.saida = pygame.Rect(920, 310, 55, 70)
        self.entrada = pygame.Rect(0, 310, 50, 80)

        # Porta
        self.porta = Obstaculo(750, 280, 12, 100, "porta")
        self.porta_aberta = False
        self.porta_msg_cooldown = 0

        # Paredes da caverna
        paredes = [
            (0, 70, 1000, 12, "parede"),
            (0, 588, 1000, 12, "parede"),
            (0, 70, 12, 530, "parede"),
            (988, 70, 12, 220, "parede"),
            (988, 390, 12, 210, "parede"),
            # Paredes internas
            (250, 82, 12, 198, "parede"),
            (250, 340, 12, 248, "parede"),
            (500, 82, 12, 318, "parede"),
            (500, 460, 12, 128, "parede"),
            (750, 82, 12, 198, "parede"),
            (750, 380, 12, 208, "parede"),
        ]
        self.obstaculos = [Obstaculo(*p) for p in paredes]
        self.obstaculos.append(self.porta)

        self.itens = [
            Item(100, 200, "pedra"),
            Item(100, 500, "pedra"),
            Item(350, 250, "pedra"),
            Item(350, 500, "pedra"),
            Item(600, 150, "pedra"),
            Item(650, 500, "chave"),
        ]
        
        self.inimigos = [
            Inimigo(150, 450, 50, 2, 15, 250),
            Inimigo(600, 250, 80, 2, 20, 200),
            Inimigo(850, 150, 40, 2, 10, 150),
        ]

    def verificar_objetivo(self):
        # Verificar porta
        if not self.porta_aberta:
            if self.porta_msg_cooldown > 0:
                self.porta_msg_cooldown -= 1
            porta_area = self.porta.rect.inflate(12, 12)
            if self.jogador.rect.colliderect(porta_area):
                if self.inventario.quantidade("chave") >= 1:
                    self.porta_aberta = True
                    if self.porta in self.obstaculos:
                        self.obstaculos.remove(self.porta)
                    self.mensagens.adicionar("A porta se abriu!", 120, (255, 215, 0))
                else:
                    if self.porta_msg_cooldown <= 0:
                        self.mensagens.adicionar("Voce precisa de uma chave!", 90, (255, 100, 100))
                        self.porta_msg_cooldown = 120

        # Verificar conclusao
        if (self.inventario.quantidade("pedra") >= 5 and
                self.inventario.quantidade("chave") >= 1 and
                self.porta_aberta):
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Objetivo concluido! Saida desbloqueada!", 120, (0, 255, 0))

    def get_progresso(self):
        ch = "Sim" if self.inventario.quantidade("chave") >= 1 else "Nao"
        pt = "Aberta" if self.porta_aberta else "Fechada"
        return f"Pedra: {self.inventario.quantidade('pedra')}/5 | Chave: {ch} | Porta: {pt}"

    def desenhar_fundo(self):
        self.tela.fill((30, 30, 45))
        for px, py in [(100, 300), (300, 200), (500, 400), (700, 300), (900, 200)]:
            s = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(s, (60, 50, 20, 30), (40, 40), 40)
            self.tela.blit(s, (px - 40, py - 40))


# ============================================================
# NIVEL 4 - MONTANHA
# ============================================================

class CenaMontanha(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 4
        self.objetivo_texto = "Colete 2 cordas"

        self.jogador = Jogador(50, 110)
        self.saida = pygame.Rect(920, 500, 60, 65)
        self.entrada = pygame.Rect(0, 110, 50, 80)

        rochas = [
            (0, 70, 1000, 15, "pedra"),
            (0, 575, 1000, 25, "pedra"),
            # Barreiras horizontais com gaps
            (0, 185, 350, 15, "pedra"),
            (450, 185, 550, 15, "pedra"),
            (200, 315, 550, 15, "pedra"),
            (850, 315, 150, 15, "pedra"),
            (0, 445, 400, 15, "pedra"),
            (550, 445, 450, 15, "pedra"),
            # Obstaculos extras
            (100, 250, 40, 30, "pedra"),
            (600, 380, 40, 30, "pedra"),
            (300, 500, 40, 30, "pedra"),
        ]
        self.obstaculos = [Obstaculo(*r) for r in rochas]

        self.itens = [
            Item(280, 250, "corda"),
            Item(700, 380, "corda"),
        ]

        self.inimigos = [
            Inimigo(200, 120, 50, 2, 15, 200),
            Inimigo(600, 250, 80, 3, 20, 300),
            Inimigo(400, 500, 60, 2, 15, 250),
        ]

    def verificar_objetivo(self):
        if self.inventario.quantidade("corda") >= 2:
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Objetivo concluido! Saida desbloqueada!", 120, (0, 255, 0))

    def get_progresso(self):
        return f"Corda: {self.inventario.quantidade('corda')}/2"

    def desenhar_fundo(self):
        self.tela.fill((100, 85, 70))
        for px, py in [(50, 130), (300, 250), (500, 500), (700, 130), (850, 370)]:
            pygame.draw.ellipse(self.tela, (110, 95, 78), (px, py, 50, 25))
        for x in range(0, 1000, 100):
            pygame.draw.ellipse(self.tela, (200, 200, 210), (x, 72, 50, 10))


# ============================================================
# NIVEL 5 - COSTA
# ============================================================

class CenaCosta(Cena):

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 5
        self.objetivo_texto = "Construa a jangada"

        self.jogador = Jogador(50, 300)
        self.saida = pygame.Rect(800, 400, 130, 80)
        self.entrada = pygame.Rect(0, 300, 50, 80)
        self.msg_falta_cooldown = 0

        self.obstaculos = [
            Obstaculo(200, 150, 50, 60, "arvore"),
            Obstaculo(400, 350, 60, 40, "pedra"),
            Obstaculo(350, 500, 50, 60, "arvore"),
            Obstaculo(550, 180, 50, 40, "pedra"),
            Obstaculo(600, 450, 50, 60, "arvore"),
        ]

        self.itens = []

        self.inimigos = [
            Inimigo(300, 200, 100, 2, 20, 250),
            Inimigo(700, 200, 100, 3, 20, 300),
            Inimigo(500, 400, 80, 2, 25, 250),
        ]

        self.recursos_necessarios = {
            "madeira": 5,
            "cipo": 3,
            "pedra": 5,
            "corda": 2,
            "chave": 1,
        }

    def tem_todos_recursos(self):
        for recurso, qtd in self.recursos_necessarios.items():
            if self.inventario.quantidade(recurso) < qtd:
                return False
        return True

    def verificar_objetivo(self):
        if self.msg_falta_cooldown > 0:
            self.msg_falta_cooldown -= 1

        if self.tem_todos_recursos():
            self.objetivo_concluido = True
            self.saida_liberada = True
            self.mensagens.adicionar("Todos os recursos reunidos! Construa a jangada!", 150, (255, 215, 0))
        else:
            raft_area = self.saida.inflate(20, 20)
            if self.jogador.rect.colliderect(raft_area) and self.msg_falta_cooldown <= 0:
                self.mensagens.adicionar("Faltam recursos para a jangada!", 90, (255, 100, 100))
                self.msg_falta_cooldown = 120

    def get_progresso(self):
        nomes = {"madeira": "Mad", "cipo": "Cip", "pedra": "Ped", "corda": "Cor", "chave": "Cha"}
        partes = []
        for rec, qtd in self.recursos_necessarios.items():
            atual = self.inventario.quantidade(rec)
            partes.append(f"{nomes[rec]}:{atual}/{qtd}")
        return " | ".join(partes)

    def desenhar_fundo(self):
        self.tela.fill((210, 190, 140))
        pygame.draw.rect(self.tela, (30, 100, 180), (750, 510, 250, 90))
        for i in range(5):
            pygame.draw.ellipse(self.tela, (50, 130, 210), (750 + i * 50, 505, 60, 14))

    def desenhar(self):
        self.desenhar_fundo()

        # Area da jangada
        if self.saida_liberada:
            pygame.draw.rect(self.tela, (139, 90, 43), self.saida)
            pygame.draw.rect(self.tela, (100, 60, 20), self.saida, 3)
            for i in range(4):
                y = self.saida.y + 10 + i * 18
                pygame.draw.line(self.tela, (100, 60, 20),
                    (self.saida.x + 5, y), (self.saida.right - 5, y), 2)
            sx = self.saida.centerx
            sy = self.saida.y
            pygame.draw.line(self.tela, (100, 60, 20), (sx, sy), (sx, sy - 40), 3)
            pygame.draw.polygon(self.tela, (220, 220, 240), [
                (sx + 2, sy - 35), (sx + 30, sy - 15), (sx + 2, sy - 5)])
            f = pygame.font.Font(None, 18)
            self.tela.blit(f.render("JANGADA", True, (255, 255, 255)),
                           f.render("JANGADA", True, (255, 255, 255)).get_rect(center=(self.saida.centerx, self.saida.bottom + 12)))
        else:
            pygame.draw.rect(self.tela, (80, 50, 30), self.saida)
            pygame.draw.rect(self.tela, (120, 80, 40), self.saida, 3)
            f = pygame.font.Font(None, 18)
            self.tela.blit(f.render("JANGADA", True, (160, 160, 160)),
                           f.render("JANGADA", True, (160, 160, 160)).get_rect(center=self.saida.center))

        for obs in self.obstaculos:
            obs.desenhar(self.tela)
        for item in self.itens:
            item.desenhar(self.tela)
        for inimigo in self.inimigos:
            inimigo.desenhar(self.tela)
        self.jogador.desenhar(self.tela)


# ============================================================
# CLASSE BASE DAS CENAS NA JANGADA
# ============================================================

class CenaJangada(Cena):
    """Cena base para as fases que se passam a bordo da jangada em alto-mar."""

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.area_jangada = pygame.Rect(180, 140, 640, 390)
        self.wave_timer = 0.0
        self.garantir_espada()

    def garantir_espada(self):
        """Garante que o jogador possua a espada/arpao para os desafios da jangada."""
        if self.inventario.quantidade("espada") == 0:
            self.inventario.adicionar("espada")
            self.mensagens.adicionar("Espada Naval equipada na jangada! [ESPACO para atacar]", 180, (255, 215, 0))

    def atualizar(self):
        self.wave_timer += 0.05
        super().atualizar()

        # Manter o jogador sobre o conves da jangada
        if self.jogador:
            conves = self.area_jangada.inflate(-20, -20)
            self.jogador.rect.clamp_ip(conves)

    def desenhar_jangada_base(self):
        """Desenha a estrutura de madeira, mastros e amarras da jangada."""
        aj = self.area_jangada

        # Sombra da jangada na agua
        sombra = aj.inflate(16, 16)
        sombra.y += 8
        pygame.draw.rect(self.tela, (15, 45, 95), sombra, border_radius=12)

        # Base de toras de madeira (madeira da ilha)
        pygame.draw.rect(self.tela, (139, 90, 43), aj, border_radius=8)
        pygame.draw.rect(self.tela, (90, 55, 25), aj, 4, border_radius=8)

        # Tabuas e toras horizontais
        num_toras = 10
        alt_tora = aj.height // num_toras
        for i in range(num_toras):
            ty = aj.y + i * alt_tora
            pygame.draw.line(self.tela, (100, 60, 20), (aj.x + 4, ty), (aj.right - 4, ty), 2)
            if i % 2 == 0:
                pygame.draw.circle(self.tela, (115, 75, 30), (aj.x + 80 + (i * 50) % 400, ty + alt_tora // 2), 3)

        # Amarras de corda e cipo nos cantos e laterais
        for cx, cy in [(aj.x + 15, aj.y + 15), (aj.right - 15, aj.y + 15),
                       (aj.x + 15, aj.bottom - 15), (aj.right - 15, aj.bottom - 15),
                       (aj.centerx, aj.y + 15), (aj.centerx, aj.bottom - 15)]:
            pygame.draw.rect(self.tela, (210, 180, 100), (cx - 10, cy - 8, 20, 16), border_radius=3)
            pygame.draw.rect(self.tela, (34, 139, 34), (cx - 6, cy - 6, 12, 12), 2)

        # Mastro central e velame
        mx, my = aj.centerx, aj.centery - 20
        # Mastro de madeira vertical
        pygame.draw.rect(self.tela, (85, 50, 20), (mx - 6, my - 60, 12, 110))
        pygame.draw.rect(self.tela, (50, 30, 10), (mx - 6, my - 60, 12, 110), 2)
        # Travessao da vela
        pygame.draw.rect(self.tela, (100, 60, 20), (mx - 50, my - 55, 100, 6))

        # Vela branca enfunada ao vento
        balanco = int(math.sin(self.wave_timer * 2) * 6)
        vela_pts = [
            (mx - 48, my - 50),
            (mx + 48, my - 50),
            (mx + 38 + balanco, my + 30),
            (mx - 38 + balanco, my + 30),
        ]
        pygame.draw.polygon(self.tela, (240, 240, 245), vela_pts)
        pygame.draw.polygon(self.tela, (180, 180, 195), vela_pts, 2)
        # Emblema na vela
        pygame.draw.circle(self.tela, (50, 120, 200), (mx + balanco // 2, my - 10), 10, 2)

        # Leme na popa
        pygame.draw.rect(self.tela, (100, 60, 20), (aj.x - 12, aj.centery - 15, 16, 30), border_radius=4)
        pygame.draw.rect(self.tela, (60, 35, 15), (aj.x - 12, aj.centery - 15, 16, 30), 2)


# ============================================================
# NIVEL 6 - ALTO-MAR (PREDADORES DAS MARES)
# ============================================================

class CenaMarAberto(CenaJangada):
    """Primeira fase em alto-mar: defender a jangada contra predadores marinhos."""

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 6
        self.objetivo_texto = "Defenda a jangada dos tubaroes com a ESPADA"

        self.jogador = Jogador(self.area_jangada.centerx - 60, self.area_jangada.centery + 30)
        self.saida = None  # Avanca automaticamente ao derrotar os monstros
        self.entrada = None
        self.timer_avanco = 0

        # Obstaculos no conves (caixotes de suprimentos recolhidos na ilha)
        self.obstaculos = [
            Obstaculo(self.area_jangada.x + 30, self.area_jangada.y + 30, 45, 45, "pedra", cor=(100, 65, 30)),
            Obstaculo(self.area_jangada.x + 30, self.area_jangada.bottom - 75, 45, 45, "pedra", cor=(100, 65, 30)),
            Obstaculo(self.area_jangada.right - 75, self.area_jangada.y + 30, 45, 45, "pedra", cor=(100, 65, 30)),
        ]

        # Destrocos recolhiveis trazidos pelas ondas
        self.itens = [
            Item(self.area_jangada.x + 120, self.area_jangada.y + 40, "madeira"),
            Item(self.area_jangada.right - 140, self.area_jangada.bottom - 50, "corda"),
            Item(self.area_jangada.x + 100, self.area_jangada.bottom - 60, "pedra"),
        ]

        # Predadores marinhos com velocidade balanceada
        self.inimigos = [
            Tubarao(100, 180, velocidade=1.4, dano=10),
            Tubarao(840, 220, velocidade=1.5, dano=12),
            Tubarao(300, 540, velocidade=1.3, dano=10),
            Tubarao(680, 540, velocidade=1.5, dano=12),
            Tubarao(500, 90, velocidade=1.4, dano=10),
        ]
        self.total_inimigos_iniciais = len(self.inimigos)

    def atualizar(self):
        super().atualizar()
        if self.timer_avanco > 0:
            self.timer_avanco -= 1
            if self.timer_avanco == 0:
                self.concluido = True

    def verificar_objetivo(self):
        vivos = len([i for i in self.inimigos if not i.morto])
        if vivos == 0 and not self.objetivo_concluido:
            self.objetivo_concluido = True
            self.timer_avanco = 70
            self.mensagens.adicionar("Predadores derrotados! A jangada segue viagem...", 120, (0, 255, 100))

    def get_progresso(self):
        vivos = len([i for i in self.inimigos if not i.morto])
        derrotados = self.total_inimigos_iniciais - vivos
        if vivos == 0:
            return "Navegando para o proximo setor..."
        return f"Tubaroes: {derrotados}/{self.total_inimigos_iniciais} | Espada: ESPACO"

    def desenhar_fundo(self):
        self.tela.fill((25, 75, 155))

        for y in range(70, 600, 35):
            for x in range(-50, 1050, 70):
                desl_x = int(math.sin(self.wave_timer + y * 0.02) * 12)
                pygame.draw.arc(self.tela, (45, 105, 185),
                                (x + desl_x, y, 60, 20), 0, math.pi, 2)

        self.desenhar_jangada_base()


# ============================================================
# NIVEL 7 - A GRANDE TEMPESTADE (VORTICES E AMARRAS)
# ============================================================

class CenaTempestade(CenaJangada):
    """Segunda fase em alto-mar: suportar a tempestade e reparar a jangada."""

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 7
        self.objetivo_texto = "Repare os 3 postos da jangada com CORDA, CIPO e PEDRA"

        self.jogador = Jogador(self.area_jangada.centerx, self.area_jangada.centery + 60)
        self.saida = None  # Avanca automaticamente ao concluir
        self.entrada = None
        self.timer_avanco = 0

        # Postos de reparo na jangada
        self.posto_mastro = pygame.Rect(self.area_jangada.centerx - 25, self.area_jangada.centery - 50, 50, 50)
        self.posto_vela = pygame.Rect(self.area_jangada.centerx + 70, self.area_jangada.centery - 70, 50, 50)
        self.posto_leme = pygame.Rect(self.area_jangada.x + 20, self.area_jangada.centery - 25, 50, 50)

        self.reparo_mastro = False
        self.reparo_vela = False
        self.reparo_leme = False

        # Caixas de amarras
        self.obstaculos = [
            Obstaculo(self.area_jangada.x + 40, self.area_jangada.bottom - 70, 40, 40, "pedra", cor=(70, 45, 25)),
            Obstaculo(self.area_jangada.right - 80, self.area_jangada.bottom - 70, 40, 40, "pedra", cor=(70, 45, 25)),
        ]

        # Itens de reserva no conves
        self.itens = [
            Item(self.area_jangada.x + 90, self.area_jangada.bottom - 60, "corda"),
            Item(self.area_jangada.right - 130, self.area_jangada.y + 40, "cipo"),
            Item(self.area_jangada.x + 140, self.area_jangada.y + 40, "pedra"),
        ]

        # Espectros da tempestade com velocidade suave
        self.inimigos = [
            EspectroTempestade(self.area_jangada.x + 80, self.area_jangada.y + 80, velocidade=1.2),
            EspectroTempestade(self.area_jangada.right - 100, self.area_jangada.y + 80, velocidade=1.2),
            EspectroTempestade(self.area_jangada.centerx, self.area_jangada.bottom - 90, velocidade=1.1),
            EspectroTempestade(self.area_jangada.x + 120, self.area_jangada.bottom - 100, velocidade=1.3),
        ]

        # Efeitos climaticos
        self.tempo_relampago = 0
        self.flash_tela = 0
        self.gotas_chuva = [(random.randint(0, 1000), random.randint(70, 600)) for _ in range(60)]

    def atualizar(self):
        super().atualizar()
        if self.timer_avanco > 0:
            self.timer_avanco -= 1
            if self.timer_avanco == 0:
                self.concluido = True

        # Atualizar chuva
        novas_gotas = []
        for gx, gy in self.gotas_chuva:
            gx += 4
            gy += 14
            if gx > 1000 or gy > 600:
                gx = random.randint(0, 1000)
                gy = 70
            novas_gotas.append((gx, gy))
        self.gotas_chuva = novas_gotas

        # Relampagos periodicos
        self.tempo_relampago += 1
        if self.tempo_relampago > 200:
            self.tempo_relampago = 0
            self.flash_tela = 8
            self.mensagens.adicionar("Relampago cortou o ceu!", 40, (255, 255, 180))

        if self.flash_tela > 0:
            self.flash_tela -= 1

        # Interacao com postos de reparo
        jr = self.jogador.rect

        if not self.reparo_mastro and jr.colliderect(self.posto_mastro):
            if self.inventario.quantidade("corda") > 0:
                self.reparo_mastro = True
                self.inventario.pontuacao += 50
                self.mensagens.adicionar("Mastro amarrado com a CORDA! (+50 pts)", 120, (255, 215, 0))
            else:
                self.mensagens.adicionar("Voce precisa de CORDA para firmar o mastro!", 40, (255, 120, 120))

        if not self.reparo_vela and jr.colliderect(self.posto_vela):
            if self.inventario.quantidade("cipo") > 0:
                self.reparo_vela = True
                self.inventario.pontuacao += 50
                self.mensagens.adicionar("Vela costurada com os CIPOS! (+50 pts)", 120, (255, 215, 0))
            else:
                self.mensagens.adicionar("Voce precisa de CIPO para remendar a vela!", 40, (255, 120, 120))

        if not self.reparo_leme and jr.colliderect(self.posto_leme):
            if self.inventario.quantidade("pedra") > 0:
                self.reparo_leme = True
                self.inventario.pontuacao += 50
                self.mensagens.adicionar("Leme fixado com as PEDRAS! (+50 pts)", 120, (255, 215, 0))
            else:
                self.mensagens.adicionar("Voce precisa de PEDRA para estabilizar o leme!", 40, (255, 120, 120))

    def verificar_objetivo(self):
        vivos = len([i for i in self.inimigos if not i.morto])
        if self.reparo_mastro and self.reparo_vela and self.reparo_leme and vivos == 0 and not self.objetivo_concluido:
            self.objetivo_concluido = True
            self.timer_avanco = 75
            self.mensagens.adicionar("Tempestade domada! A jangada ruma ao epicentro...", 120, (0, 255, 100))

    def get_progresso(self):
        vivos = len([i for i in self.inimigos if not i.morto])
        if self.reparo_mastro and self.reparo_vela and self.reparo_leme and vivos == 0:
            return "Rumo as aguas do Leviata..."
        m = "OK" if self.reparo_mastro else "Mastro (Corda)"
        v = "OK" if self.reparo_vela else "Vela (Cipo)"
        l = "OK" if self.reparo_leme else "Leme (Pedra)"
        return f"Reparos: [{m}] [{v}] [{l}] | Espectros: {vivos}"

    def desenhar_fundo(self):
        self.tela.fill((15, 25, 45))

        # Vortices no mar
        for vx, vy in [(100, 250), (900, 220), (120, 480), (880, 500)]:
            for r in [28, 20, 12, 6]:
                pygame.draw.circle(self.tela, (30, 60, 95), (vx, vy), r, 2)
            pygame.draw.circle(self.tela, (10, 15, 30), (vx, vy), 4)

        self.desenhar_jangada_base()

        # Postos de reparo
        self.desenhar_posto(self.posto_mastro, "Mastro", self.reparo_mastro, (210, 180, 100))
        self.desenhar_posto(self.posto_vela, "Vela", self.reparo_vela, (34, 139, 34))
        self.desenhar_posto(self.posto_leme, "Leme", self.reparo_leme, (150, 150, 150))

        # Chuva
        for gx, gy in self.gotas_chuva:
            pygame.draw.line(self.tela, (130, 170, 220), (gx, gy), (gx + 3, gy + 8), 1)

        # Flash de relampago
        if self.flash_tela > 0:
            flash_surf = pygame.Surface((1000, 600), pygame.SRCALPHA)
            alpha = int((self.flash_tela / 8) * 160)
            flash_surf.fill((255, 255, 255, alpha))
            self.tela.blit(flash_surf, (0, 0))

    def desenhar_posto(self, rect, nome, consertado, cor_destaque):
        if consertado:
            pygame.draw.rect(self.tela, (40, 140, 60), rect, border_radius=6)
            pygame.draw.rect(self.tela, (100, 255, 120), rect, 2, border_radius=6)
            simb = "OK!"
            cor_txt = (255, 255, 255)
        else:
            pygame.draw.rect(self.tela, (90, 40, 30), rect, border_radius=6)
            pygame.draw.rect(self.tela, cor_destaque, rect, 2, border_radius=6)
            simb = nome
            cor_txt = (255, 220, 150)

        f = pygame.font.Font(None, 16)
        txt = f.render(simb, True, cor_txt)
        self.tela.blit(txt, txt.get_rect(center=rect.center))


# ============================================================
# NIVEL 8 - O GUARDAO DAS MARES (O LEVIATA)
# ============================================================

class CenaLeviata(CenaJangada):
    """Batalha final no abismo: enfrentar o Leviata das Mares com espada e balista."""

    def __init__(self, tela, inventario, mensagens):
        super().__init__(tela, inventario, mensagens)
        self.nivel = 8
        self.objetivo_texto = "Derrote o Leviata das Mares (use a ESPADA e a BALISTA)"

        self.jogador = Jogador(self.area_jangada.centerx, self.area_jangada.centery + 70)
        self.saida = None  # Avanca automaticamente para vitoria ao derrotar
        self.entrada = None
        self.timer_avanco = 0

        # O Boss principal
        self.leviata = LeviataChefe(430, 80)

        # 4 Tentaculos ao redor da jangada
        self.tentaculos = [
            TentaculoLeviata(self.area_jangada.x + 60, self.area_jangada.y + 60),
            TentaculoLeviata(self.area_jangada.right - 100, self.area_jangada.y + 60),
            TentaculoLeviata(self.area_jangada.x + 90, self.area_jangada.bottom - 110),
            TentaculoLeviata(self.area_jangada.right - 130, self.area_jangada.bottom - 110),
        ]

        self.inimigos = [self.leviata] + self.tentaculos

        # Balista de Pedras instalada na jangada
        self.balista_rect = pygame.Rect(self.area_jangada.centerx - 30, self.area_jangada.bottom - 60, 60, 45)
        self.balista_cooldown = 0
        self.projeteis_balista = []

        # Caixotes de pedras para municao
        self.itens = [
            Item(self.area_jangada.centerx - 80, self.area_jangada.bottom - 50, "pedra"),
            Item(self.area_jangada.centerx + 60, self.area_jangada.bottom - 50, "pedra"),
        ]

        self.obstaculos = [
            Obstaculo(self.area_jangada.x + 30, self.area_jangada.centery, 35, 35, "pedra", cor=(90, 50, 30)),
            Obstaculo(self.area_jangada.right - 65, self.area_jangada.centery, 35, 35, "pedra", cor=(90, 50, 30)),
        ]

    def atualizar(self):
        super().atualizar()
        if self.timer_avanco > 0:
            self.timer_avanco -= 1
            if self.timer_avanco == 0:
                self.concluido = True

        if self.balista_cooldown > 0:
            self.balista_cooldown -= 1

        # Checar tentaculos vivos
        tentaculos_vivos = [t for t in self.tentaculos if not t.morto and t in self.inimigos]
        if len(tentaculos_vivos) == 0:
            if not self.leviata.vulneravel:
                self.leviata.vulneravel = True
                self.mensagens.adicionar("Tentaculos destruidos! Ataque o Leviata com a ESPADA!", 150, (255, 230, 50))

        # Disparo da Balista quando o jogador esta nela e pressiona ESPACO
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] and self.jogador.rect.colliderect(self.balista_rect.inflate(20, 20)):
            if self.balista_cooldown <= 0:
                if self.inventario.quantidade("pedra") > 0:
                    self.inventario.recursos["pedra"] -= 1
                    self.balista_cooldown = 40
                    self.projeteis_balista.append({
                        "rect": pygame.Rect(self.balista_rect.centerx - 8, self.balista_rect.y, 16, 16),
                        "vy": -9
                    })
                    self.mensagens.adicionar("Balista disparada com PEDRA! (-1 Pedra)", 50, (255, 200, 100))
                else:
                    self.mensagens.adicionar("Sem pedras para a Balista!", 40, (255, 120, 120))

        # Atualizar projeteis da balista
        for proj in self.projeteis_balista[:]:
            proj["rect"].y += proj["vy"]
            if proj["rect"].colliderect(self.leviata.rect):
                self.leviata.receber_dano(30)
                self.mensagens.adicionar("Impacto critico no Leviata! (-30 HP)", 60, (255, 240, 50))
                self.projeteis_balista.remove(proj)
            elif proj["rect"].bottom < 70:
                self.projeteis_balista.remove(proj)

    def verificar_objetivo(self):
        if (self.leviata.morto or self.leviata.vida <= 0) and not self.objetivo_concluido:
            self.objetivo_concluido = True
            self.timer_avanco = 90
            self.mensagens.adicionar("O LEVIATA FOI DERROTADO! Liberdade conquistada!", 180, (255, 220, 0))

    def get_progresso(self):
        if self.leviata.morto or self.leviata.vida <= 0:
            return "Vitoria alcancada!"
        tentaculos_vivos = len([t for t in self.tentaculos if not t.morto and t in self.inimigos])
        if tentaculos_vivos > 0:
            return f"Tentaculos: {tentaculos_vivos}/4 | Espada: ESPACO"
        else:
            return f"Leviata: {max(0, self.leviata.vida)}/160 HP | Balista: Pedras ({self.inventario.quantidade('pedra')})"

    def desenhar_fundo(self):
        self.tela.fill((20, 15, 35))

        for y in range(70, 600, 40):
            desl = int(math.sin(self.wave_timer * 1.5 + y * 0.03) * 16)
            for x in range(-50, 1050, 80):
                pygame.draw.arc(self.tela, (45, 30, 75), (x + desl, y, 70, 22), 0, math.pi, 2)

        self.desenhar_jangada_base()

        # Balista Naval
        br = self.balista_rect
        pygame.draw.rect(self.tela, (70, 40, 20), br, border_radius=4)
        pygame.draw.rect(self.tela, (210, 180, 100), br, 2, border_radius=4)
        pygame.draw.line(self.tela, (140, 90, 40), (br.x - 10, br.centery), (br.right + 10, br.centery), 4)
        pygame.draw.line(self.tela, (220, 220, 220), (br.x - 10, br.centery), (br.centerx, br.bottom - 4), 1)
        pygame.draw.line(self.tela, (220, 220, 220), (br.right + 10, br.centery), (br.centerx, br.bottom - 4), 1)

        f = pygame.font.Font(None, 16)
        txt_b = f.render("BALISTA", True, (255, 255, 200))
        self.tela.blit(txt_b, txt_b.get_rect(center=(br.centerx, br.centery - 2)))

        for proj in self.projeteis_balista:
            pygame.draw.circle(self.tela, (160, 160, 170), proj["rect"].center, 8)
            pygame.draw.circle(self.tela, (240, 240, 250), proj["rect"].center, 8, 2)


# ============================================================
# FABRICA DE CENAS
# ============================================================

def criar_cena(nivel, tela, inventario, mensagens):
    cenas = {
        1: CenaPraia,
        1.5: CenaBonus,
        2: CenaFloresta,
        3: CenaCaverna,
        4: CenaMontanha,
        5: CenaCosta,
        6: CenaMarAberto,
        7: CenaTempestade,
        8: CenaLeviata,
    }
    classe = cenas.get(nivel)
    if classe:
        return classe(tela, inventario, mensagens)
    return None
