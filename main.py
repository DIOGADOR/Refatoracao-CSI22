# Código para refatoração - Viagem Espacial

import pygame
import random
import time

# Constantes de layout e gameplay
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 90
HAZARD_WIDTH = 130
HAZARD_HEIGHT = 130
MARGIN_WIDTH = 60
BACKGROUND_TILE_HEIGHT = 600
MARGIN_RIGHT_X = 740
PLAY_AREA_LEFT = 45
PLAY_AREA_RIGHT = 668
HAZARD_SPAWN_X_MIN = 125
HAZARD_SPAWN_X_MAX = 660
HAZARD_START_Y = -500
PLAYER_Y_OFFSET = 125
PLAYER_SPEED = 3
BACKGROUND_SPEED = 5
HAZARD_SPEED = 7
HAZARD_SPEED_STEP = HAZARD_SPEED + HAZARD_SPEED / 4
SCORE_FONT_SIZE = 35
MESSAGE_FONT_SIZE = 100
MESSAGE_POS_X = 80
MESSAGE_POS_Y = 200
SCORE_LABEL_Y = 50
SCORE_VALUE_Y = 100
FPS_DT_MS = 16

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
        margin_left_fig = pygame.transform.scale(
            margin_left_fig, (MARGIN_WIDTH, BACKGROUND_TILE_HEIGHT)
        )
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(
            margin_right_fig, (MARGIN_WIDTH, BACKGROUND_TILE_HEIGHT)
        )
        self.margin_right = margin_right_fig
    # __init__()

    def update(self, dt):
        pass
    # update()

    # Renomeado de "move" para "draw"
    # Define posições do Plano de Fundo para criar o movimento
    def draw(self, screen, movL_x, movL_y, movR_x, movR_y):
        screen_height = screen.get_height()
        step_height = BACKGROUND_TILE_HEIGHT
        max_offset = -8 * step_height
        offsets = range(max_offset, screen_height + step_height, step_height)
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
        player_fig = pygame.transform.scale(
            player_fig, (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
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
        hazard_fig = pygame.transform.scale(
            hazard_fig, (HAZARD_WIDTH, HAZARD_HEIGHT)
        )
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
    WIDTH = SCREEN_WIDTH
    HEIGHT = SCREEN_HEIGHT
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    VELOCIDADE_BACKGROUND = BACKGROUND_SPEED
    VELOCIDADE_HAZARD = HAZARD_SPEED
    H_WIDTH = HAZARD_WIDTH
    H_HEIGHT = HAZARD_HEIGHT

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
        my_font = pygame.font.Font("Fonts/Fonte4.ttf", MESSAGE_FONT_SIZE)

        # Mensagens para o jogador
        self.render_text_bateulateral = my_font.render("COLISÃO!", 0,(255, 255, 255))
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0))
        self.score_font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

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
                    self.mudar_x = -PLAYER_SPEED
                if event.key == self.DIREITA:
                    self.mudar_x = PLAYER_SPEED

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
        passou = self.score_font.render(
            "Passou: " + str(h_passou), True, (255, 255, 128)
        )
        score = self.score_font.render(
            "Score: " + str(score), True, (253, 231, 32)
        )
        screen.blit(passou, (0, SCORE_LABEL_Y))
        screen.blit(score, (0, SCORE_VALUE_Y))
    #score_card()

    def _reset_round(
        self, score, h_passou, hzrd, h_x, h_y, movL_x, movL_y, movR_x, movR_y
    ):
        x_inicial = (self.WIDTH - PLAYER_WIDTH) / 2
        y_inicial = self.HEIGHT - PLAYER_Y_OFFSET
        self.player = Player(x_inicial, y_inicial)
        self.mudar_x = 0.0
        return (
            0,
            0,
            0,
            random.randrange(HAZARD_SPAWN_X_MIN, HAZARD_SPAWN_X_MAX),
            HAZARD_START_Y,
            0,
            0,
            MARGIN_RIGHT_X,
            0,
        )

    def _player_collides_with_hazard(self, h_x, h_y):
        px, py = self.player.x, self.player.y
        return (
            px < h_x + self.H_WIDTH
            and px + PLAYER_WIDTH > h_x
            and py < h_y + self.H_HEIGHT
            and py + PLAYER_HEIGHT > h_y
        )

    def loop(self):
        """
        Laço principal
        """
        score = 0
        h_passou = 0

        # variáveis para movimento de Plano de Fundo/Background
        hzrd = 0
        h_x = random.randrange(HAZARD_SPAWN_X_MIN, HAZARD_SPAWN_X_MAX)
        h_y = HAZARD_START_Y

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = MARGIN_RIGHT_X
        movR_y = 0

        # Criar o Plano de fundo
        self.background = Background()

        # Posicao INICIAL do Player
        x_inicial = (self.WIDTH - PLAYER_WIDTH) / 2
        y_inicial = self.HEIGHT - PLAYER_Y_OFFSET

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
        dt = FPS_DT_MS

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
            if self.player.x > PLAY_AREA_RIGHT or self.player.x < PLAY_AREA_LEFT:
                self.screen.blit(
                    self.render_text_bateulateral, (MESSAGE_POS_X, MESSAGE_POS_Y)
                )
                pygame.display.update()  # atualizar a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # adicionando movimento ao hazard (um único passo por frame)
            h_y = h_y + HAZARD_SPEED_STEP
            self.draw_hazard(hzrd, h_x, h_y)

            # definindo onde hazard vai aparecer
            if h_y > self.HEIGHT:
                h_y = 0 - self.H_HEIGHT
                h_x = random.randrange(
                    HAZARD_SPAWN_X_MIN, HAZARD_SPAWN_X_MAX - self.H_HEIGHT
                )
                hzrd = random.randint(0, 4)
                # determinando quantos hazard passaram e a pontuação
                h_passou = h_passou + 1
                score = h_passou * 10

            if self._player_collides_with_hazard(h_x, h_y):
                self.screen.blit(
                    self.render_text_perdeu, (MESSAGE_POS_X, MESSAGE_POS_Y)
                )
                pygame.display.update()
                time.sleep(3)
                self.run = False

            # atualizando a tela
            pygame.display.update()
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