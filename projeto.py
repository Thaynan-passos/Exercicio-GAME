import pygame
import sys
import random

# Inicialização
pygame.init()

# Dimensões da tela, cria tela e define titulo
LARGURA, ALTURA = 800, 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Spacial GAME")
clock = pygame.time.Clock()

# Carregando imagens
fundo = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/fundo02.jpg").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

nave = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/nave1.png").convert_alpha()
nave = pygame.transform.scale(nave, (60, 60))
nave_rect = nave.get_rect(center=(LARGURA // 2, ALTURA - 80))

inimigo_img = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/inimigo1.png").convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (60, 60))

coracao_img = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/coração.png").convert_alpha()
coracao_img = pygame.transform.scale(coracao_img, (30, 30))

# Velocidade
velocidade = 6
velocidade_tiro = 14
tiros = []



# Classe Inimigo
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
# Função principal do jogo
def main():
    inimigos = pygame.sprite.Group()
    pontuacao = 0
    vida = 3

    intervalo_inimigo = 5000
    tempo_ultimo_inimigo = pygame.time.get_ticks()

    font_path = "/home/nati-cb/Exercicio-GAME/fonte/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf"
    fonte = pygame.font.Font(font_path, 25)

    # Variáveis de dano
    dano = False
    tempo_dano = 0
    tempo_dano_max = 300  # milissegundos

    def desenhar_coracoes(tela, x, y, vida):
        for i in range(vida):
            tela.blit(coracao_img, (x + i * 35, y))

    def desenhar_pontuacao(tela, Pontuacao):
        texto = fonte.render(f'Pontuação: {Pontuacao}', True, (255, 255, 255))
        tela.blit(texto, (10, 10))

    rodando = True
    while rodando:
        clock.tick(60)
        tempo_atual = pygame.time.get_ticks()

        # Cria inimigos com intervalo
        if tempo_atual - tempo_ultimo_inimigo > intervalo_inimigo:
            if len(inimigos) < 1:
                inimigos.add(Inimigo())
                tempo_ultimo_inimigo = tempo_atual

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
        if teclas[pygame.K_SPACE]:
            if len(tiros) < 3:
                novo_tiro = pygame.Rect(nave_rect.centerx - 2, nave_rect.top, 5, 10)
                tiros.append(novo_tiro)

        inimigos.update()

        # Atualiza posição dos tiros e verifica colisões com inimigos
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

        # Verifica colisão da nave com inimigos
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

        # Desenha tudo na tela
        TELA.blit(fundo, (0, 0))

        
        if dano:
            if pygame.time.get_ticks() - tempo_dano < tempo_dano_max:
                # Efeito piscar 
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    TELA.blit(nave, nave_rect)
            else:
                    dano = False
                    TELA.blit(nave, nave_rect)
        else:
                TELA.blit(nave, nave_rect)            
                   


        inimigos.draw(TELA)
        for tiro in tiros:
            pygame.draw.rect(TELA, (0, 160, 255), tiro)
        desenhar_pontuacao(TELA, pontuacao)
        desenhar_coracoes(TELA, 10, 50, vida)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Execução
if __name__ == "__main__":
    main()
