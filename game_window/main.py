import pygame
import moderngl as mgl
import pygame as pg

import sys
from typing import NoReturn

from constants import *

# эта строка позволяет импортировать VoxelEngine для типовых аннотаций в других файлах без создания
# кругового импортирования
if __name__ == '__main__':
    import shader_program
    from shader_program import ShaderProgram
    from scene import Scene
    from player import Player
    from textures import Textures
    import settings

if FORCE_USE_GPU:
    import os
    import ctypes

    os.environ["__NV_PRIME_RENDER_OFFLOAD"] = "1"
    os.environ["__GLX_VENDOR_LIBRARY_NAME"] = "nvidia"
    ctypes.WinDLL('vcamp110')


class VoxelEngine:
    def __init__(self) -> None:
        # Pre-definitions
        self.textures = None
        self.player = None
        self.shader_program = None
        self.scene = None
        self.settings = None
        #

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.gl_set_attribute(pg.GL_STENCIL_SIZE, 8)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)

        pg.display.set_mode(WIN_RES, flags=pygame.OPENGL | pg.DOUBLEBUF)
        self.context: mgl.Context = mgl.create_context()

        self.context.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.context.gc_mode = "auto"

        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: int = 0
        self.time: float = 0
        self.events: list[pygame.event.Event] = []

        self.is_running: bool = False

        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program: shader_program.ShaderProgram = ShaderProgram(self)
        self.scene = Scene(self)
        self.settings = settings.load_settings()

    def update(self) -> None:
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick(FPS_MAX) * GAME_SPEED
        self.time = pg.time.get_ticks() * 0.001

        pg.display.set_caption(f"{str(int(self.clock.get_fps())): <10}{[round(x, 2) for x in self.player.position]}")

    def render(self) -> None:
        self.context.clear(color=BG_COLOR)
        self.scene.render()
        pg.display.flip()

    def handle_events(self) -> None:
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F10):
                self.is_running = False
            self.player.handle_event(event=event)

    def run(self) -> NoReturn:
        self.is_running = True
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        sys.exit()


def main() -> None:
    app = VoxelEngine()
    ctx = app.context
    print("Vendor:", ctx.info['GL_VENDOR'])
    print("Renderer:", ctx.info['GL_RENDERER'])
    print("OpenGL version:", ctx.info['GL_VERSION'])
    print("ModernGL version:", mgl.__version__)
    app.run()


if __name__ == '__main__':
    main()
