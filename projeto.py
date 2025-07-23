import pygame
import sys
import random

# === CONFIGURAÇÕES INICIAIS ===
pygame.init()
LARGURA, ALTURA = 800, 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Spacial GAME")
clock = pygame.time.Clock()

# === TELA INICIAL ===
def tela_inicial():
    fonte_titulo = pygame.font.Font("/home/nati-cb/Exercicio-GAME/fonte/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 75)
    fonte_instrucao = pygame.font.Font("/home/nati-cb/Exercicio-GAME/fonte/pixelart.ttf", 25)
    titulo = fonte_titulo.render("SPACIAL GAME", True, (178, 34, 34))
    instrucao = fonte_instrucao.render("Pressione ENTER para começar", True, (255, 140, 0))

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

        TELA.blit(fundo, (0, 0))
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//3))
        TELA.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA//2))
        pygame.display.flip()
        clock.tick(60)





# === CARREGAMENTO DE IMAGENS ===
fundo = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/fundo02.jpg").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

nave = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/nave1.png").convert_alpha()
nave = pygame.transform.scale(nave, (60, 60))
nave_rect = nave.get_rect(center=(LARGURA // 2, ALTURA - 80))

inimigo_img = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/inimigo1.png").convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (60, 60))

coracao_img = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/coração.png").convert_alpha()
coracao_img = pygame.transform.scale(coracao_img, (30, 30))

# === VELOCIDADES E TIROS ===
velocidade = 6
velocidade_tiro = 14
tiros = []

# === CLASSE: CHEFE FINAL ===
class Chefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/chefe-inimigo-Photoroom.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(center=(LARGURA // 2, -100))
        self.vida = 10
        self.velocidade = 3
        self.direcao = 1
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_tiro = 1000

    def update(self):
        if self.rect.top < 50:
            self.rect.y += 2
        else:
            self.rect.x += self.velocidade * self.direcao
            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.direcao *= -1

    def pode_atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro >= self.intervalo_tiro:
            self.tempo_ultimo_tiro = agora
            return True
        return False

# === CLASSE: INIMIGOS ===
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = inimigo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(2, 6)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, LARGURA - self.rect.width)
            self.velocidade = random.randint(2, 6)

# === FUNÇÃO PRINCIPAL DO JOGO ===
def main():
    # === VARIÁVEIS ===
    inimigos = pygame.sprite.Group()
    pontuacao = 0
    vida = 3
    chefe = None
    chefe_ativo = False
    tiros_chefe = []

    intervalo_inimigo = 5000
    tempo_ultimo_inimigo = pygame.time.get_ticks()

    font_path = "/home/nati-cb/Exercicio-GAME/fonte/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf"
    fonte = pygame.font.Font(font_path, 25)

    # Controle de dano
    dano = False
    tempo_dano = 0
    tempo_dano_max = 300

    # === FUNÇÕES INTERNAS ===
    def desenhar_coracoes(tela, x, y, vida):
        for i in range(vida):
            tela.blit(coracao_img, (x + i * 35, y))

    def desenhar_pontuacao(tela, pontos):
        texto = fonte.render(f'Pontuação: {pontos}', True, (255, 255, 255))
        tela.blit(texto, (10, 10))

    # === LOOP DO JOGO ===
    rodando = True
    while rodando:
        clock.tick(60)
        tempo_atual = pygame.time.get_ticks()

        # Geração de inimigos
        if tempo_atual - tempo_ultimo_inimigo > intervalo_inimigo:
            if len(inimigos) < 1:
                inimigos.add(Inimigo())
                tempo_ultimo_inimigo = tempo_atual

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimento da nave
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= velocidade
        if teclas[pygame.K_RIGHT] and nave_rect.right < LARGURA:
            nave_rect.x += velocidade
        if teclas[pygame.K_UP] and nave_rect.top > 0:
            nave_rect.y -= velocidade
        if teclas[pygame.K_DOWN] and nave_rect.bottom < ALTURA:
            nave_rect.y += velocidade
        if teclas[pygame.K_SPACE] and len(tiros) < 3:
            novo_tiro = pygame.Rect(nave_rect.centerx - 2, nave_rect.top, 5, 10)
            tiros.append(novo_tiro)

        # Atualiza inimigos
        inimigos.update()

        # Atualiza tiros da nave
        for tiro in tiros[:]:
            tiro.y -= velocidade_tiro
            if tiro.bottom < 0:
                tiros.remove(tiro)
            else:
                for inimigo in inimigos:
                    if tiro.colliderect(inimigo.rect):
                        tiros.remove(tiro)
                        inimigos.remove(inimigo)
                        pontuacao += 100
                        break
                if chefe_ativo and chefe.rect.colliderect(tiro):
                    tiros.remove(tiro)
                    chefe.vida -= 1
                    if chefe.vida <= 0:
                        print("Chefe derrotado!")
                        chefe_ativo = False
                        pontuacao += 1000

        # Tiros do chefe
        for tiro in tiros_chefe[:]:
            tiro.y += 7
            if tiro.top > ALTURA:
                tiros_chefe.remove(tiro)
            elif tiro.colliderect(nave_rect) and not dano:
                vida -= 1
                dano = True
                tempo_dano = pygame.time.get_ticks()
                tiros_chefe.remove(tiro)

        # Ativar chefe quando pontuação for suficiente
        if not chefe_ativo and pontuacao >= 1000:
            chefe = Chefe()
            chefe_ativo = True

        # Colisão com inimigos
        for inimigo in inimigos:
            if inimigo.rect.colliderect(nave_rect):
                inimigos.remove(inimigo)
                vida -= 1
                dano = True
                tempo_dano = pygame.time.get_ticks()
                if vida <= 0:
                    print("GAME OVER")
                    rodando = False
                break

        # Atualiza chefe e tiros
        if chefe_ativo:
            chefe.update()
            if chefe.pode_atirar():
                tiro = pygame.Rect(chefe.rect.centerx - 5, chefe.rect.bottom, 10, 15)
                tiros_chefe.append(tiro)

        # === DESENHAR TELA ===
        TELA.blit(fundo, (0, 0))

        # Nave piscando se levou dano
        if dano:
            if pygame.time.get_ticks() - tempo_dano < tempo_dano_max:
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    TELA.blit(nave, nave_rect)
            else:
                dano = False
                TELA.blit(nave, nave_rect)
        else:
            TELA.blit(nave, nave_rect)

        # Desenha chefe e inimigos
        if chefe_ativo:
            TELA.blit(chefe.image, chefe.rect)
        inimigos.draw(TELA)

        # Desenha tiros
        for tiro in tiros:
            pygame.draw.rect(TELA, (0, 160, 255), tiro)
        for tiro in tiros_chefe:
            pygame.draw.rect(TELA, (255, 0, 0), tiro)

        # HUD (pontuação e vidas)
        desenhar_pontuacao(TELA, pontuacao)
        desenhar_coracoes(TELA, 10, 50, vida)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# === EXECUÇÃO ===
if __name__ == "__main__":
    tela_inicial()
    main()
