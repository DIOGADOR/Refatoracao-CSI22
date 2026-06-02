# Código para refatoração - Viagem Espacial

import pygame
import random
import time

class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """
     
    def __init__(self):

        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 600))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 600))
        self.margin_right = margin_right_fig
    # __init__()

    def update(self, dt):
        pass
    # update()

    # Renomeado de "move" para "draw"
    # Define posições do Plano de Fundo para criar o movimento
    def draw(self, screen, movL_x, movL_y, movR_x, movR_y):
        screen_height = screen.get_height()
        step_height = 600
        offsets = range(-4800, screen_height + step_height, step_height)
        for offset in offsets:
            screen.blit(self.image, (movL_x, movL_y + offset))
            screen.blit(self.margin_left, (movL_x, movL_y + offset))
            screen.blit(self.margin_right, (movR_x, movR_y + offset))

    # move()
# Background:

class Player:
    """
    Classe Jogador
    """
    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y
    # __init__()

    # Atualiza a posição do Player
    def update(self, mudar_x):
        self.x += mudar_x
    # update()

    # Desenhar Player (não recebe mais x e y externos)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    # draw()
# Player:

class Hazard:

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y
    # __init__()

    # Desenhar Hazard
    def draw (self, screen, x, y):
        screen.blit(self.image, (x, y))
    #draw()
# Hazard:

class Game:

    # Atributos de classe do Game
    WIDTH = 800
    HEIGHT = 600
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    VELOCIDADE_BACKGROUND = 5
    VELOCIDADE_HAZARD = 7
    H_WIDTH = 130
    H_HEIGHT = 130

    # TAREFA 4.8: Parâmetros size e fullscreen removidos da assinatura
    def __init__(self):
        """
        Função que inicializa o pygame, define a resolução da tela,
        caption, e desabilita o mouse.
        """
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # tamanho da tela
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Viagem Espacial')

        # fontes
        my_font = pygame.font.Font("Fonts/Fonte4.ttf", 100)

        # Mensagens para o jogador
        self.render_text_bateulateral = my_font.render("COLISÃO!", 0,(255, 255, 255))
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0))

        # Variáveis para o loop do jogo
        self.run = True
        self.background = None
        self.player = None
        self.hazard_1 = self.hazard_2 = self.hazard_3 = self.hazard_4 = self.hazard_5 = None
        self.mudar_x = 0.0
    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            # se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:
                if event.key == self.ESQUERDA:
                    self.mudar_x = -3
                if event.key == self.DIREITA:
                    self.mudar_x = 3

            # se soltar qualquer tecla, não faz nada
            if event.type == pygame.KEYUP:
                if event.key == self.ESQUERDA or event.key == self.DIREITA:
                    self.mudar_x = 0
    # handle_events()

    def elements_update(self, dt):
        self.background.update(dt)
    # elements_update()

    # Os métodos inúteis (elements_draw, draw_player e move_background) foram totalmente deletados daqui!

    # Desenha Hazard
    def draw_hazard (self, hzrd, x, y):
        if hzrd == 0:
            self.hazard_1.draw(self.screen, x, y)
        elif hzrd == 1:
            self.hazard_2.draw(self.screen, x, y)
        elif hzrd == 2:
            self.hazard_3.draw(self.screen, x, y)
        elif hzrd == 3:
            self.hazard_4.draw(self.screen, x, y)
        elif hzrd == 4:
            self.hazard_5.draw(self.screen, x, y)
    # draw_hazard()

    # Informa a quantidade de hazard que passaram e a Pontuação
    def score_card(self, screen, h_passou, score):
        font = pygame.font.SysFont(None, 35)
        passou = font.render("Passou: " + str(h_passou), True, (255, 255, 128))
        score = font.render("Score: " + str(score), True, (253, 231, 32))
        screen.blit(passou, (0, 50))
        screen.blit(score, (0, 100))
    #score_card()

    def loop(self):
        """
        Laço principal
        """
        score = 0
        h_passou = 0

        # variáveis para movimento de Plano de Fundo/Background
        hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o Plano de fundo
        self.background = Background()

        # Posicao INICIAL do Player
        x_inicial = (self.WIDTH - 56) / 2
        y_inicial = self.HEIGHT - 125

        # Criar o Player (o objeto agora guarda e atualiza seu x e y internamente)
        self.player = Player(x_inicial, y_inicial)

        # Criar Harzard_1 a 5
        self.hazard_1 = Hazard("Images/nave.png", h_x, h_y)
        self.hazard_2 = Hazard("Images/satelite.png", h_x, h_y)
        self.hazard_3 = Hazard("Images/cometa.png", h_x, h_y)
        self.hazard_4 = Hazard("Images/planeta.png", h_x, h_y)
        self.hazard_5 = Hazard("Images/ameaca.png", h_x, h_y)

        # Inicializamos o relogio e o dt
        clock = pygame.time.Clock()
        dt = 16

        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.elements_update(dt)

            # Fundo agora é renderizado e movido em uma única chamada coesa
            self.background.draw(self.screen, movL_x, movL_y, movR_x, movR_y)

            # incrementa eixo Y para rolar o fundo
            movL_y = movL_y + self.VELOCIDADE_BACKGROUND
            movR_y = movR_y + self.VELOCIDADE_BACKGROUND

            # se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > self.HEIGHT and movR_y > self.HEIGHT:
                movL_y -= self.HEIGHT
                movR_y -= self.HEIGHT

            # O Player processa sua física e desenha a si mesmo
            self.player.update(self.mudar_x)
            self.player.draw(self.screen)

            # Mostrar score
            self.score_card(self.screen, h_passou, score)

            # Restrições do movimento do Player (Acessando self.player.x encapsulado)
            if self.player.x > 760 - 92 or self.player.x < 40 + 5:
                self.screen.blit(self.render_text_bateulateral, (80, 200))
                pygame.display.update()  # atualizar a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # adicionando movimento ao hazard
            h_y = h_y + self.VELOCIDADE_HAZARD / 4
            self.draw_hazard(hzrd, h_x, h_y)
            h_y = h_y + self.VELOCIDADE_HAZARD

            # definindo onde hazard vai aparecer
            if h_y > self.HEIGHT:
                h_y = 0 - self.H_HEIGHT
                h_x = random.randrange(125, 650 - self.H_HEIGHT)
                hzrd = random.randint(0, 4)
                # determinando quantos hazard passaram e a pontuação
                h_passou = h_passou + 1
                score = h_passou * 10

            # restrições para o game over (Acessando self.player.y e self.player.x encapsulados)
            if self.player.y < h_y + self.H_HEIGHT:
                if self.player.x > h_x or self.player.x > h_x - 56:
                    if self.player.x < h_x + self.H_WIDTH or self.player.x < h_x - 56:
                        self.screen.blit(self.render_text_perdeu, (80, 200))
                        pygame.display.update()
                        time.sleep(3)
                        self.run = False

            # atualizando a tela
            pygame.display.update()
            clock.tick(2000)
        # while self.run
    # loop()
# Game:

def main():
    # Cria o objeto game e chama o loop básico
    game = Game()
    game.loop()
# main()

# Chama a função main
if __name__ == '__main__':
    main()