"""
Spacial GAME - Jogo de Nave Espacial 2D em Pygame.

Controles:
  - Setas Direcionais: Movimentam a nave
  - Barra de Espaço: Dispara projéteis
  - R: Reinicia a partida na tela de Game Over
  - ESC: Encerra o jogo
"""

import sys
import random
from pathlib import Path
from typing import List, Optional
import pygame

# === DIRETÓRIOS DE RECURSOS ===
BASE_DIR = Path(__file__).resolve().parent
FONTES_DIR = BASE_DIR / "fonte"
IMAGENS_DIR = BASE_DIR / "imagem"

# === CONFIGURAÇÕES E CONSTANTES GLOBAIS ===
LARGURA_TELA: int = 800
ALTURA_TELA: int = 800
FPS: int = 60

# Cores no formato RGB
COR_TITULO = (178, 34, 34)
COR_INSTRUCAO = (255, 140, 0)
COR_GAMEOVER = (255, 0, 0)
COR_INFO = (128, 0, 0)
COR_TIRO_JOGADOR = (255, 215, 0)
COR_TIRO_CHEFE = (127, 255, 0)
COR_BRANCO = (255, 255, 255)
COR_VERDE_CLARO = (144, 238, 144)
COR_VERDE = (0, 255, 0)
COR_VERDE_ESCURO = (0, 100, 0)

# Parâmetros de Gameplay
VELOCIDADE_JOGADOR: int = 6
VELOCIDADE_TIRO_JOGADOR: int = 14
MAX_TIROS_SIMULTANEOS: int = 3
INTERVALO_SPAWN_INIMIGO_MS: int = 5000
INTERVALO_SPAWN_METEORO_MS: int = 5000
DURACAO_INVULNERABILIDADE_MS: int = 300
PONTOS_POR_INIMIGO: int = 100
PONTOS_POR_CHEFE: int = 500
INTERVALO_PONTOS_CHEFE: int = 1500

# === INICIALIZAÇÃO DO PYGAME ===
pygame.init()
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Spacial GAME")
clock = pygame.time.Clock()

# === CAMINHOS DOS ARQUIVOS DE FONTE ===
FONTE_VARIAVEL = str(FONTES_DIR / "Pixelify_Sans" / "PixelifySans-VariableFont_wght.ttf")
FONTE_PIXEL = str(FONTES_DIR / "pixelart.ttf")


def carregar_imagem(caminho_relativo: Path, dimensoes: Optional[tuple[int, int]] = None, com_alpha: bool = True) -> pygame.Surface:
    """Carrega uma imagem garantindo a conversão de formato e redimensionamento."""
    if not caminho_relativo.exists():
        raise FileNotFoundError(f"Arquivo de imagem não encontrado: {caminho_relativo}")
    img = pygame.image.load(str(caminho_relativo))
    img = img.convert_alpha() if com_alpha else img.convert()
    if dimensoes:
        img = pygame.transform.scale(img, dimensoes)
    return img


# === CARREGAMENTO SEGURO DE TEXTURAS ===
fundo_jogo = carregar_imagem(IMAGENS_DIR / "fundo2.png", (LARGURA_TELA, ALTURA_TELA), com_alpha=False)
fundo_game_over = carregar_imagem(IMAGENS_DIR / "gamerover.png", (LARGURA_TELA, ALTURA_TELA), com_alpha=False)
nave_img = carregar_imagem(IMAGENS_DIR / "nave1.png", (60, 60))
inimigo_img = carregar_imagem(IMAGENS_DIR / "inimigo1.png", (60, 60))
coracao_img = carregar_imagem(IMAGENS_DIR / "coração.png", (30, 30))
chefe_img = carregar_imagem(IMAGENS_DIR / "chefe-inimigo-Photoroom.png", (120, 120))
meteoro_img = carregar_imagem(IMAGENS_DIR / "meteoro.png", (50, 50))


# === CLASSES DE SPRITES ===
class Chefe(pygame.sprite.Sprite):
    """Representa a entidade do chefe com movimentação horizontal e disparo periódico."""

    def __init__(self, vida_inicial: int = 10) -> None:
        super().__init__()
        self.image = chefe_img
        self.rect = self.image.get_rect(center=(LARGURA_TELA // 2, -100))
        self.vida_maxima = vida_inicial
        self.vida = vida_inicial
        self.velocidade = 3
        self.direcao = 1
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_tiro = 1000

    def update(self) -> None:
        if self.rect.top < 50:
            self.rect.y += 2
        else:
            self.rect.x += self.velocidade * self.direcao
            if self.rect.left <= 0 or self.rect.right >= LARGURA_TELA:
                self.direcao *= -1

    def pode_atirar(self) -> bool:
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro >= self.intervalo_tiro:
            self.tempo_ultimo_tiro = agora
            return True
        return False


class Meteorito(pygame.sprite.Sprite):
    """Representa meteoros caindo verticalmente na tela."""

    def __init__(self) -> None:
        super().__init__()
        self.image = meteoro_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, LARGURA_TELA - self.rect.width))
        self.rect.y = -self.rect.height
        self.velocidade = random.randint(3, 8)

    def update(self) -> None:
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.kill()


class Inimigo(pygame.sprite.Sprite):
    """Representa naves inimigas regulares."""

    def __init__(self) -> None:
        super().__init__()
        self.image = inimigo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, LARGURA_TELA - self.rect.width))
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(2, 6)

    def update(self) -> None:
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, max(0, LARGURA_TELA - self.rect.width))
            self.velocidade = random.randint(2, 6)


# === TELAS DO JOGO ===
def tela_inicial() -> None:
    """Exibe a tela de abertura e aguarda comando para iniciar o jogo."""
    fonte_titulo = pygame.font.Font(FONTE_VARIAVEL, 75)
    fonte_instrucao = pygame.font.Font(FONTE_PIXEL, 25)
    titulo = fonte_titulo.render("SPACIAL GAME", True, COR_TITULO)
    instrucao = fonte_instrucao.render("Pressione ENTER para começar", True, COR_INSTRUCAO)

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

        TELA.blit(fundo_jogo, (0, 0))
        TELA.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 3))
        TELA.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 2))
        pygame.display.flip()
        clock.tick(FPS)


def game_over() -> bool:
    """
    Exibe a tela de fim de jogo.
    Retorna True se o jogador escolher reiniciar (tecla R), ou False caso deseje sair.
    """
    fonte_gameover = pygame.font.Font(FONTE_VARIAVEL, 80)
    fonte_info = pygame.font.Font(FONTE_PIXEL, 20)

    texto_gameover = fonte_gameover.render("GAME OVER", True, COR_GAMEOVER)
    texto_info = fonte_info.render("Pressione R para reiniciar ou ESC para sair", True, COR_INFO)

    while True:
        TELA.blit(fundo_game_over, (0, 0))
        TELA.blit(texto_gameover, (LARGURA_TELA // 2 - texto_gameover.get_width() // 2, ALTURA_TELA // 3))
        TELA.blit(texto_info, (LARGURA_TELA // 2 - texto_info.get_width() // 2, ALTURA_TELA // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_r:
                    return True
        clock.tick(FPS)


def desenhar_coracoes(tela: pygame.Surface, x: int, y: int, vidas: int) -> None:
    """Renderiza a quantidade de vidas restantes como ícones de coração."""
    for i in range(max(0, vidas)):
        tela.blit(coracao_img, (x + i * 35, y))


def desenhar_barra_vida(tela: pygame.Surface, chefe: Chefe) -> None:
    """Renderiza a barra de vida acima da entidade do chefe."""
    largura_barra = 120
    altura_barra = 15
    pos_x = chefe.rect.centerx - largura_barra // 2
    pos_y = chefe.rect.top - 20

    vida_max = max(1, chefe.vida_maxima)
    vida_atual = max(0, min(chefe.vida, vida_max))
    proporcao = vida_atual / vida_max
    largura_vida = int(largura_barra * proporcao)

    pygame.draw.rect(tela, (200, 0, 0), (pos_x, pos_y, largura_barra, altura_barra))
    pygame.draw.rect(tela, COR_VERDE, (pos_x, pos_y, largura_vida, altura_barra))
    pygame.draw.rect(tela, COR_VERDE_CLARO, (pos_x, pos_y, largura_barra, altura_barra), 2)


# === LOOP PRINCIPAL DA PARTIDA ===
def executar_partida() -> bool:
    """
    Executa uma rodada do jogo.
    Retorna True se o jogador escolher reiniciar na tela de Game Over, ou False para sair.
    """
    nave_rect = nave_img.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 80))

    inimigos = pygame.sprite.Group()
    meteoritos = pygame.sprite.Group()
    todos_sprites = pygame.sprite.Group()

    tiros_jogador: List[pygame.Rect] = []
    tiros_chefe: List[pygame.Rect] = []

    pontuacao = 0
    vidas = 3
    chefe: Optional[Chefe] = None
    chefe_ativo = False
    chefe_vida_base = 10
    pontuacao_ultima_aparicao = 0

    tempo_ultimo_inimigo = pygame.time.get_ticks()
    dano = False
    tempo_dano = 0

    fonte_hud = pygame.font.Font(FONTE_VARIAVEL, 25)

    EVENTO_METEORITO = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_METEORITO, INTERVALO_SPAWN_METEORO_MS)

    partida_ativa = True
    while partida_ativa:
        clock.tick(FPS)
        tempo_atual = pygame.time.get_ticks()

        # Geração contínua de inimigos regulares
        if tempo_atual - tempo_ultimo_inimigo > INTERVALO_SPAWN_INIMIGO_MS:
            if len(inimigos) < 1:
                novo_inimigo = Inimigo()
                inimigos.add(novo_inimigo)
                tempo_ultimo_inimigo = tempo_atual

        # Processamento de eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.time.set_timer(EVENTO_METEORITO, 0)
                pygame.quit()
                sys.exit(0)
            elif evento.type == EVENTO_METEORITO:
                m = Meteorito()
                todos_sprites.add(m)
                meteoritos.add(m)

        # Movimento e ações da nave do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_RIGHT] and nave_rect.right < LARGURA_TELA:
            nave_rect.x += VELOCIDADE_JOGADOR
        if teclas[pygame.K_UP] and nave_rect.top > 0:
            nave_rect.y -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_DOWN] and nave_rect.bottom < ALTURA_TELA:
            nave_rect.y += VELOCIDADE_JOGADOR
        if teclas[pygame.K_SPACE] and len(tiros_jogador) < MAX_TIROS_SIMULTANEOS:
            novo_tiro = pygame.Rect(nave_rect.centerx - 2, nave_rect.top, 5, 10)
            tiros_jogador.append(novo_tiro)

        # Atualizações de estado dos sprites
        inimigos.update()
        todos_sprites.update()

        # Atualização dos tiros do jogador
        for tiro in tiros_jogador[:]:
            tiro.y -= VELOCIDADE_TIRO_JOGADOR
            if tiro.bottom < 0:
                tiros_jogador.remove(tiro)
            else:
                for inimigo in inimigos:
                    if tiro.colliderect(inimigo.rect):
                        tiros_jogador.remove(tiro)
                        inimigos.remove(inimigo)
                        pontuacao += PONTOS_POR_INIMIGO
                        break
                if chefe_ativo and chefe and chefe.rect.colliderect(tiro):
                    if tiro in tiros_jogador:
                        tiros_jogador.remove(tiro)
                    chefe.vida -= 1
                    if chefe.vida <= 0:
                        chefe_ativo = False
                        chefe = None
                        pontuacao += PONTOS_POR_CHEFE

        # Atualização dos tiros do chefe
        for tiro in tiros_chefe[:]:
            tiro.y += 7
            if tiro.top > ALTURA_TELA:
                tiros_chefe.remove(tiro)
            elif tiro.colliderect(nave_rect) and not dano:
                vidas -= 1
                dano = True
                tempo_dano = pygame.time.get_ticks()
                tiros_chefe.remove(tiro)

        # Mecânica de invocação do chefe
        if not chefe_ativo and pontuacao >= pontuacao_ultima_aparicao + INTERVALO_PONTOS_CHEFE:
            chefe = Chefe(vida_inicial=chefe_vida_base)
            chefe_vida_base += 5
            chefe_ativo = True
            pontuacao_ultima_aparicao = pontuacao

        # Colisões da nave com inimigos
        for inimigo in inimigos:
            if inimigo.rect.colliderect(nave_rect):
                inimigos.remove(inimigo)
                vidas -= 1
                dano = True
                tempo_dano = pygame.time.get_ticks()
                break

        # Colisões da nave com meteoritos
        for meteorito in meteoritos:
            if meteorito.rect.colliderect(nave_rect) and not dano:
                vidas -= 1
                dano = True
                tempo_dano = pygame.time.get_ticks()
                meteorito.kill()

        # Verificação de derrota
        if vidas <= 0:
            pygame.time.set_timer(EVENTO_METEORITO, 0)
            return game_over()

        # Atualização da inteligência do chefe
        if chefe_ativo and chefe:
            chefe.update()
            if chefe.pode_atirar():
                tiro_novo = pygame.Rect(chefe.rect.centerx - 5, chefe.rect.bottom, 10, 15)
                tiros_chefe.append(tiro_novo)

        # === RENDERIZAÇÃO GRÁFICA ===
        TELA.blit(fundo_jogo, (0, 0))

        # Efeito de piscar da nave durante dano
        if dano:
            if pygame.time.get_ticks() - tempo_dano < DURACAO_INVULNERABILIDADE_MS:
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    TELA.blit(nave_img, nave_rect)
            else:
                dano = False
                TELA.blit(nave_img, nave_rect)
        else:
            TELA.blit(nave_img, nave_rect)

        # Renderização do chefe e seus atributos
        if chefe_ativo and chefe:
            desenhar_barra_vida(TELA, chefe)
            TELA.blit(chefe.image, chefe.rect)

        inimigos.draw(TELA)
        todos_sprites.draw(TELA)

        # Renderização de projéteis
        for tiro in tiros_jogador:
            pygame.draw.rect(TELA, COR_TIRO_JOGADOR, tiro)
        for tiro in tiros_chefe:
            pygame.draw.rect(TELA, COR_TIRO_CHEFE, tiro)

        # Interface do Usuário (HUD)
        texto_pontos = fonte_hud.render(f"Pontuação: {pontuacao}", True, COR_BRANCO)
        TELA.blit(texto_pontos, (10, 10))
        desenhar_coracoes(TELA, 10, 50, vidas)

        pygame.display.flip()

    pygame.time.set_timer(EVENTO_METEORITO, 0)
    return False


def main() -> None:
    """Função principal com suporte a ciclo completo de inicialização e reinício."""
    tela_inicial()
    while True:
        deve_reiniciar = executar_partida()
        if not deve_reiniciar:
            break
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
