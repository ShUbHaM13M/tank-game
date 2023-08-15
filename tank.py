import pygame as pg
from settings import RES, PLAYER_WIDTH, PLAYER_HEIGHT


class Tank:
    def __init__(self, game) -> None:
        self.game = game
        self.x = RES[0] * 0.5
        self.y = RES[0] * 0.5
        self.speed = 0.5

    def check_bounds(self):
        if self.x - PLAYER_WIDTH * 0.5 < 0:
            self.x = 0
        elif self.x + PLAYER_WIDTH > RES[0]:
            pass

    def render(self):
        pg.draw.rect(
            self.game.screen,
            "red",
            (
                self.x - PLAYER_WIDTH * 0.5,
                self.y - PLAYER_WIDTH * 0.5,
                PLAYER_WIDTH,
                PLAYER_HEIGHT,
            ),
        )

    def update(self):
        self.check_events()

    def check_events(self):
        keys = pg.key.get_pressed()
        delta_time = self.game.delta_time

        if keys[pg.K_d]:
            self.x += self.speed * delta_time
        elif keys[pg.K_a]:
            self.x -= self.speed * delta_time

        elif keys[pg.K_w]:
            self.y -= self.speed * delta_time
        elif keys[pg.K_s]:
            self.y += self.speed * delta_time
