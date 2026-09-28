import pygame
from scripts.inventario import Inventario
from scripts.interfaces import (
    GerenciadorMensagens, desenhar_hud, desenhar_menu,
    desenhar_vitoria, desenhar_game_over, desenhar_construcao,
    desenhar_transicao, desenhar_selecao_personagens,
    CATEGORIAS_GALERIA,
)
from scripts.cenas import criar_cena

# ============================================
# CONFIGURACOES
# ============================================

LARGURA = 1000
ALTURA = 600
FPS = 60
TITULO = "Between Tides"

# Estados do jogo
MENU = "MENU"
TRANSICAO = "TRANSICAO"
JOGANDO = "JOGANDO"
GAME_OVER = "GAME_OVER"
CONSTRUINDO = "CONSTRUINDO"
VITORIA = "VITORIA"
GALERIA = "GALERIA"

# Codigo secreto para acessar a galeria de personagens
CODIGO_SECRETO = "MARETIDE"

NOMES_NIVEIS = {
    1: "Praia",
    1.5: "Caverna Secreta",
    2: "Floresta",
    3: "Caverna",
    4: "Montanha",
    5: "Costa",
}

CONSTRUCAO_DURACAO = 180   # 3 segundos
TRANSICAO_DURACAO = 90     # 1.5 segundos

# ============================================
# INICIALIZACAO
# ============================================

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()

# ============================================
# VARIAVEIS DO JOGO
# ============================================

estado = MENU
nivel_atual = 1
inventario = Inventario()
inventario_backup = Inventario()
mensagens = GerenciadorMensagens()
cena = None
cenas_ativas = {}
construcao_timer = 0
transicao_timer = 0

# Variaveis da galeria de personagens
codigo_buffer = ""
galeria_categoria = 0
galeria_sub = 0
galeria_anim = 0


def iniciar_nivel(nivel, vida=100, indo_frente=True):
    """Cria a cena do nivel e salva backup do inventario."""
    global cena, inventario_backup, cenas_ativas
    inventario_backup = inventario.copiar()
    mensagens.mensagens.clear()
    
    if nivel not in cenas_ativas:
        cenas_ativas[nivel] = criar_cena(nivel, tela, inventario, mensagens)
    else:
        cenas_ativas[nivel].inventario = inventario
        cenas_ativas[nivel].mensagens = mensagens
        
    cena = cenas_ativas[nivel]
    if cena and cena.jogador:
        cena.jogador.vida = vida
        
        # Posicionar jogador dependendo de onde veio
        if not indo_frente and cena.saida:
            cena.jogador.rect.right = cena.saida.left - 20
        elif indo_frente and cena.entrada:
            cena.jogador.rect.left = cena.entrada.right + 20
            
        cena.voltou = False
        cena.concluido = False


# ============================================
# LOOP PRINCIPAL
# ============================================

rodando = True

while rodando:

    # --- Eventos ---
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if estado == MENU:
                if evento.key == pygame.K_RETURN:
                    nivel_atual = 1
                    inventario = Inventario()
                    inventario_backup = Inventario()
                    cenas_ativas.clear()
                    iniciar_nivel(nivel_atual)
                    estado = TRANSICAO
                    transicao_timer = 0
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False
                else:
                    # Detectar codigo secreto
                    nome_tecla = pygame.key.name(evento.key).upper()
                    if len(nome_tecla) == 1 and nome_tecla.isalpha():
                        codigo_buffer += nome_tecla
                        # Manter apenas os ultimos N caracteres
                        codigo_buffer = codigo_buffer[-len(CODIGO_SECRETO):]
                        if codigo_buffer == CODIGO_SECRETO:
                            codigo_buffer = ""
                            galeria_categoria = 0
                            galeria_sub = 0
                            galeria_anim = 0
                            estado = GALERIA

            elif estado == GALERIA:
                if evento.key == pygame.K_ESCAPE:
                    estado = MENU
                elif evento.key == pygame.K_RIGHT:
                    galeria_categoria = (galeria_categoria + 1) % len(CATEGORIAS_GALERIA)
                    galeria_sub = 0
                elif evento.key == pygame.K_LEFT:
                    galeria_categoria = (galeria_categoria - 1) % len(CATEGORIAS_GALERIA)
                    galeria_sub = 0
                elif evento.key == pygame.K_DOWN:
                    galeria_sub += 1
                elif evento.key == pygame.K_UP:
                    galeria_sub -= 1

            elif estado == JOGANDO:
                if evento.key == pygame.K_ESCAPE:
                    estado = MENU
                    cena = None
                elif evento.key == pygame.K_SPACE:
                    if inventario.quantidade("espada") > 0:
                        cena.jogador.atacar()

            elif estado == GAME_OVER:
                if evento.key == pygame.K_RETURN:
                    inventario.restaurar(inventario_backup)
                    if nivel_atual in cenas_ativas:
                        del cenas_ativas[nivel_atual]
                    iniciar_nivel(nivel_atual)
                    estado = JOGANDO
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

            elif estado == VITORIA:
                if evento.key == pygame.K_RETURN:
                    nivel_atual = 1
                    inventario = Inventario()
                    inventario_backup = Inventario()
                    cenas_ativas.clear()
                    mensagens.mensagens.clear()
                    cena = None
                    estado = MENU
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

    # --- Atualizar e Desenhar ---

    if estado == MENU:
        desenhar_menu(tela)

    elif estado == TRANSICAO:
        desenhar_transicao(tela, nivel_atual, NOMES_NIVEIS.get(nivel_atual, ""))
        transicao_timer += 1
        if transicao_timer >= TRANSICAO_DURACAO:
            estado = JOGANDO

    elif estado == JOGANDO:
        if cena:
            cena.atualizar()
            cena.desenhar()

            desenhar_hud(
                tela, nivel_atual, cena.objetivo_texto,
                cena.jogador.vida, cena.jogador.vida_max,
                cena.get_progresso(), inventario.pontuacao
            )

            mensagens.atualizar()
            mensagens.desenhar(tela)

            # Morte
            if cena.jogador.vida <= 0:
                estado = GAME_OVER

            # Nivel completo (Avancar)
            if cena.concluido:
                vida_atual = cena.jogador.vida
                if hasattr(cena, 'foi_para_bonus') and cena.foi_para_bonus:
                    nivel_atual = 1.5
                    cena.foi_para_bonus = False
                elif nivel_atual == 1.5:
                    nivel_atual = 2
                else:
                    if nivel_atual < 5:
                        nivel_atual += 1
                    else:
                        estado = CONSTRUINDO
                        construcao_timer = 0
                        continue
                
                iniciar_nivel(nivel_atual, vida_atual, indo_frente=True)
                estado = TRANSICAO
                transicao_timer = 0

            # Voltar de nivel
            if cena.voltou:
                vida_atual = cena.jogador.vida
                if nivel_atual > 1 and nivel_atual != 1.5:
                    nivel_atual -= 1
                    iniciar_nivel(nivel_atual, vida_atual, indo_frente=False)
                    estado = TRANSICAO
                    transicao_timer = 0

    elif estado == GAME_OVER:
        desenhar_game_over(tela)

    elif estado == CONSTRUINDO:
        progresso = min(1.0, construcao_timer / CONSTRUCAO_DURACAO)
        desenhar_construcao(tela, progresso)
        construcao_timer += 1
        if construcao_timer >= CONSTRUCAO_DURACAO:
            estado = VITORIA

    elif estado == VITORIA:
        desenhar_vitoria(tela, inventario.pontuacao)

    elif estado == GALERIA:
        galeria_anim += 1
        desenhar_selecao_personagens(tela, galeria_categoria, galeria_sub, galeria_anim)

    # --- Exibir ---
    pygame.display.flip()
    clock.tick(FPS)

# ============================================
# ENCERRAMENTO
# ============================================

pygame.quit()