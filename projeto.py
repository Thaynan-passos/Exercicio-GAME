import pygame
import sys
import random   

# Inicialização
pygame.init()

# Dimensões da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Spacial GAME")
clock = pygame.time.Clock()

# Carregando imagens
fundo = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/fundo1.png").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

nave = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/nave1.png").convert_alpha()
nave = pygame.transform.scale(nave, (60, 60)) 
nave_rect = nave.get_rect(center=(LARGURA // 2, ALTURA - 80))

inimigo_img = pygame.image.load("/home/nati-cb/Exercicio-GAME/imagem/inimigo1.png").convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))  # usar a mesma imagem na classe

# Velocidade da nave
velocidade = 5

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

# Função principal
def main():
    # Criar grupo de sprites
    # O que e uma sprite? e um objeto que pode ser desenhado na tela e pode se mover e coledir com outros objetos
    # Grupo de inimigos
    inimigos = pygame.sprite.Group()

    # Tempo para controlar a criação de inimigos
    intervalo_inimigo = 2000  # em milissegundos (2 segundos)
    tempo_ultimo_inimigo = pygame.time.get_ticks()
    
    
    
    
    
    
    
 
 
    


    rodando = True
    while rodando:
        clock.tick(60)

                # Tempo atual do jogo
        tempo_atual = pygame.time.get_ticks()

        # Cria um inimigo novo a cada 2 segundos
        if tempo_atual - tempo_ultimo_inimigo > intervalo_inimigo:
            inimigos.add(Inimigo())
            tempo_ultimo_inimigo = tempo_atual

        MAX_INIMIGOS = 20
        if len(inimigos) < MAX_INIMIGOS and tempo_atual - tempo_ultimo_inimigo > intervalo_inimigo:
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

        # Atualiza inimigos
        inimigos.update()

        # Desenha na tela
        TELA.blit(fundo, (0, 0))
        TELA.blit(nave, nave_rect)
        inimigos.draw(TELA)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Execução
if __name__ == "__main__":
    main()
