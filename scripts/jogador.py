import math
import pygame


class Jogador:
    """Classe do jogador (naufrago) com visual em terceira pessoa zenith/GTA."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocidade = 4
        self.vida = 100
        self.vida_max = 100
        self.dano_cooldown = 0
        self.cooldown_ataque = 0
        self.animacao_ataque = 0
        self.area_ataque = None
        self.direcao = "baixo"
        self.anim_passo = 0.0
        self.inimigos_atingidos = set()

    def receber_dano(self, quantidade):
        if self.dano_cooldown <= 0:
            self.vida -= quantidade
            self.dano_cooldown = 60
            if self.vida < 0:
                self.vida = 0

    def atacar(self):
        if self.cooldown_ataque <= 0:
            self.cooldown_ataque = 40
            self.animacao_ataque = 15
            self.inimigos_atingidos.clear()
            self.atualizar_area_ataque()
            return self.area_ataque
        return None

    def atualizar_area_ataque(self):
        # Cria um retangulo de ataque na direcao que o jogador esta olhando
        alcance = 55
        largura_ataque = 80
        if self.direcao == "cima":
            self.area_ataque = pygame.Rect(self.rect.centerx - largura_ataque//2, self.rect.top - alcance, largura_ataque, alcance)
        elif self.direcao == "baixo":
            self.area_ataque = pygame.Rect(self.rect.centerx - largura_ataque//2, self.rect.bottom, largura_ataque, alcance)
        elif self.direcao == "esquerda":
            self.area_ataque = pygame.Rect(self.rect.left - alcance, self.rect.centery - largura_ataque//2, alcance, largura_ataque)
        elif self.direcao == "direita":
            self.area_ataque = pygame.Rect(self.rect.right, self.rect.centery - largura_ataque//2, alcance, largura_ataque)

    def atualizar(self, obstaculos, largura, altura, hud_altura=70):
        teclas = pygame.key.get_pressed()

        mov_x = 0
        mov_y = 0

        if teclas[pygame.K_w]:
            mov_y = -self.velocidade
            self.direcao = "cima"
        elif teclas[pygame.K_s]:
            mov_y = self.velocidade
            self.direcao = "baixo"
        elif teclas[pygame.K_a]:
            mov_x = -self.velocidade
            self.direcao = "esquerda"
        elif teclas[pygame.K_d]:
            mov_x = self.velocidade
            self.direcao = "direita"

        if mov_x != 0 or mov_y != 0:
            self.anim_passo += 0.25

        # Movimento horizontal com colisao
        self.rect.x += mov_x
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if mov_x > 0:
                    self.rect.right = obs.rect.left
                elif mov_x < 0:
                    self.rect.left = obs.rect.right

        # Movimento vertical com colisao
        self.rect.y += mov_y
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if mov_y > 0:
                    self.rect.bottom = obs.rect.top
                elif mov_y < 0:
                    self.rect.top = obs.rect.bottom

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.top < hud_altura:
            self.rect.top = hud_altura
        if self.rect.bottom > altura:
            self.rect.bottom = altura

        # Cooldown de dano e ataque
        if self.dano_cooldown > 0:
            self.dano_cooldown -= 1
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1
        if self.animacao_ataque > 0:
            self.animacao_ataque -= 1
            if self.animacao_ataque > 0:
                self.atualizar_area_ataque()
            else:
                self.area_ataque = None
                self.inimigos_atingidos.clear()
        else:
            self.area_ataque = None
            self.inimigos_atingidos.clear()

    def desenhar(self, tela):
        # Piscar quando invencivel
        if self.dano_cooldown > 0 and (self.dano_cooldown // 5) % 2 == 0:
            return

        cx, cy = self.rect.center

        # Renderizacao estilo GTA 1/2 (olhando de cima diretamente para a cabeca e ombros)
        cor_camisa = (35, 115, 205)
        cor_camisa_borda = (20, 75, 145)
        cor_pele = (235, 195, 155)
        cor_cabelo = (75, 45, 25)
        cor_cinto = (110, 70, 30)
        cor_sapato = (50, 40, 35)

        surf = pygame.Surface((44, 44), pygame.SRCALPHA)
        scx, scy = 22, 22

        # 1. Pes (passos animados)
        off_pe1 = math.sin(self.anim_passo) * 3
        off_pe2 = -math.sin(self.anim_passo) * 3
        pygame.draw.ellipse(surf, cor_sapato, (scx - 8, scy + 4 + off_pe1, 6, 9))
        pygame.draw.ellipse(surf, cor_sapato, (scx + 2, scy + 4 + off_pe2, 6, 9))

        # 2. Ombros e Tronco (visto de cima: retangulo largo horizontal)
        ombro_rect = pygame.Rect(scx - 12, scy - 5, 24, 13)
        pygame.draw.rect(surf, cor_camisa, ombro_rect, border_radius=5)
        pygame.draw.rect(surf, cor_camisa_borda, ombro_rect, 2, border_radius=5)
        pygame.draw.line(surf, cor_cinto, (scx - 11, scy + 4), (scx + 11, scy + 4), 2)

        # 3. Bracos e Maos
        # Braco esquerdo
        pygame.draw.rect(surf, cor_camisa, (scx - 13, scy - 9, 6, 8), border_radius=2)
        pygame.draw.circle(surf, cor_pele, (scx - 10, scy - 10), 3)

        # Braco direito (mao da espada)
        if self.animacao_ataque > 0:
            # Mao estendida mais a frente segurando a espada
            pygame.draw.rect(surf, cor_camisa, (scx + 7, scy - 14, 6, 11), border_radius=2)
            pygame.draw.circle(surf, cor_pele, (scx + 10, scy - 15), 3)
            # Espada estendida para cima/frente
            pygame.draw.rect(surf, (140, 100, 40), (scx + 9, scy - 19, 2, 5))   # cabo
            pygame.draw.rect(surf, (220, 180, 50), (scx + 6, scy - 20, 8, 2))   # guarda
            pygame.draw.polygon(surf, (230, 235, 245), [
                (scx + 8, scy - 20), (scx + 12, scy - 20), (scx + 10, scy - 36)
            ])  # lamina afiada
            pygame.draw.line(surf, (255, 255, 255), (scx + 10, scy - 20), (scx + 10, scy - 34), 1)
        else:
            pygame.draw.rect(surf, cor_camisa, (scx + 7, scy - 9, 6, 8), border_radius=2)
            pygame.draw.circle(surf, cor_pele, (scx + 10, scy - 10), 3)

        # 4. Cabeca (no centro, vista de cima)
        pygame.draw.circle(surf, cor_pele, (scx, scy - 1), 7)
        pygame.draw.circle(surf, cor_cabelo, (scx, scy + 1), 7)
        pygame.draw.circle(surf, cor_cabelo, (scx, scy - 2), 5)
        # Nariz / ponta do rosto na direcao de visao
        pygame.draw.polygon(surf, (220, 175, 135), [(scx - 2, scy - 7), (scx + 2, scy - 7), (scx, scy - 9)])

        # Rotacionar conforme a direcao (norte/cima = 0)
        angulos = {
            "cima": 0,
            "esquerda": 90,
            "baixo": 180,
            "direita": 270
        }
        ang = angulos.get(self.direcao, 180)
        surf_rot = pygame.transform.rotate(surf, ang)
        rect_rot = surf_rot.get_rect(center=(cx, cy))
        tela.blit(surf_rot, rect_rot)

        # Arco do golpe de espada ao atacar
        if self.area_ataque and self.animacao_ataque > 0:
            raio = 52
            start_angle = 0
            end_angle = 0
            if self.direcao == "direita":
                start_angle, end_angle = -math.pi/3, math.pi/3
            elif self.direcao == "cima":
                start_angle, end_angle = math.pi/2 - math.pi/3, math.pi/2 + math.pi/3
            elif self.direcao == "esquerda":
                start_angle, end_angle = math.pi - math.pi/3, math.pi + math.pi/3
            elif self.direcao == "baixo":
                start_angle, end_angle = 3*math.pi/2 - math.pi/3, 3*math.pi/2 + math.pi/3

            rect_arc = pygame.Rect(cx - raio, cy - raio, raio * 2, raio * 2)
            pygame.draw.arc(tela, (210, 220, 240), rect_arc, start_angle, end_angle, 4)
            pygame.draw.arc(tela, (255, 255, 255), rect_arc.inflate(-8, -8), start_angle, end_angle, 2)
