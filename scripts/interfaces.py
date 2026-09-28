import pygame


class GerenciadorMensagens:
    """Sistema de mensagens temporarias na tela."""

    def __init__(self):
        self.mensagens = []

    def adicionar(self, texto, duracao=90, cor=(255, 255, 100)):
        self.mensagens.append([texto, duracao, cor])

    def atualizar(self):
        self.mensagens = [[t, d - 1, c] for t, d, c in self.mensagens if d > 0]

    def desenhar(self, tela):
        fonte = pygame.font.Font(None, 28)
        y = 320
        for texto, duracao, cor in self.mensagens:
            superficie = fonte.render(texto, True, cor)
            rect = superficie.get_rect(center=(500, y))
            bg_rect = rect.inflate(20, 10)
            bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg.fill((0, 0, 0, min(180, duracao * 6)))
            tela.blit(bg, bg_rect)
            tela.blit(superficie, rect)
            y += 35


def desenhar_hud(tela, nivel, objetivo, vida, vida_max, progresso="", pontuacao=0):
    """Desenha a interface superior do jogo."""
    hud = pygame.Surface((1000, 65), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 180))
    tela.blit(hud, (0, 0))

    fn = pygame.font.Font(None, 26)
    fp = pygame.font.Font(None, 22)

    tela.blit(fn.render(f"Nivel {nivel}  |  Pontos: {pontuacao}", True, (255, 255, 255)), (12, 5))
    tela.blit(fp.render(f"Objetivo: {objetivo}", True, (200, 200, 200)), (12, 27))
    if progresso:
        tela.blit(fp.render(progresso, True, (255, 255, 100)), (12, 46))

    # Barra de vida
    bx, by, bw, bh = 860, 8, 120, 14
    pygame.draw.rect(tela, (60, 0, 0), (bx, by, bw, bh))
    vw = max(0, int(bw * vida / vida_max))
    cv = (0, 200, 0) if vida > 60 else (200, 200, 0) if vida > 30 else (200, 0, 0)
    pygame.draw.rect(tela, cv, (bx, by, vw, bh))
    pygame.draw.rect(tela, (200, 200, 200), (bx, by, bw, bh), 1)
    tela.blit(fp.render(f"Vida: {vida}", True, (255, 255, 255)), (bx, by + 18))


def desenhar_menu(tela):
    """Tela inicial do jogo."""
    tela.fill((10, 25, 50))

    ft = pygame.font.Font(None, 72)
    fs = pygame.font.Font(None, 28)
    fi = pygame.font.Font(None, 26)

    # Titulo com sombra
    sombra = ft.render("BETWEEN TIDES", True, (5, 15, 35))
    tela.blit(sombra, sombra.get_rect(center=(502, 172)))
    titulo = ft.render("BETWEEN TIDES", True, (200, 220, 255))
    tela.blit(titulo, titulo.get_rect(center=(500, 170)))

    sub = fs.render('"Uma ilha. Um naufrago. Uma ultima chance."', True, (140, 160, 190))
    tela.blit(sub, sub.get_rect(center=(500, 240)))

    # Ilha decorativa
    pygame.draw.ellipse(tela, (30, 80, 30), (350, 330, 300, 60))
    pygame.draw.ellipse(tela, (194, 178, 128), (370, 340, 260, 40))
    pygame.draw.rect(tela, (100, 60, 20), (480, 300, 8, 42))
    pygame.draw.ellipse(tela, (20, 100, 20), (455, 288, 60, 22))

    # Ondas
    for i in range(20):
        x = i * 55
        y = 410 + (i % 3) * 10
        pygame.draw.ellipse(tela, (20, 50, 100), (x, y, 60, 20))

    tela.blit(fi.render("Pressione ENTER para comecar", True, (220, 220, 220)),
              fi.render("Pressione ENTER para comecar", True, (220, 220, 220)).get_rect(center=(500, 500)))
    tela.blit(fi.render("W A S D = mover  |  ESC = sair", True, (100, 120, 150)),
              fi.render("W A S D = mover  |  ESC = sair", True, (100, 120, 150)).get_rect(center=(500, 545)))


def desenhar_vitoria(tela, pontuacao=0):
    """Tela de vitoria."""
    tela.fill((10, 35, 20))

    ft = pygame.font.Font(None, 56)
    fm = pygame.font.Font(None, 30)
    fi = pygame.font.Font(None, 26)

    tela.blit(ft.render("JANGADA CONSTRUIDA!", True, (255, 220, 50)),
              ft.render("JANGADA CONSTRUIDA!", True, (255, 220, 50)).get_rect(center=(500, 140)))

    tela.blit(fm.render("O naufrago conseguiu escapar da ilha.", True, (180, 240, 180)),
              fm.render("O naufrago conseguiu escapar da ilha.", True, (180, 240, 180)).get_rect(center=(500, 210)))

    tela.blit(fm.render(f"PONTUACAO FINAL: {pontuacao}", True, (255, 255, 100)),
              fm.render(f"PONTUACAO FINAL: {pontuacao}", True, (255, 255, 100)).get_rect(center=(500, 250)))

    # Jangada
    rx, ry = 420, 290
    pygame.draw.rect(tela, (139, 90, 43), (rx, ry, 160, 70))
    pygame.draw.rect(tela, (100, 60, 20), (rx, ry, 160, 70), 3)
    for i in range(4):
        pygame.draw.line(tela, (100, 60, 20), (rx + 5, ry + 8 + i * 16), (rx + 155, ry + 8 + i * 16), 2)
    pygame.draw.line(tela, (100, 60, 20), (rx + 80, ry), (rx + 80, ry - 55), 3)
    pygame.draw.polygon(tela, (220, 220, 240), [
        (rx + 82, ry - 50), (rx + 130, ry - 25), (rx + 82, ry - 5)])

    # Agua
    for i in range(20):
        pygame.draw.ellipse(tela, (20, 60, 140), (i * 55, 395 + (i % 3) * 8, 60, 15))

    tela.blit(fi.render("Pressione ENTER para jogar novamente", True, (255, 255, 255)),
              fi.render("Pressione ENTER para jogar novamente", True, (255, 255, 255)).get_rect(center=(500, 490)))
    tela.blit(fi.render("ESC para sair", True, (150, 150, 150)),
              fi.render("ESC para sair", True, (150, 150, 150)).get_rect(center=(500, 530)))


def desenhar_game_over(tela):
    """Tela de derrota."""
    tela.fill((40, 10, 10))

    ft = pygame.font.Font(None, 56)
    fi = pygame.font.Font(None, 28)

    tela.blit(ft.render("VOCE FOI DERROTADO", True, (200, 50, 50)),
              ft.render("VOCE FOI DERROTADO", True, (200, 50, 50)).get_rect(center=(500, 240)))
    tela.blit(fi.render("Pressione ENTER para tentar novamente", True, (255, 255, 255)),
              fi.render("Pressione ENTER para tentar novamente", True, (255, 255, 255)).get_rect(center=(500, 340)))
    tela.blit(fi.render("ESC para sair", True, (150, 150, 150)),
              fi.render("ESC para sair", True, (150, 150, 150)).get_rect(center=(500, 390)))


def desenhar_construcao(tela, progresso):
    """Animacao de construcao da jangada."""
    tela.fill((20, 15, 10))

    ft = pygame.font.Font(None, 48)
    fi = pygame.font.Font(None, 28)

    tela.blit(ft.render("Construindo a jangada...", True, (255, 220, 150)),
              ft.render("Construindo a jangada...", True, (255, 220, 150)).get_rect(center=(500, 170)))

    # Barra de progresso
    bx, by, bw, bh = 300, 260, 400, 30
    pygame.draw.rect(tela, (60, 40, 20), (bx, by, bw, bh))
    pygame.draw.rect(tela, (139, 90, 43), (bx, by, int(bw * progresso), bh))
    pygame.draw.rect(tela, (200, 160, 100), (bx, by, bw, bh), 2)

    tela.blit(fi.render(f"{int(progresso * 100)}%", True, (255, 255, 255)),
              fi.render(f"{int(progresso * 100)}%", True, (255, 255, 255)).get_rect(center=(500, 320)))

    # Jangada sendo construida
    rx, ry = 420, 370
    if progresso > 0.15:
        pygame.draw.rect(tela, (139, 90, 43), (rx, ry + 60, 160, 15))
    if progresso > 0.30:
        pygame.draw.rect(tela, (139, 90, 43), (rx, ry + 40, 160, 15))
    if progresso > 0.50:
        pygame.draw.rect(tela, (139, 90, 43), (rx, ry + 20, 160, 15))
    if progresso > 0.65:
        pygame.draw.rect(tela, (139, 90, 43), (rx, ry, 160, 15))
    if progresso > 0.80:
        pygame.draw.line(tela, (100, 60, 20), (rx + 80, ry), (rx + 80, ry - 50), 3)
    if progresso > 0.92:
        pygame.draw.polygon(tela, (220, 220, 240), [
            (rx + 82, ry - 45), (rx + 120, ry - 20), (rx + 82, ry - 5)])

    for i in range(20):
        pygame.draw.ellipse(tela, (20, 60, 140), (i * 55, 490 + (i % 3) * 8, 60, 15))


def desenhar_transicao(tela, nivel, nome):
    """Tela de transicao entre niveis."""
    tela.fill((10, 20, 40))

    fn = pygame.font.Font(None, 52)
    fm = pygame.font.Font(None, 36)

    tela.blit(fn.render(f"Nivel {nivel}", True, (255, 255, 255)),
              fn.render(f"Nivel {nivel}", True, (255, 255, 255)).get_rect(center=(500, 270)))
    tela.blit(fm.render(nome, True, (180, 200, 220)),
              fm.render(nome, True, (180, 200, 220)).get_rect(center=(500, 320)))


# ============================================
# DADOS DA GALERIA DE PERSONAGENS
# ============================================

CATEGORIAS_GALERIA = [
    {
        "nome": "JOGADOR",
        "subtitulo": "O Naufrago",
        "descricao": [
            "Um sobrevivente preso em uma ilha misteriosa.",
            "Controles: W A S D para mover",
            "ESPACO para atacar (precisa de espada)",
            "Vida: 100 HP | Velocidade: 4",
        ],
        "cor_fundo": (10, 25, 60),
    },
    {
        "nome": "INIMIGO",
        "subtitulo": "Criaturas Hostis",
        "descricao": [
            "Criaturas que patrulham a ilha.",
            "Perseguem o jogador quando se aproxima.",
            "Dano variavel | Vida: 20 HP",
            "Derrotar: +100 pontos",
        ],
        "cor_fundo": (40, 10, 10),
    },
    {
        "nome": "OBSTACULOS",
        "subtitulo": "Elementos do Cenario",
        "itens": [
            {"tipo": "arvore", "nome": "Arvore", "desc": "Bloqueia passagem"},
            {"tipo": "pedra", "nome": "Pedra", "desc": "Bloqueia passagem"},
            {"tipo": "parede", "nome": "Parede", "desc": "Limita areas"},
            {"tipo": "porta", "nome": "Porta", "desc": "Precisa de chave"},
            {"tipo": "armadilha", "nome": "Armadilha", "desc": "Causa 10 de dano"},
        ],
        "cor_fundo": (15, 20, 15),
    },
    {
        "nome": "ITENS",
        "subtitulo": "Coletaveis",
        "itens": [
            {"tipo": "madeira", "nome": "Madeira", "desc": "+10 pts | Jangada"},
            {"tipo": "cipo", "nome": "Cipo", "desc": "+10 pts | Jangada"},
            {"tipo": "pedra_item", "nome": "Pedra", "desc": "+10 pts | Jangada"},
            {"tipo": "corda", "nome": "Corda", "desc": "+10 pts | Jangada"},
            {"tipo": "chave", "nome": "Chave", "desc": "+50 pts | Abre portas"},
            {"tipo": "espada", "nome": "Espada", "desc": "+50 pts | Permite atacar"},
        ],
        "cor_fundo": (10, 15, 35),
    },
]


def _desenhar_personagem_jogador(tela, cx, cy, escala=3):
    """Desenha o jogador em escala aumentada para a galeria."""
    s = int(32 * escala)
    rect = pygame.Rect(cx - s // 2, cy - s // 2, s, s)
    # Corpo
    pygame.draw.rect(tela, (30, 120, 200), rect)
    pygame.draw.rect(tela, (20, 80, 160), rect, 3)
    # Olhos
    oy = rect.y + int(10 * escala)
    r_olho = int(4 * escala)
    r_pupila = int(2 * escala)
    ox1 = rect.x + int(10 * escala)
    ox2 = rect.x + int(22 * escala)
    pygame.draw.circle(tela, (255, 255, 255), (ox1, oy), r_olho)
    pygame.draw.circle(tela, (255, 255, 255), (ox2, oy), r_olho)
    pygame.draw.circle(tela, (0, 0, 0), (ox1, oy), r_pupila)
    pygame.draw.circle(tela, (0, 0, 0), (ox2, oy), r_pupila)
    # Brilho
    pygame.draw.rect(tela, (50, 150, 230), (rect.x + 4, rect.y + 4, 12, 8))


def _desenhar_personagem_inimigo(tela, cx, cy, escala=3):
    """Desenha o inimigo em escala aumentada para a galeria."""
    s = int(30 * escala)
    rect = pygame.Rect(cx - s // 2, cy - s // 2, s, s)
    # Corpo
    pygame.draw.rect(tela, (200, 30, 30), rect)
    pygame.draw.rect(tela, (150, 20, 20), rect, 3)
    # Olhos
    oy = rect.y + int(10 * escala)
    r_olho = int(5 * escala)
    r_pupila = int(2 * escala)
    ox1 = rect.x + int(8 * escala)
    ox2 = rect.x + int(22 * escala)
    pygame.draw.circle(tela, (255, 255, 0), (ox1, oy), r_olho)
    pygame.draw.circle(tela, (255, 255, 0), (ox2, oy), r_olho)
    pygame.draw.circle(tela, (0, 0, 0), (ox1, oy), r_pupila)
    pygame.draw.circle(tela, (0, 0, 0), (ox2, oy), r_pupila)
    # Sobrancelhas
    sb_y1 = oy - int(6 * escala)
    sb_y2 = oy - int(3 * escala)
    pygame.draw.line(tela, (0, 0, 0),
        (rect.x + int(3 * escala), sb_y1), (rect.x + int(12 * escala), sb_y2), 3)
    pygame.draw.line(tela, (0, 0, 0),
        (rect.x + int(27 * escala), sb_y1), (rect.x + int(18 * escala), sb_y2), 3)


def _desenhar_obstaculo_galeria(tela, tipo, cx, cy, escala=2):
    """Desenha um obstaculo em escala para a galeria."""
    s = int(40 * escala)
    rect = pygame.Rect(cx - s // 2, cy - s // 2, s, s)

    if tipo == "arvore":
        tronco_w = int(14 * escala)
        tronco_h = int(18 * escala)
        tronco = pygame.Rect(rect.centerx - tronco_w // 2, rect.bottom - tronco_h, tronco_w, tronco_h)
        pygame.draw.rect(tela, (100, 60, 20), tronco)
        raio = s // 2
        centro = (rect.centerx, rect.centery - int(5 * escala))
        pygame.draw.circle(tela, (20, 100, 20), centro, raio)
        pygame.draw.circle(tela, (10, 70, 10), centro, raio, 2)

    elif tipo == "pedra":
        pygame.draw.rect(tela, (120, 110, 100), rect)
        pygame.draw.rect(tela, (90, 80, 70), rect, 3)

    elif tipo == "parede":
        pygame.draw.rect(tela, (55, 55, 65), rect)
        pygame.draw.rect(tela, (25, 25, 35), rect, 3)
        # Tijolos
        for i in range(4):
            y = rect.y + i * (s // 4)
            pygame.draw.line(tela, (35, 35, 45), (rect.x, y), (rect.right, y), 1)
        for i in range(3):
            x = rect.x + (i + 1) * (s // 3)
            pygame.draw.line(tela, (35, 35, 45), (x, rect.y), (x, rect.bottom), 1)

    elif tipo == "porta":
        pygame.draw.rect(tela, (140, 90, 40), rect)
        pygame.draw.rect(tela, (100, 60, 20), rect, 4)
        pcx, pcy = rect.centerx, rect.centery
        pygame.draw.circle(tela, (60, 40, 10), (pcx, pcy - int(3 * escala)), int(5 * escala))
        pygame.draw.polygon(tela, (60, 40, 10), [
            (pcx - int(3 * escala), pcy + int(2 * escala)),
            (pcx + int(3 * escala), pcy + int(2 * escala)),
            (pcx, pcy + int(10 * escala)),
        ])

    elif tipo == "armadilha":
        pygame.draw.rect(tela, (60, 60, 60), rect)
        spike_size = int(8 * escala)
        cols = max(1, s // (spike_size + 4))
        rows = max(1, s // (spike_size + 4))
        for i in range(cols):
            for j in range(rows):
                px = rect.x + int((i + 0.5) * s / cols) - spike_size // 2
                py = rect.y + int((j + 0.5) * s / rows) - spike_size // 2
                pygame.draw.polygon(tela, (150, 150, 150), [
                    (px, py + spike_size), (px + spike_size, py + spike_size), (px + spike_size // 2, py)
                ])


def _desenhar_item_galeria(tela, tipo, cx, cy, escala=2.5):
    """Desenha um item em escala para a galeria."""
    s = int(22 * escala)
    rect = pygame.Rect(cx - s // 2, cy - s // 2, s, s)

    cores = {
        "madeira": (139, 90, 43),
        "cipo": (34, 139, 34),
        "pedra_item": (150, 150, 150),
        "corda": (210, 180, 100),
        "chave": (255, 215, 0),
        "espada": (192, 192, 192),
    }
    cor = cores.get(tipo, (255, 255, 255))

    if tipo == "madeira":
        pygame.draw.rect(tela, cor, rect)
        for i in range(5):
            y = rect.y + int((i + 1) * s / 6)
            pygame.draw.line(tela, (100, 60, 20), (rect.x + 4, y), (rect.right - 4, y), 2)

    elif tipo == "cipo":
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, (20, 100, 20), rect, 3)

    elif tipo == "pedra_item":
        pygame.draw.circle(tela, (150, 150, 150), rect.center, s // 2)
        pygame.draw.circle(tela, (100, 100, 100), rect.center, s // 2, 3)

    elif tipo == "corda":
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, (180, 150, 70), rect, 3)

    elif tipo == "chave":
        pcx, pcy = rect.center
        raio_cab = int(7 * escala)
        pygame.draw.circle(tela, cor, (pcx, pcy - int(4 * escala)), raio_cab)
        pygame.draw.circle(tela, (200, 170, 0), (pcx, pcy - int(4 * escala)), raio_cab, 3)
        pygame.draw.rect(tela, cor, (pcx - int(2 * escala), pcy + int(1 * escala), int(4 * escala), int(12 * escala)))
        pygame.draw.rect(tela, cor, (pcx, pcy + int(9 * escala), int(5 * escala), int(3 * escala)))

    elif tipo == "espada":
        pcx, pcy = rect.center
        # Cabo
        pygame.draw.rect(tela, (139, 69, 19), (pcx - int(2 * escala), pcy + int(2 * escala), int(4 * escala), int(8 * escala)))
        # Guarda
        pygame.draw.rect(tela, (100, 100, 100), (pcx - int(6 * escala), pcy, int(12 * escala), int(2 * escala)))
        # Lamina
        pygame.draw.polygon(tela, cor, [
            (pcx - int(3 * escala), pcy),
            (pcx + int(3 * escala), pcy),
            (pcx, pcy - int(12 * escala)),
        ])


def desenhar_selecao_personagens(tela, categoria_idx, sub_idx, anim_timer):
    """Tela de selecao/galeria de personagens acessada pelo codigo secreto."""
    cat = CATEGORIAS_GALERIA[categoria_idx]
    tela.fill(cat["cor_fundo"])

    # Efeito de particulas decorativas
    import math
    for i in range(12):
        angle = anim_timer * 0.01 + i * 0.52
        px = 500 + int(math.cos(angle) * (200 + i * 15))
        py = 300 + int(math.sin(angle) * (120 + i * 10))
        alpha_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, 25))
        tela.blit(alpha_surf, (px, py))

    # Titulo da galeria
    ft = pygame.font.Font(None, 52)
    fs = pygame.font.Font(None, 32)
    fd = pygame.font.Font(None, 24)
    fi = pygame.font.Font(None, 22)

    # Titulo com efeito glow
    titulo_sombra = ft.render("GALERIA DE PERSONAGENS", True, (0, 0, 0))
    tela.blit(titulo_sombra, titulo_sombra.get_rect(center=(502, 42)))
    titulo = ft.render("GALERIA DE PERSONAGENS", True, (255, 220, 100))
    tela.blit(titulo, titulo.get_rect(center=(500, 40)))

    # Indicadores de categoria (tabs)
    tab_y = 75
    tab_w = 200
    total_w = tab_w * len(CATEGORIAS_GALERIA) + 20 * (len(CATEGORIAS_GALERIA) - 1)
    start_x = (1000 - total_w) // 2

    for i, c in enumerate(CATEGORIAS_GALERIA):
        tx = start_x + i * (tab_w + 20)
        if i == categoria_idx:
            pygame.draw.rect(tela, (255, 220, 100), (tx, tab_y, tab_w, 30), border_radius=6)
            cor_tab_txt = (10, 10, 10)
        else:
            pygame.draw.rect(tela, (40, 40, 50), (tx, tab_y, tab_w, 30), border_radius=6)
            pygame.draw.rect(tela, (80, 80, 90), (tx, tab_y, tab_w, 30), 2, border_radius=6)
            cor_tab_txt = (160, 160, 170)
        tab_txt = fd.render(c["nome"], True, cor_tab_txt)
        tela.blit(tab_txt, tab_txt.get_rect(center=(tx + tab_w // 2, tab_y + 15)))

    # Separador
    pygame.draw.line(tela, (60, 60, 70), (50, 115), (950, 115), 1)

    # Subtitulo da categoria
    sub_surf = fs.render(cat["subtitulo"], True, (200, 200, 220))
    tela.blit(sub_surf, sub_surf.get_rect(center=(500, 135)))

    # Area central de exibicao
    area_y = 160
    area_h = 320

    if categoria_idx == 0:
        # JOGADOR
        bob = int(math.sin(anim_timer * 0.05) * 5)
        _desenhar_personagem_jogador(tela, 500, area_y + area_h // 2 + bob, escala=3.5)
        # Descricao
        for i, linha in enumerate(cat["descricao"]):
            desc_surf = fd.render(linha, True, (180, 200, 220))
            tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 20 + i * 24)))

    elif categoria_idx == 1:
        # INIMIGO
        bob = int(math.sin(anim_timer * 0.07) * 4)
        _desenhar_personagem_inimigo(tela, 500, area_y + area_h // 2 + bob, escala=3.5)
        for i, linha in enumerate(cat["descricao"]):
            desc_surf = fd.render(linha, True, (220, 180, 180))
            tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 20 + i * 24)))

    elif categoria_idx == 2:
        # OBSTACULOS - mostra lista com seletor
        lista = cat["itens"]
        qtd = len(lista)
        # Sub-indice limitado
        idx = sub_idx % qtd

        # Desenhar o obstaculo selecionado no centro
        item_info = lista[idx]
        bob = int(math.sin(anim_timer * 0.06) * 3)
        _desenhar_obstaculo_galeria(tela, item_info["tipo"], 500, area_y + area_h // 2 - 20 + bob, escala=2.5)

        # Nome e descricao
        nome_surf = fs.render(item_info["nome"], True, (200, 220, 200))
        tela.blit(nome_surf, nome_surf.get_rect(center=(500, area_y + area_h + 10)))
        desc_surf = fd.render(item_info["desc"], True, (160, 180, 160))
        tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 38)))

        # Indicador de sub-item
        ind_surf = fi.render(f"{idx + 1}/{qtd}  (CIMA/BAIXO para navegar)", True, (120, 140, 120))
        tela.blit(ind_surf, ind_surf.get_rect(center=(500, area_y + area_h + 62)))

        # Mini previews na lateral
        for offset in [-2, -1, 1, 2]:
            other_idx = (idx + offset) % qtd
            other = lista[other_idx]
            lateral_x = 500 + offset * 160
            alpha_s = pygame.Surface((70, 70), pygame.SRCALPHA)
            alpha_s.fill((0, 0, 0, 80))
            tela.blit(alpha_s, (lateral_x - 35, area_y + area_h // 2 - 55))
            _desenhar_obstaculo_galeria(tela, other["tipo"], lateral_x, area_y + area_h // 2 - 20, escala=0.8)
            mini_nome = fi.render(other["nome"], True, (100, 120, 100))
            tela.blit(mini_nome, mini_nome.get_rect(center=(lateral_x, area_y + area_h // 2 + 20)))

    elif categoria_idx == 3:
        # ITENS - mostra lista com seletor
        lista = cat["itens"]
        qtd = len(lista)
        idx = sub_idx % qtd

        item_info = lista[idx]
        bob = int(math.sin(anim_timer * 0.06) * 3)
        _desenhar_item_galeria(tela, item_info["tipo"], 500, area_y + area_h // 2 - 20 + bob, escala=3)

        nome_surf = fs.render(item_info["nome"], True, (180, 200, 255))
        tela.blit(nome_surf, nome_surf.get_rect(center=(500, area_y + area_h + 10)))
        desc_surf = fd.render(item_info["desc"], True, (150, 170, 220))
        tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 38)))

        ind_surf = fi.render(f"{idx + 1}/{qtd}  (CIMA/BAIXO para navegar)", True, (120, 130, 180))
        tela.blit(ind_surf, ind_surf.get_rect(center=(500, area_y + area_h + 62)))

        # Mini previews
        for offset in [-2, -1, 1, 2]:
            other_idx = (idx + offset) % qtd
            other = lista[other_idx]
            lateral_x = 500 + offset * 140
            alpha_s = pygame.Surface((60, 60), pygame.SRCALPHA)
            alpha_s.fill((0, 0, 0, 80))
            tela.blit(alpha_s, (lateral_x - 30, area_y + area_h // 2 - 50))
            _desenhar_item_galeria(tela, other["tipo"], lateral_x, area_y + area_h // 2 - 20, escala=1)
            mini_nome = fi.render(other["nome"], True, (100, 110, 160))
            tela.blit(mini_nome, mini_nome.get_rect(center=(lateral_x, area_y + area_h // 2 + 15)))

    # Setas de navegacao de categoria
    seta_y = area_y + area_h // 2
    # Seta esquerda
    pygame.draw.polygon(tela, (255, 220, 100), [
        (30, seta_y), (55, seta_y - 20), (55, seta_y + 20)])
    # Seta direita
    pygame.draw.polygon(tela, (255, 220, 100), [
        (970, seta_y), (945, seta_y - 20), (945, seta_y + 20)])

    # Instrucoes no rodape
    pygame.draw.rect(tela, (0, 0, 0, 120), (0, 560, 1000, 40))
    rod = pygame.Surface((1000, 40), pygame.SRCALPHA)
    rod.fill((0, 0, 0, 150))
    tela.blit(rod, (0, 560))

    inst = fi.render(
        "ESQUERDA/DIREITA = Categoria  |  CIMA/BAIXO = Sub-item  |  ESC = Voltar ao Menu",
        True, (180, 180, 190),
    )
    tela.blit(inst, inst.get_rect(center=(500, 580)))