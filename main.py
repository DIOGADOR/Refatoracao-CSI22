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
HAZARD_IMAGE_PATHS = [
    "Images/nave.png",
    "Images/satelite.png",
    "Images/cometa.png",
    "Images/planeta.png",
    "Images/ameaca.png",
]


class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """

    def __init__(self):
        self.image = pygame.image.load("Images/background.png").convert()

        margin_left_fig = pygame.image.load("Images/margin_1.png").convert()
        margin_left_fig = pygame.transform.scale(
            margin_left_fig, (MARGIN_WIDTH, BACKGROUND_TILE_HEIGHT)
        )
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png").convert()
        margin_right_fig = pygame.transform.scale(
            margin_right_fig, (MARGIN_WIDTH, BACKGROUND_TILE_HEIGHT)
        )
        self.margin_right = margin_right_fig
    # __init__()

    def draw(self, screen, movL_x, movL_y, movR_x, movR_y):
        step_height = BACKGROUND_TILE_HEIGHT
        max_offset = -8 * step_height
        offsets = range(max_offset, screen.get_height() + step_height, step_height)
        for offset in offsets:
            screen.blit(self.image, (movL_x, movL_y + offset))
            screen.blit(self.margin_left, (movL_x, movL_y + offset))
            screen.blit(self.margin_right, (movR_x, movR_y + offset))
    # draw()
# Background:


class Player:
    """
    Classe Jogador
    """

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png").convert()
        player_fig = pygame.transform.scale(
            player_fig, (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self.image = player_fig
        self.x = x
        self.y = y
    # __init__()

    def update(self, mudar_x):
        self.x += mudar_x
    # update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    # draw()
# Player:


class Hazard:

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img).convert()
        hazard_fig = pygame.transform.scale(
            hazard_fig, (HAZARD_WIDTH, HAZARD_HEIGHT)
        )
        self.image = hazard_fig
        self.x = x
        self.y = y
    # __init__()

    def update(self, dy):
        self.y += dy
    # update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    # draw()
# Hazard:


class Game:

    WIDTH = SCREEN_WIDTH
    HEIGHT = SCREEN_HEIGHT
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    VELOCIDADE_BACKGROUND = BACKGROUND_SPEED
    VELOCIDADE_HAZARD = HAZARD_SPEED
    H_WIDTH = HAZARD_WIDTH
    H_HEIGHT = HAZARD_HEIGHT

    def __init__(self):
        """
        Inicializa o pygame, define a resolução da tela, caption e
        desabilita o mouse.
        """
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Viagem Espacial')

        my_font = pygame.font.Font("Fonts/Fonte4.ttf", MESSAGE_FONT_SIZE)
        self.render_text_bateulateral = my_font.render("COLISÃO!", 0, (255, 255, 255))
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0))
        self.score_font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

        self.run = True
        self.background = None
        self.player = None
        self.hazards = []
        self.mudar_x = 0.0

        # Estado do hazard ativo
        self.hzrd = 0
        self.h_x = 0
        self.h_y = 0

        # Estado do scroll do background
        self.movL_x = 0
        self.movL_y = 0
        self.movR_x = MARGIN_RIGHT_X
        self.movR_y = 0

        # Pontuação
        self.score = 0
        self.h_passou = 0
    # __init__()

    def handle_events(self):
        """
        Trata os eventos de input do jogador.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == self.ESQUERDA:
                    self.mudar_x = -PLAYER_SPEED
                if event.key == self.DIREITA:
                    self.mudar_x = PLAYER_SPEED

            if event.type == pygame.KEYUP:
                if event.key == self.ESQUERDA or event.key == self.DIREITA:
                    self.mudar_x = 0
    # handle_events()

    def score_card(self):
        """
        Renderiza o placar na tela.
        """
        passou = self.score_font.render(
            "Passou: " + str(self.h_passou), True, (255, 255, 128)
        )
        score = self.score_font.render(
            "Score: " + str(self.score), True, (253, 231, 32)
        )
        self.screen.blit(passou, (0, SCORE_LABEL_Y))
        self.screen.blit(score, (0, SCORE_VALUE_Y))
    # score_card()

    def _init_objects(self):
        """
        Instancia todos os objetos do jogo e reinicia o estado da partida.
        """
        self.background = Background()

        x_inicial = (self.WIDTH - PLAYER_WIDTH) / 2
        y_inicial = self.HEIGHT - PLAYER_Y_OFFSET
        self.player = Player(x_inicial, y_inicial)

        self.h_x = random.randrange(HAZARD_SPAWN_X_MIN, HAZARD_SPAWN_X_MAX)
        self.h_y = HAZARD_START_Y
        self.hzrd = 0
        self.hazards = [Hazard(path, self.h_x, self.h_y) for path in HAZARD_IMAGE_PATHS]

        self.movL_x = 0
        self.movL_y = 0
        self.movR_x = MARGIN_RIGHT_X
        self.movR_y = 0

        self.score = 0
        self.h_passou = 0
        self.mudar_x = 0.0
    # _init_objects()

    def _update_physics(self):
        """
        Atualiza as posições do background, do player e do hazard ativo.
        """
        # Scroll do background
        self.movL_y += self.VELOCIDADE_BACKGROUND
        self.movR_y += self.VELOCIDADE_BACKGROUND
        if self.movL_y > self.HEIGHT and self.movR_y > self.HEIGHT:
            self.movL_y -= self.HEIGHT
            self.movR_y -= self.HEIGHT

        # Movimento do player
        self.player.update(self.mudar_x)

        # Movimento do hazard ativo
        active_hazard = self.hazards[self.hzrd]
        active_hazard.x = self.h_x
        active_hazard.y = self.h_y
        active_hazard.update(HAZARD_SPEED_STEP)
        self.h_x = active_hazard.x
        self.h_y = active_hazard.y

        # Reposiciona hazard ao sair da tela e atualiza pontuação
        if self.h_y > self.HEIGHT:
            self.h_y = -self.H_HEIGHT
            self.h_x = random.randrange(
                HAZARD_SPAWN_X_MIN, HAZARD_SPAWN_X_MAX - self.H_HEIGHT
            )
            self.hzrd = random.randint(0, len(self.hazards) - 1)
            self.h_passou += 1
            self.score = self.h_passou * 10
    # _update_physics()

    def _check_collisions(self):
        """
        Verifica colisões laterais e com hazards. Encerra ou reinicia conforme
        o tipo de colisão.
        """
        # Colisão com a lateral
        bateu_lateral = (
            self.player.x > PLAY_AREA_RIGHT or self.player.x < PLAY_AREA_LEFT
        )
        if bateu_lateral:
            if self.player.x > PLAY_AREA_RIGHT:
                self.player.x = PLAY_AREA_RIGHT
            else:
                self.player.x = PLAY_AREA_LEFT
            self.screen.blit(
                self.render_text_bateulateral, (MESSAGE_POS_X, MESSAGE_POS_Y)
            )
            pygame.display.update()
            time.sleep(3)
            self._init_objects()
            return

        # Colisão com hazard (game over)
        px, py = self.player.x, self.player.y
        colidiu = (
            px < self.h_x + self.H_WIDTH
            and px + PLAYER_WIDTH > self.h_x
            and py < self.h_y + self.H_HEIGHT
            and py + PLAYER_HEIGHT > self.h_y
        )
        if colidiu:
            self.screen.blit(
                self.render_text_perdeu, (MESSAGE_POS_X, MESSAGE_POS_Y)
            )
            pygame.display.update()
            time.sleep(3)
            self.run = False
    # _check_collisions()

    def _render(self):
        """
        Desenha todos os elementos visuais na tela.
        """
        self.background.draw(
            self.screen, self.movL_x, self.movL_y, self.movR_x, self.movR_y
        )
        self.player.draw(self.screen)
        self.hazards[self.hzrd].x = self.h_x
        self.hazards[self.hzrd].y = self.h_y
        self.hazards[self.hzrd].draw(self.screen)
        self.score_card()
    # _render()

    def loop(self):
        """
        Laço principal: inicializa os objetos e executa o ciclo do jogo.
        """
        self._init_objects()
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(1000 / FPS_DT_MS)
            self.handle_events()
            self._update_physics()
            self._render()
            self._check_collisions()
            pygame.display.update()
        # while self.run
    # loop()
# Game:


def main():
    game = Game()
    game.loop()
# main()


if __name__ == '__main__':
    main()