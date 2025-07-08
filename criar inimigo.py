import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Exemplo de Inimigos")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Classe do Inimigo
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
        # Reseta a posição se sair da tela
        if self.rect.top > altura:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.velocidade = random.randint(2, 6)

# Grupo de sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()

# Criar vários inimigos
for i in range(5):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

# Loop principal
rodando = True
while rodando:
    clock.tick(FPS)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar inimigos
    todos_sprites.update()

    # Desenhar
    tela.fill(BRANCO)
    todos_sprites.draw(tela)
    pygame.display.flip()

pygame.quit()
