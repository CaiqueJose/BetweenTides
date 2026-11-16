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


def desenhar_input_nome(tela, nome_atual, timer_cursor=0):
    """Tela de entrada de nome do jogador antes de iniciar a partida."""
    tela.fill((12, 22, 42))

    ft = pygame.font.Font(None, 52)
    fm = pygame.font.Font(None, 28)
    fi = pygame.font.Font(None, 22)
    f_input = pygame.font.Font(None, 38)

    # Ondas decorativas de fundo
    for i in range(20):
        ox = i * 55
        oy = 460 + (i % 3) * 12
        pygame.draw.ellipse(tela, (20, 45, 85), (ox, oy, 70, 22))

    # Titulo
    sombra = ft.render("REGISTRO DO NAUFRAGO", True, (5, 10, 20))
    tela.blit(sombra, sombra.get_rect(center=(502, 142)))
    titulo = ft.render("REGISTRO DO NAUFRAGO", True, (255, 220, 90))
    tela.blit(titulo, titulo.get_rect(center=(500, 140)))

    sub = fm.render("Informe seu nome para o quadro de recordes das mares:", True, (180, 210, 230))
    tela.blit(sub, sub.get_rect(center=(500, 205)))

    # Caixa de entrada de texto
    box_w, box_h = 460, 60
    box_rect = pygame.Rect((1000 - box_w) // 2, 260, box_w, box_h)
    pygame.draw.rect(tela, (18, 30, 56), box_rect, border_radius=8)
    pygame.draw.rect(tela, (255, 215, 0), box_rect, 2, border_radius=8)

    # Texto digitado e cursor
    cursor = "_" if (timer_cursor // 25) % 2 == 0 else " "
    texto_exibido = nome_atual if nome_atual else ""
    texto_surf = f_input.render(texto_exibido + cursor, True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(midleft=(box_rect.x + 20, box_rect.centery))
    tela.blit(texto_surf, texto_rect)

    # Dica quando vazio
    if not nome_atual:
        dica_fantasma = f_input.render("Digite seu nome... (Padrao: Naufrago)", True, (100, 125, 160))
        dica_rect = dica_fantasma.get_rect(midleft=(box_rect.x + 20, box_rect.centery))
        tela.blit(dica_fantasma, dica_rect)

    info_limite = fi.render("Maximo de 14 caracteres  |  Apenas letras, numeros e espacos", True, (140, 165, 190))
    tela.blit(info_limite, info_limite.get_rect(center=(500, 345)))

    # Instrucoes no rodape
    tela.blit(fm.render("Pressione ENTER para Confirmar e Iniciar", True, (255, 235, 100)),
              fm.render("Pressione ENTER para Confirmar e Iniciar", True, (255, 235, 100)).get_rect(center=(500, 440)))
    tela.blit(fi.render("ESC = Voltar ao Menu Principal", True, (150, 165, 185)),
              fi.render("ESC = Voltar ao Menu Principal", True, (150, 165, 185)).get_rect(center=(500, 485)))


def desenhar_vitoria(tela, pontuacao=0, recordes=None, posicao_jogador=None):
    """Tela de vitoria definitiva exibindo o ranking das melhores pontuacoes."""
    tela.fill((10, 25, 20))

    if recordes is None:
        from scripts.ranking import obter_recordes
        recordes, ultima_pos = obter_recordes()
        if posicao_jogador is None:
            posicao_jogador = ultima_pos

    ft = pygame.font.Font(None, 48)
    fs = pygame.font.Font(None, 24)
    fm = pygame.font.Font(None, 28)
    fi = pygame.font.Font(None, 22)
    fp = pygame.font.Font(None, 36)

    # Titulo superior com sombra
    sombra = ft.render("VITORIA DEFINITIVA!", True, (5, 15, 10))
    tela.blit(sombra, sombra.get_rect(center=(502, 37)))
    titulo = ft.render("VITORIA DEFINITIVA!", True, (255, 220, 50))
    tela.blit(titulo, titulo.get_rect(center=(500, 35)))

    sub = fs.render("O naufrago superou as mares revoltas e o lendario Leviata!", True, (180, 230, 200))
    tela.blit(sub, sub.get_rect(center=(500, 68)))

    # --- PAINEL ESQUERDO: Resumo da Expedicao (x: 40 a 470) ---
    p_esq = pygame.Rect(40, 95, 430, 435)
    card_esq = pygame.Surface((p_esq.width, p_esq.height), pygame.SRCALPHA)
    card_esq.fill((15, 35, 25, 210))
    tela.blit(card_esq, p_esq.topleft)
    pygame.draw.rect(tela, (40, 100, 60), p_esq, 2, border_radius=8)

    t_esq = fm.render("JORNADA CONCLUIDA", True, (200, 240, 210))
    tela.blit(t_esq, t_esq.get_rect(center=(p_esq.centerx, p_esq.y + 24)))

    txt_pts = fp.render(f"PONTUACAO: {pontuacao}", True, (255, 235, 90))
    tela.blit(txt_pts, txt_pts.get_rect(center=(p_esq.centerx, p_esq.y + 60)))

    if posicao_jogador and posicao_jogador <= 5:
        txt_pos = fs.render(f"* NOVO RECORDE: {posicao_jogador}o LUGAR NO RANKING! *", True, (255, 215, 0))
    elif posicao_jogador:
        txt_pos = fs.render(f"Posicao alcancada: {posicao_jogador}o lugar", True, (190, 220, 200))
    else:
        txt_pos = fs.render("Jangada em aguas calmas e seguras", True, (190, 220, 200))
    tela.blit(txt_pos, txt_pos.get_rect(center=(p_esq.centerx, p_esq.y + 92)))

    # Jangada ilustrada
    rx, ry = p_esq.centerx - 70, p_esq.y + 165
    pygame.draw.rect(tela, (139, 90, 43), (rx, ry, 140, 60), border_radius=6)
    pygame.draw.rect(tela, (100, 60, 20), (rx, ry, 140, 60), 3, border_radius=6)
    for i in range(3):
        pygame.draw.line(tela, (100, 60, 20), (rx + 4, ry + 12 + i * 15), (rx + 136, ry + 12 + i * 15), 2)
    pygame.draw.line(tela, (100, 60, 20), (rx + 70, ry), (rx + 70, ry - 50), 3)
    pygame.draw.polygon(tela, (235, 235, 245), [
        (rx + 72, ry - 45), (rx + 115, ry - 22), (rx + 72, ry - 5)])
    pygame.draw.polygon(tela, (190, 190, 205), [
        (rx + 72, ry - 45), (rx + 115, ry - 22), (rx + 72, ry - 5)], 2)

    # Ondas do mar iluminadas
    for i in range(9):
        ox = p_esq.x + 25 + i * 45
        oy = ry + 75 + (i % 2) * 6
        pygame.draw.ellipse(tela, (30, 95, 140), (ox, oy, 50, 14))
        pygame.draw.ellipse(tela, (70, 160, 190), (ox + 5, oy + 2, 40, 6))

    desc_final = fi.render("A liberdade foi reconquistada sobre as mares.", True, (160, 200, 180))
    tela.blit(desc_final, desc_final.get_rect(center=(p_esq.centerx, p_esq.bottom - 45)))
    desc_sub = fi.render("Todas as 8 fases foram superadas com sucesso!", True, (130, 175, 155))
    tela.blit(desc_sub, desc_sub.get_rect(center=(p_esq.centerx, p_esq.bottom - 22)))

    # --- PAINEL DIREITO: Ranking das Melhores Pontuacoes (x: 495 a 960) ---
    p_dir = pygame.Rect(495, 95, 465, 435)
    card_dir = pygame.Surface((p_dir.width, p_dir.height), pygame.SRCALPHA)
    card_dir.fill((15, 20, 35, 220))
    tela.blit(card_dir, p_dir.topleft)
    pygame.draw.rect(tela, (180, 150, 70), p_dir, 2, border_radius=8)

    t_rank = fm.render("* RANKING DAS MARES *", True, (255, 220, 90))
    tela.blit(t_rank, t_rank.get_rect(center=(p_dir.centerx, p_dir.y + 24)))

    sub_rank = fi.render("Melhores Pontuacoes Registradas", True, (160, 175, 200))
    tela.blit(sub_rank, sub_rank.get_rect(center=(p_dir.centerx, p_dir.y + 50)))

    # Cabecalho da tabela
    bar_y = p_dir.y + 72
    pygame.draw.rect(tela, (25, 35, 60), (p_dir.x + 15, bar_y, p_dir.width - 30, 28), border_radius=4)
    tela.blit(fi.render("POS", True, (210, 210, 220)), (p_dir.x + 28, bar_y + 6))
    tela.blit(fi.render("NAVEGADOR", True, (210, 210, 220)), (p_dir.x + 95, bar_y + 6))
    tela.blit(fi.render("PONTOS", True, (210, 210, 220)), (p_dir.right - 95, bar_y + 6))

    cores_pos = {
        1: (255, 215, 0),    # Ouro
        2: (215, 215, 225),  # Prata
        3: (205, 135, 75),   # Bronze
    }

    start_row_y = bar_y + 36
    row_h = 52

    for idx in range(5):
        row_rect = pygame.Rect(p_dir.x + 15, start_row_y + idx * row_h, p_dir.width - 30, row_h - 6)

        if recordes and idx < len(recordes):
            item = recordes[idx]
            nome = item.get("nome", "Naufrago")
            pts = str(item.get("pontos", 0))
            eh_atual = item.get("atual", False)
        else:
            nome = "---"
            pts = "---"
            eh_atual = False

        if eh_atual:
            pygame.draw.rect(tela, (65, 52, 18), row_rect, border_radius=6)
            pygame.draw.rect(tela, (255, 215, 0), row_rect, 2, border_radius=6)
        else:
            cor_bg = (20, 26, 44) if idx % 2 == 0 else (26, 34, 56)
            pygame.draw.rect(tela, cor_bg, row_rect, border_radius=6)

        pos_str = f"#{idx + 1}"
        cor_pos = cores_pos.get(idx + 1, (160, 175, 195))
        if eh_atual:
            cor_pos = (255, 230, 80)
        tela.blit(fm.render(pos_str, True, cor_pos), (row_rect.x + 12, row_rect.y + 12))

        cor_nome = (255, 255, 255) if eh_atual else (210, 215, 225)
        tag_atual = "  [VOCE]" if eh_atual else ""
        txt_nome = fi.render(f"{nome}{tag_atual}", True, cor_nome)
        tela.blit(txt_nome, (row_rect.x + 80, row_rect.y + 14))

        cor_pts = (255, 225, 80) if eh_atual else (180, 220, 255)
        txt_p = fm.render(str(pts), True, cor_pts)
        tela.blit(txt_p, (row_rect.right - 85, row_rect.y + 12))

    # Rodape
    tela.blit(fi.render("Pressione ENTER para jogar novamente   |   ESC para sair", True, (210, 220, 230)),
              fi.render("Pressione ENTER para jogar novamente   |   ESC para sair", True, (210, 220, 230)).get_rect(center=(500, 560)))


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
    """Animacao de construcao da jangada e partida para o mar."""
    tela.fill((20, 15, 10))

    ft = pygame.font.Font(None, 44)
    fi = pygame.font.Font(None, 28)

    titulo_const = "Zarpando para o Alto-Mar!" if progresso > 0.85 else "Construindo a jangada com os recursos..."
    tela.blit(ft.render(titulo_const, True, (255, 220, 150)),
              ft.render(titulo_const, True, (255, 220, 150)).get_rect(center=(500, 170)))

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
        "subtitulo": "O Naufrago Sobrevivente",
        "descricao": [
            "Um sobrevivente determinado a escapar das mares misteriosas.",
            "Controles: W A S D para mover pelo mapa e conves.",
            "ESPACO: Ataque com a Espada (Dano: 25 HP | Alcance amplo).",
            "Vida: 100 HP | Velocidade: 4.0 | Pontuacao acumulada na jornada.",
        ],
        "cor_fundo": (10, 25, 60),
    },
    {
        "nome": "INIMIGOS",
        "subtitulo": "Bestiario da Ilha e dos Mares",
        "itens": [
            {
                "tipo": "inimigo_comum",
                "nome": "Criatura da Ilha",
                "desc": "Vida: 25 HP | Dano: 10 | Patrulha terrestre",
                "detalhe": "Derrotado com 1 golpe de Espada. Tenta encurralar o naufrago.",
            },
            {
                "tipo": "tubarao",
                "nome": "Tubarao das Mares",
                "desc": "Vida: 35 HP | Dano: 10 | Predador marinho",
                "detalhe": "Derrotado com 2 golpes de Espada. Salta e investe contra o conves.",
            },
            {
                "tipo": "espectro",
                "nome": "Espectro da Tempestade",
                "desc": "Vida: 25 HP | Dano: 10 | Entidade eletrica flutuante",
                "detalhe": "Derrotado com 1 golpe de Espada. Emite descargas eletricas no ar.",
            },
            {
                "tipo": "tentaculo",
                "nome": "Tentaculo Abissal",
                "desc": "Vida: 40 HP | Dano: 15 | Membro colossal do Leviata",
                "detalhe": "Derrotado com 2 golpes de Espada. Golpeia o conves com violencia.",
            },
            {
                "tipo": "leviata",
                "nome": "Leviata das Mares (Boss)",
                "desc": "Vida: 160 HP | Dano: 20 | Chefe Supremo do Oceano",
                "detalhe": "Vulneravel a Espada (25 dano) e Balista (35 dano). Derrote para vencer!",
            },
        ],
        "cor_fundo": (35, 12, 18),
    },
    {
        "nome": "JANGADA",
        "subtitulo": "Embarcacao de Fuga e Combate",
        "descricao": [
            "Construida com 5 Madeiras, 3 Cipos, 5 Pedras, 2 Cordas e 1 Chave.",
            "Navega pelas 3 fases de alto-mar: Predadores, Tempestade e Leviata.",
            "Equipada com Mastro reforcado, Velame costurado, Leme e Balista Naval.",
            "A Balista dispara PEDRAS causando 35 de dano critico no Leviata!",
        ],
        "cor_fundo": (15, 30, 45),
    },
    {
        "nome": "OBSTACULOS",
        "subtitulo": "Elementos do Cenario",
        "itens": [
            {"tipo": "arvore", "nome": "Arvore", "desc": "Vegetacao tropical que bloqueia passagens"},
            {"tipo": "pedra", "nome": "Pedra Grande", "desc": "Formacao rochosa solida nos cenarios"},
            {"tipo": "parede", "nome": "Parede de Pedra", "desc": "Estrutura ancestral dos labirintos da ilha"},
            {"tipo": "porta", "nome": "Porta Selada", "desc": "Requer uma Chave dourada para destravar"},
            {"tipo": "armadilha", "nome": "Armadilha de Espinhos", "desc": "Causa 10 de dano ao caminhar por cima"},
        ],
        "cor_fundo": (15, 25, 18),
    },
    {
        "nome": "ITENS",
        "subtitulo": "Recursos da Sobrevivencia",
        "itens": [
            {"tipo": "madeira", "nome": "Madeira", "desc": "Coletada na Praia | Estrutura da jangada (+10 pts)"},
            {"tipo": "cipo", "nome": "Cipo", "desc": "Coletado na Floresta | Amarras e velame (+10 pts)"},
            {"tipo": "pedra_item", "nome": "Pedra", "desc": "Coletada na Caverna | Lastro e municao da Balista (+10 pts)"},
            {"tipo": "corda", "nome": "Corda", "desc": "Coletada na Montanha | Amarra do mastro (+10 pts)"},
            {"tipo": "chave", "nome": "Chave Dourada", "desc": "Encontrada na Caverna | Destranca portas (+50 pts)"},
            {"tipo": "espada", "nome": "Espada Naval", "desc": "Arma forjada para o naufrago | Dano: 25 HP [ESPACO]"},
        ],
        "cor_fundo": (10, 15, 35),
    },
    {
        "nome": "RANKING",
        "subtitulo": "Quadro dos Melhores Navegadores",
        "descricao": [
            "As melhores pontuacoes registradas na historia de Between Tides.",
            "Complete a fuga na jangada derrotando o Leviata para entrar no rank!",
            "Inimigos derrotados concedem +100 pontos; itens rendem +10 ou +50.",
            "As pontuacoes sao salvas automaticamente no arquivo recordes.json.",
        ],
        "cor_fundo": (12, 18, 32),
    },
]


def _desenhar_personagem_jogador(tela, cx, cy, escala=3):
    """Desenha o jogador em escala aumentada estilo GTA zenith para a galeria."""
    cor_camisa = (35, 115, 205)
    cor_camisa_borda = (20, 75, 145)
    cor_pele = (235, 195, 155)
    cor_cabelo = (75, 45, 25)
    cor_cinto = (110, 70, 30)

    # 1. Ombros e Tronco vistos de cima
    ow = int(24 * escala)
    oh = int(14 * escala)
    ombro_rect = pygame.Rect(cx - ow // 2, cy - oh // 2, ow, oh)
    pygame.draw.rect(tela, cor_camisa, ombro_rect, border_radius=int(4 * escala))
    pygame.draw.rect(tela, cor_camisa_borda, ombro_rect, 2, border_radius=int(4 * escala))
    pygame.draw.line(tela, cor_cinto, (ombro_rect.left + 2, ombro_rect.bottom - 3),
                     (ombro_rect.right - 2, ombro_rect.bottom - 3), int(2 * escala))

    # 2. Bracos e Maos voltados para a frente (baixo na galeria)
    bw = int(6 * escala)
    bh = int(8 * escala)
    # Braco esquerdo
    pygame.draw.rect(tela, cor_camisa, (ombro_rect.left - 2, ombro_rect.centery, bw, bh), border_radius=2)
    pygame.draw.circle(tela, cor_pele, (ombro_rect.left + bw // 2 - 2, ombro_rect.centery + bh), int(3 * escala))

    # Braco direito com espada desembainhada
    pygame.draw.rect(tela, cor_camisa, (ombro_rect.right - bw + 2, ombro_rect.centery, bw, bh + 4), border_radius=2)
    m_dir_x = ombro_rect.right - bw // 2 + 2
    m_dir_y = ombro_rect.centery + bh + 4
    pygame.draw.circle(tela, cor_pele, (m_dir_x, m_dir_y), int(3 * escala))
    # Lamina da espada para frente
    pygame.draw.rect(tela, (140, 100, 40), (m_dir_x - 1, m_dir_y + 2, 3, int(5 * escala)))  # cabo
    pygame.draw.rect(tela, (220, 180, 50), (m_dir_x - int(5 * escala), m_dir_y + int(7 * escala), int(10 * escala), 3))  # guarda
    pts_lamina = [
        (m_dir_x - int(3 * escala), m_dir_y + int(8 * escala)),
        (m_dir_x + int(3 * escala), m_dir_y + int(8 * escala)),
        (m_dir_x, m_dir_y + int(24 * escala))
    ]
    pygame.draw.polygon(tela, (230, 235, 245), pts_lamina)
    pygame.draw.line(tela, (255, 255, 255), (m_dir_x, m_dir_y + int(8 * escala)), (m_dir_x, m_dir_y + int(22 * escala)), 1)

    # 3. Cabeca no centro vista diretamente de cima
    r_cabeca = int(7 * escala)
    pygame.draw.circle(tela, cor_pele, (cx, cy - 2), r_cabeca)
    pygame.draw.circle(tela, cor_cabelo, (cx, cy - int(4 * escala)), r_cabeca)
    pygame.draw.circle(tela, cor_cabelo, (cx, cy), int(5 * escala))
    # Nariz / frente da cabeca apontando para baixo
    pygame.draw.polygon(tela, (220, 175, 135), [
        (cx - int(2 * escala), cy + r_cabeca - 2),
        (cx + int(2 * escala), cy + r_cabeca - 2),
        (cx, cy + r_cabeca + int(2 * escala))
    ])


def _desenhar_personagem_inimigo(tela, cx, cy, escala=3):
    """Desenha o inimigo quadrado em escala aumentada estilo GTA zenith para a galeria."""
    cor_corpo = (205, 30, 30)
    cor_corpo_escuro = (130, 15, 15)
    cor_ombro_esp = (80, 15, 15)
    cor_olho = (255, 235, 40)
    cor_garra = (50, 10, 10)

    # 1. Ombros quadrados musculosos
    ow = int(26 * escala)
    oh = int(14 * escala)
    ombro_rect = pygame.Rect(cx - ow // 2, cy - oh // 2, ow, oh)
    pygame.draw.rect(tela, cor_corpo, ombro_rect, border_radius=int(4 * escala))
    pygame.draw.rect(tela, cor_corpo_escuro, ombro_rect, 2, border_radius=int(4 * escala))

    # Espinhos nos ombros
    pygame.draw.polygon(tela, cor_ombro_esp, [
        (ombro_rect.left, cy - int(3 * escala)),
        (ombro_rect.left - int(5 * escala), cy),
        (ombro_rect.left, cy + int(3 * escala))
    ])
    pygame.draw.polygon(tela, cor_ombro_esp, [
        (ombro_rect.right, cy - int(3 * escala)),
        (ombro_rect.right + int(5 * escala), cy),
        (ombro_rect.right, cy + int(3 * escala))
    ])

    # 2. Bracos e garras projetados para frente
    bw = int(7 * escala)
    bh = int(10 * escala)
    # Braco esquerdo
    pygame.draw.rect(tela, cor_corpo, (ombro_rect.left, ombro_rect.centery, bw, bh), border_radius=2)
    pygame.draw.polygon(tela, cor_garra, [
        (ombro_rect.left, ombro_rect.centery + bh),
        (ombro_rect.left + bw, ombro_rect.centery + bh),
        (ombro_rect.left + bw // 2, ombro_rect.centery + bh + int(4 * escala))
    ])
    # Braco direito
    pygame.draw.rect(tela, cor_corpo, (ombro_rect.right - bw, ombro_rect.centery, bw, bh), border_radius=2)
    pygame.draw.polygon(tela, cor_garra, [
        (ombro_rect.right - bw, ombro_rect.centery + bh),
        (ombro_rect.right, ombro_rect.centery + bh),
        (ombro_rect.right - bw // 2, ombro_rect.centery + bh + int(4 * escala))
    ])

    # 3. Cabeca quadrada no centro vista de cima
    cw = int(14 * escala)
    ch = int(13 * escala)
    cabeca_rect = pygame.Rect(cx - cw // 2, cy - ch // 2, cw, ch)
    pygame.draw.rect(tela, (165, 20, 20), cabeca_rect, border_radius=3)
    pygame.draw.rect(tela, cor_corpo_escuro, cabeca_rect, 2, border_radius=3)

    # Chifres frontais
    pygame.draw.polygon(tela, cor_ombro_esp, [
        (cabeca_rect.left + 2, cabeca_rect.bottom - 2),
        (cabeca_rect.left - 2, cabeca_rect.bottom + int(6 * escala)),
        (cabeca_rect.left + int(4 * escala), cabeca_rect.bottom)
    ])
    pygame.draw.polygon(tela, cor_ombro_esp, [
        (cabeca_rect.right - 2, cabeca_rect.bottom - 2),
        (cabeca_rect.right + 2, cabeca_rect.bottom + int(6 * escala)),
        (cabeca_rect.right - int(4 * escala), cabeca_rect.bottom)
    ])

    # Olhos brilhantes ferozes
    olho_w = int(4 * escala)
    olho_h = int(3 * escala)
    pygame.draw.ellipse(tela, cor_olho, (cabeca_rect.left + int(2 * escala), cabeca_rect.bottom - int(5 * escala), olho_w, olho_h))
    pygame.draw.ellipse(tela, cor_olho, (cabeca_rect.right - int(2 * escala) - olho_w, cabeca_rect.bottom - int(5 * escala), olho_w, olho_h))
    pygame.draw.circle(tela, (0, 0, 0), (cabeca_rect.left + int(4 * escala), cabeca_rect.bottom - int(3 * escala)), 2)
    pygame.draw.circle(tela, (0, 0, 0), (cabeca_rect.right - int(4 * escala), cabeca_rect.bottom - int(3 * escala)), 2)


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


def _desenhar_inimigo_galeria(tela, tipo, cx, cy, escala=2.5):
    """Desenha qualquer inimigo em escala aumentada para a galeria."""
    if tipo == "inimigo_comum":
        _desenhar_personagem_inimigo(tela, cx, cy, escala)
    elif tipo == "tubarao":
        w, h = int(42 * escala), int(32 * escala)
        rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        pygame.draw.ellipse(tela, (55, 85, 115), rect)
        pygame.draw.polygon(tela, (40, 65, 90), [(cx - 10, cy - 10), (cx + 10, cy - 10), (cx, cy - 40)])
        pygame.draw.polygon(tela, (55, 85, 115), [(rect.left, cy), (rect.left - 25, cy - 20), (rect.left - 25, cy + 20)])
        pygame.draw.circle(tela, (255, 230, 50), (rect.right - 25, cy - 5), 8)
        pygame.draw.circle(tela, (0, 0, 0), (rect.right - 25, cy - 5), 4)
        for i in range(4):
            dy = cy - 8 + i * 8
            pygame.draw.polygon(tela, (255, 255, 255), [(rect.right, dy), (rect.right - 8, dy - 4), (rect.right - 8, dy + 4)])
    elif tipo == "espectro":
        raio = int(24 * escala)
        pygame.draw.circle(tela, (70, 180, 240), (cx, cy), raio + 10, 2)
        pygame.draw.ellipse(tela, (90, 220, 255), (cx - raio, cy - raio, raio * 2, int(raio * 1.5)))
        pygame.draw.ellipse(tela, (180, 250, 255), (cx - raio + 10, cy - raio + 5, int(raio * 1.5), raio))
        for i in range(5):
            tx = cx - 25 + i * 12
            pygame.draw.line(tela, (60, 200, 255), (tx, cy + 15), (tx, cy + 50), 3)
            pygame.draw.circle(tela, (255, 255, 200), (tx, cy + 50), 4)
        pygame.draw.circle(tela, (255, 255, 255), (cx - 12, cy - 5), 6)
        pygame.draw.circle(tela, (255, 255, 255), (cx + 12, cy - 5), 6)
        pygame.draw.circle(tela, (0, 140, 220), (cx - 12, cy - 5), 3)
        pygame.draw.circle(tela, (0, 140, 220), (cx + 12, cy - 5), 3)
    elif tipo == "tentaculo":
        h = int(90 * escala)
        w = int(35 * escala)
        pts = [
            (cx - w, cy + h // 2),
            (cx - w // 2, cy),
            (cx, cy - h // 2),
            (cx + w // 3, cy - h // 2 + 10),
            (cx + w // 2, cy),
            (cx + w, cy + h // 2),
        ]
        pygame.draw.polygon(tela, (30, 80, 80), pts)
        pygame.draw.polygon(tela, (80, 160, 150), pts, 3)
        for i in range(4):
            vy = cy + h // 2 - 25 - i * 30
            vx = cx + w // 2
            pygame.draw.circle(tela, (230, 150, 180), (vx, vy), 8)
            pygame.draw.circle(tela, (150, 60, 100), (vx, vy), 4)
    elif tipo == "leviata":
        w, h = int(120 * escala), int(65 * escala)
        rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        pygame.draw.ellipse(tela, (20, 65, 75), rect)
        pygame.draw.ellipse(tela, (40, 130, 145), rect, 4)
        pygame.draw.polygon(tela, (210, 130, 60), [(cx - 60, cy - 10), (cx - 100, cy - 60), (cx - 40, cy - 30)])
        pygame.draw.polygon(tela, (210, 130, 60), [(cx + 60, cy - 10), (cx + 100, cy - 60), (cx + 40, cy - 30)])
        pygame.draw.ellipse(tela, (255, 220, 0), (cx - 45, cy - 10, 30, 20))
        pygame.draw.ellipse(tela, (255, 220, 0), (cx + 15, cy - 10, 30, 20))
        pygame.draw.circle(tela, (0, 0, 0), (cx - 30, cy), 6)
        pygame.draw.circle(tela, (0, 0, 0), (cx + 30, cy), 6)
        pygame.draw.circle(tela, (255, 80, 80), (cx, cy - 25), 14)
        pygame.draw.circle(tela, (255, 255, 255), (cx, cy - 25), 14, 3)
        for i in range(6):
            px = cx - 45 + i * 18
            pygame.draw.polygon(tela, (245, 245, 240), [(px, cy + 20), (px + 12, cy + 20), (px + 6, cy + 36)])


def _desenhar_jangada_galeria(tela, cx, cy, escala=1.8):
    """Desenha a jangada completa em escala para a galeria."""
    w, h = int(160 * escala), int(90 * escala)
    rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    pygame.draw.rect(tela, (139, 90, 43), rect, border_radius=8)
    pygame.draw.rect(tela, (90, 55, 25), rect, 4, border_radius=8)
    for i in range(5):
        y = rect.y + i * (h // 5)
        pygame.draw.line(tela, (100, 60, 20), (rect.x + 4, y), (rect.right - 4, y), 2)
    mx, my = rect.centerx, rect.centery - 10
    pygame.draw.rect(tela, (85, 50, 20), (mx - 4, my - 60, 8, 80))
    pygame.draw.rect(tela, (100, 60, 20), (mx - 40, my - 55, 80, 4))
    vela_pts = [(mx - 38, my - 52), (mx + 38, my - 52), (mx + 28, my + 10), (mx - 28, my + 10)]
    pygame.draw.polygon(tela, (240, 240, 245), vela_pts)
    pygame.draw.polygon(tela, (180, 180, 195), vela_pts, 2)
    pygame.draw.rect(tela, (70, 40, 20), (rect.centerx - 20, rect.bottom - 22, 40, 18), border_radius=3)
    pygame.draw.rect(tela, (210, 180, 100), (rect.centerx - 20, rect.bottom - 22, 40, 18), 1, border_radius=3)


def desenhar_selecao_personagens(tela, categoria_idx, sub_idx, anim_timer):
    """Tela de selecao/galeria de personagens acessada pelo codigo secreto MARETIDE."""
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

    # Titulos
    ft = pygame.font.Font(None, 48)
    fs = pygame.font.Font(None, 30)
    fm = pygame.font.Font(None, 26)
    fd = pygame.font.Font(None, 24)
    fi = pygame.font.Font(None, 20)

    titulo_sombra = ft.render("GALERIA SECRETA MARETIDE", True, (0, 0, 0))
    tela.blit(titulo_sombra, titulo_sombra.get_rect(center=(502, 37)))
    titulo = ft.render("GALERIA SECRETA MARETIDE", True, (255, 220, 100))
    tela.blit(titulo, titulo.get_rect(center=(500, 35)))

    # Indicadores de categoria (tabs)
    tab_y = 65
    tab_w = 145
    espaco = 10
    total_w = tab_w * len(CATEGORIAS_GALERIA) + espaco * (len(CATEGORIAS_GALERIA) - 1)
    start_x = (1000 - total_w) // 2

    for i, c in enumerate(CATEGORIAS_GALERIA):
        tx = start_x + i * (tab_w + espaco)
        if i == categoria_idx:
            pygame.draw.rect(tela, (255, 220, 100), (tx, tab_y, tab_w, 28), border_radius=6)
            cor_tab_txt = (10, 10, 10)
        else:
            pygame.draw.rect(tela, (40, 40, 50), (tx, tab_y, tab_w, 28), border_radius=6)
            pygame.draw.rect(tela, (80, 80, 90), (tx, tab_y, tab_w, 28), 2, border_radius=6)
            cor_tab_txt = (160, 160, 170)
        tab_txt = fd.render(c["nome"], True, cor_tab_txt)
        tela.blit(tab_txt, tab_txt.get_rect(center=(tx + tab_w // 2, tab_y + 14)))

    pygame.draw.line(tela, (60, 60, 70), (40, 105), (960, 105), 1)

    sub_surf = fs.render(cat["subtitulo"], True, (200, 200, 220))
    tela.blit(sub_surf, sub_surf.get_rect(center=(500, 125)))

    area_y = 150
    area_h = 320

    if categoria_idx == 0:
        # JOGADOR
        bob = int(math.sin(anim_timer * 0.05) * 5)
        _desenhar_personagem_jogador(tela, 500, area_y + area_h // 2 + bob - 20, escala=3.5)
        for i, linha in enumerate(cat["descricao"]):
            desc_surf = fd.render(linha, True, (180, 200, 220))
            tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 10 + i * 24)))

    elif categoria_idx == 1:
        # INIMIGOS (com sub-itens)
        lista = cat["itens"]
        qtd = len(lista)
        idx = sub_idx % qtd
        item_info = lista[idx]
        bob = int(math.sin(anim_timer * 0.07) * 4)

        _desenhar_inimigo_galeria(tela, item_info["tipo"], 500, area_y + area_h // 2 - 30 + bob, escala=2.5)

        nome_surf = fs.render(item_info["nome"], True, (255, 180, 180))
        tela.blit(nome_surf, nome_surf.get_rect(center=(500, area_y + area_h + 10)))
        desc_surf = fd.render(item_info["desc"], True, (220, 200, 200))
        tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 36)))
        det_surf = fi.render(item_info["detalhe"], True, (190, 160, 160))
        tela.blit(det_surf, det_surf.get_rect(center=(500, area_y + area_h + 60)))

        ind_surf = fi.render(f"{idx + 1}/{qtd}  (CIMA/BAIXO para navegar)", True, (160, 130, 130))
        tela.blit(ind_surf, ind_surf.get_rect(center=(500, area_y + area_h + 82)))

        for offset in [-2, -1, 1, 2]:
            other_idx = (idx + offset) % qtd
            other = lista[other_idx]
            lateral_x = 500 + offset * 150
            alpha_s = pygame.Surface((60, 60), pygame.SRCALPHA)
            alpha_s.fill((0, 0, 0, 90))
            tela.blit(alpha_s, (lateral_x - 30, area_y + area_h // 2 - 60))
            _desenhar_inimigo_galeria(tela, other["tipo"], lateral_x, area_y + area_h // 2 - 30, escala=0.7)
            mini_nome = fi.render(other["nome"].split()[0], True, (160, 120, 120))
            tela.blit(mini_nome, mini_nome.get_rect(center=(lateral_x, area_y + area_h // 2 + 10)))

    elif categoria_idx == 2:
        # JANGADA
        bob = int(math.sin(anim_timer * 0.05) * 4)
        _desenhar_jangada_galeria(tela, 500, area_y + area_h // 2 - 30 + bob, escala=1.8)
        for i, linha in enumerate(cat["descricao"]):
            desc_surf = fd.render(linha, True, (180, 220, 240))
            tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 10 + i * 24)))

    elif categoria_idx == 3:
        # OBSTACULOS
        lista = cat["itens"]
        qtd = len(lista)
        idx = sub_idx % qtd
        item_info = lista[idx]
        bob = int(math.sin(anim_timer * 0.06) * 3)

        _desenhar_obstaculo_galeria(tela, item_info["tipo"], 500, area_y + area_h // 2 - 30 + bob, escala=2.5)

        nome_surf = fs.render(item_info["nome"], True, (200, 220, 200))
        tela.blit(nome_surf, nome_surf.get_rect(center=(500, area_y + area_h + 10)))
        desc_surf = fd.render(item_info["desc"], True, (160, 180, 160))
        tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 38)))

        ind_surf = fi.render(f"{idx + 1}/{qtd}  (CIMA/BAIXO para navegar)", True, (120, 140, 120))
        tela.blit(ind_surf, ind_surf.get_rect(center=(500, area_y + area_h + 65)))

        for offset in [-2, -1, 1, 2]:
            other_idx = (idx + offset) % qtd
            other = lista[other_idx]
            lateral_x = 500 + offset * 150
            alpha_s = pygame.Surface((60, 60), pygame.SRCALPHA)
            alpha_s.fill((0, 0, 0, 80))
            tela.blit(alpha_s, (lateral_x - 30, area_y + area_h // 2 - 60))
            _desenhar_obstaculo_galeria(tela, other["tipo"], lateral_x, area_y + area_h // 2 - 30, escala=0.8)
            mini_nome = fi.render(other["nome"].split()[0], True, (100, 120, 100))
            tela.blit(mini_nome, mini_nome.get_rect(center=(lateral_x, area_y + area_h // 2 + 10)))

    elif categoria_idx == 4:
        # ITENS
        lista = cat["itens"]
        qtd = len(lista)
        idx = sub_idx % qtd
        item_info = lista[idx]
        bob = int(math.sin(anim_timer * 0.06) * 3)

        _desenhar_item_galeria(tela, item_info["tipo"], 500, area_y + area_h // 2 - 30 + bob, escala=3)

        nome_surf = fs.render(item_info["nome"], True, (180, 200, 255))
        tela.blit(nome_surf, nome_surf.get_rect(center=(500, area_y + area_h + 10)))
        desc_surf = fd.render(item_info["desc"], True, (150, 170, 220))
        tela.blit(desc_surf, desc_surf.get_rect(center=(500, area_y + area_h + 38)))

        ind_surf = fi.render(f"{idx + 1}/{qtd}  (CIMA/BAIXO para navegar)", True, (120, 130, 180))
        tela.blit(ind_surf, ind_surf.get_rect(center=(500, area_y + area_h + 65)))

        for offset in [-2, -1, 1, 2]:
            other_idx = (idx + offset) % qtd
            other = lista[other_idx]
            lateral_x = 500 + offset * 140
            alpha_s = pygame.Surface((60, 60), pygame.SRCALPHA)
            alpha_s.fill((0, 0, 0, 80))
            tela.blit(alpha_s, (lateral_x - 30, area_y + area_h // 2 - 60))
            _desenhar_item_galeria(tela, other["tipo"], lateral_x, area_y + area_h // 2 - 30, escala=1)
            mini_nome = fi.render(other["nome"].split()[0], True, (100, 110, 160))
            tela.blit(mini_nome, mini_nome.get_rect(center=(lateral_x, area_y + area_h // 2 + 10)))

    elif categoria_idx == 5:
        # RANKING
        from scripts.ranking import carregar_recordes
        recs = carregar_recordes()

        qw, qh = 580, 270
        qx = (1000 - qw) // 2
        qy = area_y - 10

        q_surf = pygame.Surface((qw, qh), pygame.SRCALPHA)
        q_surf.fill((10, 15, 25, 230))
        tela.blit(q_surf, (qx, qy))
        pygame.draw.rect(tela, (210, 180, 80), (qx, qy, qw, qh), 2, border_radius=8)

        # Cabecalho da tabela
        pygame.draw.rect(tela, (25, 35, 60), (qx + 15, qy + 12, qw - 30, 28), border_radius=4)
        tela.blit(fi.render("POS", True, (210, 210, 220)), (qx + 30, qy + 18))
        tela.blit(fi.render("NAVEGADOR", True, (210, 210, 220)), (qx + 110, qy + 18))
        tela.blit(fi.render("PONTOS", True, (210, 210, 220)), (qx + qw - 95, qy + 18))

        cores_pos = {1: (255, 215, 0), 2: (215, 215, 225), 3: (205, 135, 75)}
        for idx in range(5):
            row_y = qy + 46 + idx * 42
            row_rect = pygame.Rect(qx + 15, row_y, qw - 30, 36)
            cor_bg = (18, 24, 40) if idx % 2 == 0 else (24, 32, 50)
            pygame.draw.rect(tela, cor_bg, row_rect, border_radius=5)

            if idx < len(recs):
                nome = recs[idx].get("nome", "---")
                pts = str(recs[idx].get("pontos", 0))
            else:
                nome = "---"
                pts = "---"

            cor_pos = cores_pos.get(idx + 1, (160, 175, 195))
            tela.blit(fm.render(f"#{idx + 1}", True, cor_pos), (row_rect.x + 15, row_rect.y + 8))
            tela.blit(fi.render(nome, True, (220, 225, 235)), (row_rect.x + 95, row_rect.y + 10))
            tela.blit(fm.render(str(pts), True, (255, 225, 80)), (row_rect.right - 85, row_rect.y + 8))

        for i, linha in enumerate(cat["descricao"]):
            desc_surf = fi.render(linha, True, (170, 190, 215))
            tela.blit(desc_surf, desc_surf.get_rect(center=(500, qy + qh + 20 + i * 20)))

    # Setas de navegacao
    seta_y = area_y + area_h // 2 - 20
    pygame.draw.polygon(tela, (255, 220, 100), [(30, seta_y), (55, seta_y - 20), (55, seta_y + 20)])
    pygame.draw.polygon(tela, (255, 220, 100), [(970, seta_y), (945, seta_y - 20), (945, seta_y + 20)])

    # Rodape
    pygame.draw.rect(tela, (0, 0, 0, 120), (0, 560, 1000, 40))
    rod = pygame.Surface((1000, 40), pygame.SRCALPHA)
    rod.fill((0, 0, 0, 150))
    tela.blit(rod, (0, 560))

    inst = fi.render(
        "ESQUERDA/DIREITA = Categoria  |  CIMA/BAIXO = Sub-item  |  ESC = Voltar ao Menu",
        True, (180, 180, 190),
    )
    tela.blit(inst, inst.get_rect(center=(500, 580)))