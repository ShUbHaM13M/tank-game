import pygame as pg
from settings import RES
import math
import os


def clamp(num, min, max):
    return min if num < min else max if num > max else num


class Tank:
    def __init__(self, game) -> None:
        self.game = game
        self.x = RES[0] * 0.5
        self.y = RES[1] * 0.5
        self.scale_factor = 0.6
        self.angle = 0

        self.image = pg.image.load(
            os.path.join("assets", "tankBody_blue.png")
        ).convert()
        self.image = pg.transform.rotate(
            pg.transform.scale_by(self.image, (self.scale_factor, self.scale_factor)),
            90,
        )
        self.image.set_colorkey((0, 0, 0))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.barrel_image = pg.image.load(
            os.path.join("assets", "tankBlue_barrel2.png")
        ).convert()
        self.barrel_image = pg.transform.scale_by(self.barrel_image, (0.8, 0.8))

        self.barrel_image.set_colorkey((0, 0, 0))

        self.speed = 0.5
        self.velocity = [0, 0]
        self.gun_angle = 0

    def render(self):
        self.game.screen.blit(
            pg.transform.rotate(self.image, self.angle),
            (self.x - self.width * 0.5, self.y - self.height * 0.5),
        )
        self.game.screen.blit(
            pg.transform.rotate(self.barrel_image, self.gun_angle),
            (
                self.x - self.barrel_image.get_width() * 0.5,
                self.y,
            ),
        )

    def update(self):
        self.movement()
        self.gun_movement()

    def gun_movement(self):
        mouse_pos = pg.mouse.get_pos()
        angle = math.atan2(
            mouse_pos[1] - self.y,
            mouse_pos[0] - self.x - self.barrel_image.get_width() * 0.5,
        )
        self.gun_angle = angle * (180 / math.pi)

    def movement(self):
        keys = pg.key.get_pressed()
        delta_time = self.game.delta_time

        if keys[pg.K_d]:
            self.velocity[0] = 1
            self.angle = 0
        elif keys[pg.K_a]:
            self.velocity[0] = -1
            self.angle = 180

        elif keys[pg.K_w]:
            self.velocity[1] = -1
            self.angle = 90
        elif keys[pg.K_s]:
            self.velocity[1] = 1
            self.angle = 270

        self.x += self.velocity[0] * self.speed * delta_time
        self.y += self.velocity[1] * self.speed * delta_time

        self.x = clamp(
            self.x,
            self.width * 0.5,
            RES[0] - self.width * 0.5,
        )
        self.y = clamp(
            self.y,
            self.height * 0.5,
            RES[1] - self.height * 0.5,
        )
        self.velocity = [0, 0]
