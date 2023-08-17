import pygame as pg
from settings import RES
import math
import os


def clamp(num, min, max):
    return min if num < min else max if num > max else num


class Tank(pg.sprite.Sprite):
    def __init__(self, game) -> None:
        pg.sprite.Sprite.__init__(self)
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
        self.rect = self.image.get_rect()

        self.barrel_image = pg.image.load(
            os.path.join("assets", "tankBlue_barrel2.png")
        ).convert()
        self.barrel_image = pg.transform.rotate(
            pg.transform.scale_by(self.barrel_image, (0.8, 0.8)), 90
        )
        self.barrel_image.set_colorkey((0, 0, 0))

        self.barrel_pos = [self.x, self.y]
        self.barrel_rect = self.barrel_image.get_rect()

        self.speed = 0.2
        self.velocity = [0, 0]
        self.gun_angle = 0

    def render(self):
        self.game.screen.blit(
            pg.transform.rotate(self.image, self.angle),
            (self.x - self.width * 0.5, self.y - self.height * 0.5),
        )
        # self.game.screen.blit(
        #     self.barrel_image,
        #     self.barrel_pos,
        # )

    def update(self):
        self.movement()
        self.gun_movement()

    def rotate(self):
        pos = self.x, self.y

        width = self.barrel_image.get_width()
        height = self.barrel_image.get_height()
        box = [
            pg.math.Vector2(p)
            for p in [(0, 0), (width, 0), (width, -height), (0, -height)]
        ]

        box_rotate = [p.rotate(self.gun_angle) for p in box]

        min_box = [
            min(box_rotate, key=lambda p: p[0])[0],
            min(box_rotate, key=lambda p: p[1])[1],
        ]

        max_box = [
            max(box_rotate, key=lambda p: p[0])[0],
            max(box_rotate, key=lambda p: p[1])[1],
        ]

        pivot = pg.math.Vector2(0, 0)
        pivot_rotate = pivot.rotate(self.gun_angle)
        pivot_move = pivot_rotate - pivot

        origin = (
            pos[0] + min_box[0] - pivot_move[0],
            pos[1] - max_box[1] + pivot_move[1],
        )

        rotated_image = pg.transform.rotate(self.barrel_image, self.gun_angle)
        return rotated_image, origin

    def gun_movement(self):
        mouse_pos = pg.mouse.get_pos()
        angle = -(math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x))
        self.gun_angle = math.degrees(angle)
        barrel_image, origin = self.rotate()
        self.game.screen.blit(
            barrel_image,
            origin,
        )

    def shoot(self):
        print("pew pew")

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
