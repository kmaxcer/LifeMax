import pygame as pg
import moderngl as mgl

from main import VoxelEngine
from texture_array_builder import TextureArrayBuilder


class Textures:
    def __init__(self, app: VoxelEngine):
        self.app = app
        self.context = app.context

        # load texture
        self.texture_0 = self.load(pg.image.load(r'assets/frame.png'))
        self.texture_array_0 = self.load(TextureArrayBuilder().load_texture_pack(), is_tex_array=True)

        # assign texture unit
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)

    def load(self, texture, is_tex_array=False):
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        if is_tex_array:
            num_layers = 6 * texture.get_height() // texture.get_width()
            texture = self.app.context.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, 'RGBA')
            )
        else:
            texture = self.context.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, 'RGBA', False)
            )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
