import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Espacial com Imagens")
clock = pygame.time.Clock()

# Carregar imagens
fundo = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/fundo1.png").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

nave = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/nave1.png").convert_alpha()
nave = pygame.transform.scale(nave, (60, 60))  # Ajuste o tamanho se necessário
nave_rect = nave.get_rect(center=(LARGURA // 2, ALTURA - 80))

# Velocidade da nave
velocidade = 5

def main():
    rodando = True
    while rodando:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Controles
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= velocidade
        if teclas[pygame.K_RIGHT] and nave_rect.right < LARGURA:
            nave_rect.x += velocidade
        if teclas[pygame.K_UP] and nave_rect.top > 0:
            nave_rect.y -= velocidade
        if teclas[pygame.K_DOWN] and nave_rect.bottom < ALTURA:
            nave_rect.y += velocidade

        # Desenho
        TELA.blit(fundo, (0, 0))
        TELA.blit(nave, nave_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
