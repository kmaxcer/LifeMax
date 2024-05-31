import glm
import pygame as pg

import custom_vec_functions
from constants import *
from frustum import Frustum


class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        self.frustum = Frustum(self)

    def _update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self):
        ...

    def move_right(self):
        ...

    def move_up(self):
        ...

    def move_down(self):
        ...

    def move_forward(self):
        ...

    def move_back(self):
        ...


class PlayerCamera(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)

        self.lock_mouse = False

        self.player_vel = glm.vec3(0, 0, 1)
        self.min_vel = 0.1  # Минимальное значение для вектора скорости

        self.is_flying = True

    def move_player(self):
        self.position += self.player_vel / 2

    def move_left(self):
        self.player_vel -= glm.normalize(self.right * glm.vec3(1, 0, 1)) * PLAYER_ACCELERATION * self.app.delta_time

    def move_right(self):
        self.player_vel += glm.normalize(self.right * glm.vec3(1, 0, 1)) * PLAYER_ACCELERATION * self.app.delta_time

    def move_forward(self):
        self.player_vel += glm.normalize(self.forward * glm.vec3(1, 0, 1)) * PLAYER_ACCELERATION * self.app.delta_time

    def move_back(self):
        self.player_vel -= glm.normalize(self.forward * glm.vec3(1, 0, 1)) * PLAYER_ACCELERATION * self.app.delta_time

    def move_down(self):
        self.position.y -= PLAYER_VERTICAL_SPEED

    def move_up(self):
        self.position.y += PLAYER_VERTICAL_SPEED

    def update(self):
        deltatime = self.app.delta_time
        self.keyboard_control()
        self.mouse_control()

        self.move_player()
        self.apply_friction(deltatime)
        self.move_player()
        self.apply_friction(deltatime)

        self._update()

    def apply_friction(self, deltatime):
        friction_vec = (1.0 - PLAYER_FRICTION) * custom_vec_functions.safe_normalize(self.player_vel)
        friction_vec *= deltatime
        if glm.length(friction_vec) > glm.length(self.player_vel):
            self.player_vel = glm.vec3(0, 0, 0)
        else:
            self.player_vel -= friction_vec

        if glm.length(self.player_vel) > PLAYER_MAX_SPEED:
            self.player_vel = custom_vec_functions.safe_normalize(self.player_vel) * PLAYER_MAX_SPEED

        if glm.length(self.player_vel) < self.min_vel:
            self.player_vel = glm.vec3(0, 0, 0)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = self.app.delta_time
        if key_state[pg.K_w]:
            self.move_forward()
        if key_state[pg.K_s]:
            self.move_back()
        if key_state[pg.K_d]:
            self.move_right()
        if key_state[pg.K_a]:
            self.move_left()
        if key_state[pg.K_c]:
            self.position = PLAYER_POS
        if self.is_flying:
            if key_state[pg.K_SPACE]:
                self.move_up()
            if key_state[pg.K_LSHIFT]:
                self.move_down()

    def handle_event(self, event):
        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 3:
                voxel_handler.set_voxel()
            if event.button == 1:
                voxel_handler.remove_voxel()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        for event in self.app.events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.lock_mouse = not self.lock_mouse
                pg.event.set_grab(self.lock_mouse)
                pg.mouse.set_visible(not self.lock_mouse)
        if self.lock_mouse:
            if mouse_dx:
                self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
            if mouse_dy:
                self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
