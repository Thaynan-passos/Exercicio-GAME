"""Exemplo de geração e movimentação contínua de inimigos na tela."""

import random
import pygame

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Exemplo de Inimigos")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60


class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(2, 6)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.velocidade = random.randint(2, 6)


todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()

for _ in range(5):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

rodando = True
while rodando:
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    todos_sprites.update()

    tela.fill(PRETO)
    todos_sprites.draw(tela)
    pygame.display.flip()

pygame.quit()
