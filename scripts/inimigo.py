import pygame
import math


class Inimigo:
    """Inimigo simples com patrulha e perseguicao."""

    def __init__(self, x, y, patrol_range=100, velocidade=2, dano=10, chase_range=180, eixo_patrulha="x"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidade = velocidade
        self.start_x = x
        self.start_y = y
        self.patrol_range = patrol_range
        self.direcao = 1
        self.chase_range = chase_range
        self.dano = dano
        self.vida = 25
        self.vida_max = 25
        self.morto = False
        self.eixo_patrulha = eixo_patrulha
        self.direcao_olhar = "baixo" if eixo_patrulha == "y" else "direita"
        self.anim_passo = 0.0
        self.eh_chefe = False
        self.tempo_atordoado = 0
        # Posicao fracionaria para movimento suave
        self.float_x = float(x)
        self.float_y = float(y)

    def receber_dano(self, quantidade):
        self.vida -= quantidade
        # Atordoamento para inimigos que nao sao chefes
        if not self.eh_chefe:
            self.tempo_atordoado = 45  # ~0.75 segundo de atordoamento
        if self.vida <= 0:
            self.morto = True

    def desenhar_efeito_atordoado(self, tela):
        """Desenha estrelas giratorias amarelas quando atordoado."""
        if not self.eh_chefe and self.tempo_atordoado > 0:
            cx, cy = self.rect.centerx, self.rect.top - 8
            ang_base = (45 - self.tempo_atordoado) * 0.25
            for i in range(3):
                ang = ang_base + i * (2 * math.pi / 3)
                sx = cx + int(math.cos(ang) * 12)
                sy = cy + int(math.sin(ang) * 5)
                pygame.draw.line(tela, (255, 230, 50), (sx - 3, sy), (sx + 3, sy), 2)
                pygame.draw.line(tela, (255, 230, 50), (sx, sy - 3), (sx, sy + 3), 2)
                pygame.draw.circle(tela, (255, 255, 255), (sx, sy), 1)

    def atualizar(self, jogador_rect, obstaculos=None):
        if not self.eh_chefe and self.tempo_atordoado > 0:
            self.tempo_atordoado -= 1
            return

        if obstaculos is None:
            obstaculos = []

        dx = jogador_rect.centerx - self.rect.centerx
        dy = jogador_rect.centery - self.rect.centery
        distancia = math.sqrt(dx * dx + dy * dy)

        mov_x = 0.0
        mov_y = 0.0

        if distancia < self.chase_range and distancia > 0:
            # Perseguir o jogador
            mov_x = self.velocidade * dx / distancia
            mov_y = self.velocidade * dy / distancia
            if dx > 0:
                self.direcao = 1
            elif dx < 0:
                self.direcao = -1
        else:
            # Patrulhar de acordo com o eixo de configuracao
            if self.eixo_patrulha == "y":
                mov_y = 1 * self.direcao
                if self.rect.y > self.start_y + self.patrol_range:
                    self.direcao = -1
                elif self.rect.y < self.start_y - self.patrol_range:
                    self.direcao = 1
            else:
                mov_x = 1 * self.direcao
                if self.rect.x > self.start_x + self.patrol_range:
                    self.direcao = -1
                elif self.rect.x < self.start_x - self.patrol_range:
                    self.direcao = 1

        # Atualizar orientacao do olhar e passos
        if abs(mov_x) > 0 or abs(mov_y) > 0:
            self.anim_passo += 0.2
            if abs(mov_x) >= abs(mov_y):
                self.direcao_olhar = "direita" if mov_x > 0 else "esquerda"
            else:
                self.direcao_olhar = "baixo" if mov_y > 0 else "cima"

        # Acumular movimento fracionario suavemente (sem descartar fracoes a cada frame)
        self.float_x += mov_x
        self.float_y += mov_y
        pixel_mov_x = int(self.float_x) - self.rect.x
        pixel_mov_y = int(self.float_y) - self.rect.y

        # Movimento horizontal com colisao em obstaculos
        colidiu_x = False
        self.rect.x += pixel_mov_x
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if pixel_mov_x > 0:
                    self.rect.right = obs.rect.left
                elif pixel_mov_x < 0:
                    self.rect.left = obs.rect.right
                self.float_x = float(self.rect.x)
                colidiu_x = True

        # Movimento vertical com colisao em obstaculos
        colidiu_y = False
        self.rect.y += pixel_mov_y
        for obs in obstaculos:
            if obs.tipo != "armadilha" and self.rect.colliderect(obs.rect):
                if pixel_mov_y > 0:
                    self.rect.bottom = obs.rect.top
                elif pixel_mov_y < 0:
                    self.rect.top = obs.rect.bottom
                self.float_y = float(self.rect.y)
                colidiu_y = True

        # Desvio inteligente caso bloqueado por obstaculo durante perseguicao
        if distancia < self.chase_range:
            if colidiu_x and not colidiu_y and pixel_mov_y == 0:
                desvio = 1 if dy >= 0 else -1
                self.rect.y += desvio
                self.float_y = float(self.rect.y)
            elif colidiu_y and not colidiu_x and pixel_mov_x == 0:
                desvio = 1 if dx >= 0 else -1
                self.rect.x += desvio
                self.float_x = float(self.rect.x)

        # Limitar a tela apenas quando atinge a borda
        orig_x, orig_y = self.rect.x, self.rect.y
        self.rect.clamp_ip(pygame.Rect(0, 70, 1000, 530))
        if self.rect.x != orig_x:
            self.float_x = float(self.rect.x)
        if self.rect.y != orig_y:
            self.float_y = float(self.rect.y)

    def desenhar(self, tela):
        cx, cy = self.rect.center

        # Renderizacao estilo GTA 1/2 (olhando diretamente para a cabeca e ombros de cima)
        cor_corpo = (205, 30, 30)
        cor_corpo_escuro = (130, 15, 15)
        cor_ombro_esp = (80, 15, 15)
        cor_olho = (255, 235, 40)
        cor_garra = (50, 10, 10)

        surf = pygame.Surface((44, 44), pygame.SRCALPHA)
        scx, scy = 22, 22

        # 1. Patas/pes com animacao de passos
        off_pe1 = math.sin(self.anim_passo) * 2.5
        off_pe2 = -math.sin(self.anim_passo) * 2.5
        pygame.draw.rect(surf, (100, 15, 15), (scx - 10, scy + 6 + off_pe1, 7, 8), border_radius=2)
        pygame.draw.rect(surf, (100, 15, 15), (scx + 3, scy + 6 + off_pe2, 7, 8), border_radius=2)

        # 2. Ombros largos e quadrados
        corpo_rect = pygame.Rect(scx - 13, scy - 5, 26, 14)
        pygame.draw.rect(surf, cor_corpo, corpo_rect, border_radius=4)
        pygame.draw.rect(surf, cor_corpo_escuro, corpo_rect, 2, border_radius=4)

        # Espinhos afiados nos ombros
        pygame.draw.polygon(surf, cor_ombro_esp, [(scx - 13, scy - 3), (scx - 17, scy - 1), (scx - 13, scy + 3)])
        pygame.draw.polygon(surf, cor_ombro_esp, [(scx + 13, scy - 3), (scx + 17, scy - 1), (scx + 13, scy + 3)])

        # 3. Bracos musculosos e garras estendidas para frente
        pygame.draw.rect(surf, cor_corpo, (scx - 14, scy - 10, 7, 9), border_radius=2)
        pygame.draw.polygon(surf, cor_garra, [(scx - 14, scy - 10), (scx - 11, scy - 14), (scx - 8, scy - 10)])

        pygame.draw.rect(surf, cor_corpo, (scx + 7, scy - 10, 7, 9), border_radius=2)
        pygame.draw.polygon(surf, cor_garra, [(scx + 8, scy - 10), (scx + 11, scy - 14), (scx + 14, scy - 10)])

        # 4. Cabeca (vista de cima)
        cabeca_rect = pygame.Rect(scx - 7, scy - 7, 14, 13)
        pygame.draw.rect(surf, (165, 20, 20), cabeca_rect, border_radius=3)
        pygame.draw.rect(surf, cor_corpo_escuro, cabeca_rect, 1, border_radius=3)

        # Chifres frontais voltados na direcao do olhar
        pygame.draw.polygon(surf, cor_ombro_esp, [(scx - 6, scy - 6), (scx - 9, scy - 13), (scx - 3, scy - 7)])
        pygame.draw.polygon(surf, cor_ombro_esp, [(scx + 6, scy - 6), (scx + 9, scy - 13), (scx + 3, scy - 7)])

        # Olhos amarelados ameacadores voltados para frente
        pygame.draw.ellipse(surf, cor_olho, (scx - 6, scy - 9, 4, 3))
        pygame.draw.ellipse(surf, cor_olho, (scx + 2, scy - 9, 4, 3))
        pygame.draw.circle(surf, (0, 0, 0), (scx - 4, scy - 8), 1)
        pygame.draw.circle(surf, (0, 0, 0), (scx + 4, scy - 8), 1)

        # Rotacionar conforme a direcao de movimento
        angulos = {
            "cima": 0,
            "esquerda": 90,
            "baixo": 180,
            "direita": 270
        }
        ang = angulos.get(self.direcao_olhar, 270)
        surf_rot = pygame.transform.rotate(surf, ang)
        rect_rot = surf_rot.get_rect(center=(cx, cy))
        tela.blit(surf_rot, rect_rot)

        # Efeito de atordoamento
        self.desenhar_efeito_atordoado(tela)

        # Barra de vida se ferido
        if self.vida < self.vida_max:
            bx, by = self.rect.x, self.rect.y - 10
            pygame.draw.rect(tela, (40, 40, 40), (bx, by, self.rect.width, 4))
            pct = max(0.0, self.vida / self.vida_max)
            pygame.draw.rect(tela, (220, 40, 40), (bx, by, int(self.rect.width * pct), 4))


# ============================================================
# INIMIGOS MARINHOS (AVENTURA NA JANGADA)
# ============================================================

class Tubarao(Inimigo):
    """Predador marinho que nada nas aguas e ataca a jangada."""

    def __init__(self, x, y, velocidade=1.5, dano=12):
        super().__init__(x, y, patrol_range=80, velocidade=velocidade, dano=dano, chase_range=320)
        self.rect = pygame.Rect(x, y, 42, 32)
        self.vida = 35
        self.vida_max = 35
        self.tipo = "tubarao"
        self.anim_offset = 0.0

    def atualizar(self, jogador_rect, obstaculos=None):
        super().atualizar(jogador_rect, obstaculos)
        self.anim_offset += 0.15

    def desenhar(self, tela):
        cx, cy = self.rect.center
        # Rastro de espuma na agua
        espuma_x = cx - 18 if self.direcao >= 0 else cx + 18
        pygame.draw.circle(tela, (180, 220, 255), (int(espuma_x), cy + 4), 6, 1)

        # Corpo do tubarao (cinza azulado)
        cor_corpo = (55, 85, 115)
        cor_barriga = (180, 200, 215)
        pygame.draw.ellipse(tela, cor_corpo, self.rect)

        # Barbatana dorsal
        barbatana_pts = [
            (cx - 4, cy - 4),
            (cx + 4, cy - 4),
            (cx - 2, cy - 16),
        ]
        pygame.draw.polygon(tela, (40, 65, 90), barbatana_pts)

        # Cauda
        cauda_osc = math.sin(self.anim_offset) * 4
        cauda_x = self.rect.left if self.direcao >= 0 else self.rect.right
        pygame.draw.polygon(tela, cor_corpo, [
            (cauda_x, cy),
            (cauda_x - 10 if self.direcao >= 0 else cauda_x + 10, cy - 8 + cauda_osc),
            (cauda_x - 10 if self.direcao >= 0 else cauda_x + 10, cy + 8 + cauda_osc),
        ])

        # Olho amarelo predador
        olho_x = self.rect.right - 10 if self.direcao >= 0 else self.rect.left + 10
        pygame.draw.circle(tela, (255, 230, 50), (olho_x, cy - 2), 4)
        pygame.draw.circle(tela, (0, 0, 0), (olho_x, cy - 2), 2)

        # Dentes afiados
        focinho_x = self.rect.right if self.direcao >= 0 else self.rect.left
        for i in range(3):
            dy = cy - 2 + i * 4
            pygame.draw.polygon(tela, (255, 255, 255), [
                (focinho_x, dy),
                (focinho_x - (4 if self.direcao >= 0 else -4), dy - 2),
                (focinho_x - (4 if self.direcao >= 0 else -4), dy + 2)
            ])

        # Barra de vida se ferido
        if self.vida < self.vida_max:
            bx, by = self.rect.x, self.rect.y - 10
            pygame.draw.rect(tela, (40, 40, 40), (bx, by, 42, 5))
            pct = max(0.0, self.vida / self.vida_max)
            pygame.draw.rect(tela, (220, 40, 40), (bx, by, int(42 * pct), 5))

        self.desenhar_efeito_atordoado(tela)


class EspectroTempestade(Inimigo):
    """Entidade eletrica das tempestades que flutua pelo conves."""

    def __init__(self, x, y, velocidade=1.2, dano=10):
        super().__init__(x, y, patrol_range=60, velocidade=velocidade, dano=dano, chase_range=350)
        self.rect = pygame.Rect(x, y, 32, 34)
        self.vida = 25
        self.vida_max = 25
        self.tipo = "espectro"
        self.fase_onda = 0.0

    def atualizar(self, jogador_rect, obstaculos=None):
        self.fase_onda += 0.1
        # Flutuacao vertical senoidal
        super().atualizar(jogador_rect, obstaculos)
        self.float_y += math.sin(self.fase_onda) * 0.8
        self.rect.y = int(self.float_y)

    def desenhar(self, tela):
        cx, cy = self.rect.center
        # Halo eletrico
        raio_aura = 18 + int(math.sin(self.fase_onda * 2) * 3)
        pygame.draw.circle(tela, (70, 180, 240), (cx, cy - 2), raio_aura, 1)

        # Cupula viva (azul eletrico / ciano)
        pygame.draw.ellipse(tela, (90, 220, 255), (cx - 14, cy - 14, 28, 22))
        pygame.draw.ellipse(tela, (180, 250, 255), (cx - 10, cy - 12, 20, 12))

        # Tentaculos eletricos ondulantes
        for i in range(4):
            tx = cx - 9 + i * 6
            ty = cy + 4
            dy = int(math.sin(self.fase_onda + i) * 6)
            pygame.draw.line(tela, (60, 200, 255), (tx, ty), (tx + dy // 2, ty + 12), 2)
            pygame.draw.circle(tela, (255, 255, 200), (tx + dy // 2, ty + 12), 2)

        # Olhos brilhantes
        pygame.draw.circle(tela, (255, 255, 255), (cx - 5, cy - 5), 3)
        pygame.draw.circle(tela, (255, 255, 255), (cx + 5, cy - 5), 3)
        pygame.draw.circle(tela, (0, 150, 220), (cx - 5, cy - 5), 1)
        pygame.draw.circle(tela, (0, 150, 220), (cx + 5, cy - 5), 1)

        # Barra de vida
        if self.vida < self.vida_max:
            bx, by = self.rect.x, self.rect.y - 8
            pygame.draw.rect(tela, (40, 40, 40), (bx, by, 32, 4))
            pct = max(0.0, self.vida / self.vida_max)
            pygame.draw.rect(tela, (0, 220, 220), (bx, by, int(32 * pct), 4))

        self.desenhar_efeito_atordoado(tela)


class TentaculoLeviata(Inimigo):
    """Tentaculo colossal do Leviata que emerge e ataca o conves da jangada."""

    def __init__(self, x, y, dano=15):
        super().__init__(x, y, patrol_range=0, velocidade=1.0, dano=dano, chase_range=150)
        self.rect = pygame.Rect(x, y, 46, 46)
        self.vida = 40
        self.vida_max = 40
        self.tipo = "tentaculo"
        self.anim = 0.0
        self.base_y = y

    def atualizar(self, jogador_rect, obstaculos=None):
        if self.tempo_atordoado > 0:
            self.tempo_atordoado -= 1
            return
        self.anim += 0.08
        # O tentaculo oscila levemente para frente e para tras
        self.rect.y = int(self.base_y + math.sin(self.anim) * 8)
        # Nao colide como obstaculo comum, ataca se o jogador estiver proximo
        dx = jogador_rect.centerx - self.rect.centerx
        dy = jogador_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < 80:
            self.rect.x += 1 if dx > 0 else -1

    def desenhar(self, tela):
        cx, cy = self.rect.center

        # Espuma borbulhante na base da agua
        for i in range(4):
            ex = cx - 18 + i * 12
            pygame.draw.circle(tela, (140, 210, 240), (ex, self.rect.bottom - 4), 6, 1)

        # Corpo espesso do tentaculo (verde abissal e purpura escuro)
        cor_base = (30, 80, 80)
        cor_detalhe = (80, 160, 150)
        cor_ventosa = (230, 150, 180)

        # Segmentos do tentaculo
        pontos_tentaculo = [
            (cx - 16, self.rect.bottom),
            (cx - 12 + int(math.sin(self.anim) * 6), cy),
            (cx - 4 + int(math.sin(self.anim) * 10), self.rect.top),
            (cx + 6 + int(math.sin(self.anim) * 10), self.rect.top),
            (cx + 12 + int(math.sin(self.anim) * 6), cy),
            (cx + 16, self.rect.bottom),
        ]
        pygame.draw.polygon(tela, cor_base, pontos_tentaculo)
        pygame.draw.polygon(tela, cor_detalhe, pontos_tentaculo, 2)

        # Ventosas brilhantes ao lado
        for i in range(3):
            vy = self.rect.bottom - 10 - i * 12
            vx = cx + 8 + int(math.sin(self.anim) * 6)
            pygame.draw.circle(tela, cor_ventosa, (vx, vy), 4)
            pygame.draw.circle(tela, (150, 60, 100), (vx, vy), 2)

        # Barra de vida do tentaculo
        bx, by = self.rect.x, self.rect.y - 10
        pygame.draw.rect(tela, (30, 30, 30), (bx, by, 46, 6))
        pct = max(0.0, self.vida / self.vida_max)
        cor_hp = (220, 60, 80) if pct < 0.4 else (60, 200, 100)
        pygame.draw.rect(tela, cor_hp, (bx, by, int(46 * pct), 6))
        pygame.draw.rect(tela, (200, 200, 200), (bx, by, 46, 6), 1)

        self.desenhar_efeito_atordoado(tela)


class LeviataChefe(Inimigo):
    """O Boss final: O lendario Leviata das Mares."""

    def __init__(self, x, y):
        super().__init__(x, y, patrol_range=120, velocidade=1.0, dano=20, chase_range=400)
        self.rect = pygame.Rect(x, y, 140, 80)
        self.vida = 160
        self.vida_max = 160
        self.tipo = "leviata"
        self.eh_chefe = True
        self.anim = 0.0
        self.vulneravel = False
        self.timer_ataque = 0
        self.rugindo = False

    def atualizar(self, jogador_rect, obstaculos=None):
        self.anim += 0.05
        # Move-se horizontalmente na beirada da agua
        self.rect.x = int(self.start_x + math.sin(self.anim) * self.patrol_range)
        
        # Se estiver vulneravel (tentaculos destruidos), desce mais perto do conves
        alvo_y = 120 if self.vulneravel else 75
        if self.rect.y < alvo_y:
            self.rect.y += 1
        elif self.rect.y > alvo_y:
            self.rect.y -= 1

    def desenhar(self, tela):
        cx, cy = self.rect.center

        # Efeito de turbilhao / espuma d'agua gigante ao redor
        for i in range(8):
            ang = self.anim * 2 + i * (math.pi / 4)
            ex = cx + int(math.cos(ang) * 75)
            ey = self.rect.bottom - 10 + int(math.sin(ang) * 15)
            pygame.draw.ellipse(tela, (120, 210, 255), (ex - 15, ey - 6, 30, 12), 1)

        # Cabeca titanica (azul abissal / verde musgo)
        cor_escama = (20, 65, 75)
        cor_borda = (40, 130, 145)

        # Corpo dorsal
        pygame.draw.ellipse(tela, cor_escama, self.rect)
        pygame.draw.ellipse(tela, cor_borda, self.rect, 3)

        # Chifres de coral luminosos
        chifre_esq = [(cx - 45, cy - 10), (cx - 65, cy - 40), (cx - 35, cy - 25)]
        chifre_dir = [(cx + 45, cy - 10), (cx + 65, cy - 40), (cx + 35, cy - 25)]
        pygame.draw.polygon(tela, (210, 130, 60), chifre_esq)
        pygame.draw.polygon(tela, (255, 170, 80), chifre_esq, 2)
        pygame.draw.polygon(tela, (210, 130, 60), chifre_dir)
        pygame.draw.polygon(tela, (255, 170, 80), chifre_dir, 2)

        # Olhos titanicos flamejantes
        olho_e_x, olho_d_x = cx - 28, cx + 28
        olho_y = cy - 6
        pygame.draw.ellipse(tela, (255, 220, 0), (olho_e_x - 10, olho_y - 6, 20, 14))
        pygame.draw.ellipse(tela, (255, 220, 0), (olho_d_x - 10, olho_y - 6, 20, 14))
        pygame.draw.circle(tela, (0, 0, 0), (olho_e_x, olho_y + 1), 5)
        pygame.draw.circle(tela, (0, 0, 0), (olho_d_x, olho_y + 1), 5)
        pygame.draw.circle(tela, (255, 100, 0), (olho_e_x + 1, olho_y), 2)
        pygame.draw.circle(tela, (255, 100, 0), (olho_d_x + 1, olho_y), 2)

        # Presas e fauces
        for i in range(5):
            px = cx - 30 + i * 15
            py = cy + 18
            pygame.draw.polygon(tela, (245, 245, 240), [
                (px, py), (px + 10, py), (px + 5, py + 14)
            ])

        # Joia fraca na testa (ponto critico da espada!) — sempre visivel
        joia_cor = (255, 80, 80) if (int(self.anim * 10) % 2 == 0) else (255, 220, 50)
        pygame.draw.circle(tela, joia_cor, (cx, cy - 18), 9)
        pygame.draw.circle(tela, (255, 255, 255), (cx, cy - 18), 9, 2)

        # Grande Barra de Vida de Chefe no topo
        bw, bh = 340, 14
        bx, by = 330, 75
        pygame.draw.rect(tela, (20, 20, 30), (bx - 2, by - 2, bw + 4, bh + 4))
        pygame.draw.rect(tela, (50, 20, 20), (bx, by, bw, bh))
        pct = max(0.0, self.vida / self.vida_max)
        cor_hp = (220, 40, 40) if pct < 0.3 else (240, 140, 20)
        pygame.draw.rect(tela, cor_hp, (bx, by, int(bw * pct), bh))
        pygame.draw.rect(tela, (255, 215, 0), (bx - 2, by - 2, bw + 4, bh + 4), 2)

        fonte = pygame.font.Font(None, 20)
        texto_boss = fonte.render(f"LEVIATA DAS MARES: {self.vida}/{self.vida_max}", True, (255, 255, 255))
        tela.blit(texto_boss, texto_boss.get_rect(center=(500, by - 10)))

