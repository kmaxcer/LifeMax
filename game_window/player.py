import pygame
import pygame as pg
from camera import PlayerCamera
from constants import *
from rays import ray_cast


class Player(PlayerCamera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        super().__init__(app, position, yaw, pitch)

        # player states
        self.is_standing: bool = False
        self.is_falling: bool = True
        self.is_flying: bool = False

    def update(self) -> None:
        self.keyboard_control()
        self.mouse_control()
        self.check_collisions()
        if self.is_falling:
            self.player_vel += glm.vec3(0, -0.002 * self.app.delta_time, 0)
        else:
            self.player_vel *= glm.vec3(1, 0, 1)
        deltatime = self.app.delta_time

        self.move_player()
        self.apply_friction(deltatime)
        self.move_player()
        self.apply_friction(deltatime)
        self._update()

    def check_collisions(self) -> None:
        return
        # bottom collision
        r_d = [glm.vec3(PLAYER_WIDTH / 2, 0, PLAYER_WIDTH / 2), glm.vec3(-PLAYER_WIDTH / 2, 0, PLAYER_WIDTH / 2),
               glm.vec3(PLAYER_WIDTH / 2, 0, -PLAYER_WIDTH / 2), glm.vec3(-PLAYER_WIDTH / 2, 0, -PLAYER_WIDTH / 2)]

        results = [(None, -1)]
        for displacement in r_d:
            t = ray_cast(self.position + glm.vec3(0, PLAYER_HEIGHT / 2, 0) + displacement, self.position + displacement)
            if t[0]:
                results.append(t[-1])

        new_y = max(results, key=lambda n: n[1])[1]
        if new_y != -1:
            self.position.y = new_y + 0.001
            self.is_falling = False
            self.is_standing = True
        else:
            self.is_falling = True
            self.is_standing = False
