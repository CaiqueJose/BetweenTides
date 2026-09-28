import pygame
from scripts.jogador import Jogador
from scripts.obstaculo import Obstaculo
from scripts.itens import Item
from scripts.inimigo import Inimigo


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

        # Ataque do jogador
        if self.jogador.area_ataque:
            for inimigo in self.inimigos:
                if self.jogador.area_ataque.colliderect(inimigo.rect) and not inimigo.morto:
                    inimigo.receber_dano(20)
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

        self.jogador = Jogador(50, 300)
        self.saida = pygame.Rect(900, 260, 50, 80)
        
        self.obstaculos = [
            # Paredes do labirinto
            Obstaculo(0, 70, 1000, 20, "parede"),
            Obstaculo(0, 580, 1000, 20, "parede"),
            Obstaculo(0, 70, 20, 530, "parede"),
            Obstaculo(980, 70, 20, 530, "parede"),
            
            Obstaculo(150, 200, 20, 380, "parede"),
            Obstaculo(300, 90, 20, 380, "parede"),
            Obstaculo(450, 200, 20, 380, "parede"),
            Obstaculo(600, 90, 20, 380, "parede"),
            Obstaculo(750, 200, 20, 380, "parede"),
            
            # Armadilhas no chao
            Obstaculo(200, 150, 50, 40, "armadilha"),
            Obstaculo(350, 500, 50, 40, "armadilha"),
            Obstaculo(500, 150, 50, 40, "armadilha"),
            Obstaculo(650, 500, 50, 40, "armadilha"),
            Obstaculo(800, 150, 50, 40, "armadilha"),
        ]

        self.itens = [
            Item(850, 300, "espada"),
        ]

        self.inimigos = [
            Inimigo(200, 300, 40, 1, 10, 100),
            Inimigo(350, 300, 40, 1, 10, 100),
            Inimigo(500, 300, 40, 1, 10, 100),
            Inimigo(650, 300, 40, 1, 10, 100),
            Inimigo(800, 300, 40, 1, 10, 100),
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
    }
    classe = cenas.get(nivel)
    if classe:
        return classe(tela, inventario, mensagens)
    return None
