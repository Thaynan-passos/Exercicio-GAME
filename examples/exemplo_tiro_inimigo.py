"""Exemplo básico de movimentação, disparos e colisão de tiros com inimigos."""

import sys
import pygame

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Nave com Tiros")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

nave_largura, nave_altura = 50, 30
nave_x = LARGURA // 2 - nave_largura // 2
nave_y = ALTURA - nave_altura - 10
velocidade_nave = 5

tiros = []
velocidade_tiro = 7

inimigos = []
for i in range(5):
    inimigo = pygame.Rect(100 * i + 50, 50, 40, 40)
    inimigos.append(inimigo)


def desenhar_jogo():
    TELA.fill(PRETO)
    pygame.draw.rect(TELA, BRANCO, (nave_x, nave_y, nave_largura, nave_altura))

    for tiro in tiros:
        pygame.draw.rect(TELA, VERMELHO, tiro)

    for inimigo in inimigos:
        pygame.draw.rect(TELA, VERDE, inimigo)

    pygame.display.update()


rodando = True
while rodando:
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= velocidade_nave
    if teclas[pygame.K_RIGHT] and nave_x < LARGURA - nave_largura:
        nave_x += velocidade_nave

    if teclas[pygame.K_SPACE]:
        if len(tiros) < 20:
            novo_tiro = pygame.Rect(nave_x + nave_largura // 2 - 2, nave_y, 5, 10)
            tiros.append(novo_tiro)

    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro
        if tiro.y < 0:
            tiros.remove(tiro)

    for tiro in tiros[:]:
        for inimigo in inimigos[:]:
            if tiro.colliderect(inimigo):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                break

    desenhar_jogo()

pygame.quit()
sys.exit(0)
