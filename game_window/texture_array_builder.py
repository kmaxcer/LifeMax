import pygame as pg

import paths
from paths import get_resource_path
import os


class TextureArrayBuilder:
    def __init__(self):
        self.texture_array: pg.image | None = None

    def load_texture_pack(self, pack_directory: str | None = None) -> pg.Surface:
        import json
        if pack_directory is None:
            pack_directory = get_resource_path("test_texture_pack")

        pack_data = None
        images = []

        for file in os.listdir(pack_directory):
            full_path = os.path.join(pack_directory, file)
            if file == "pack_data.json":
                with open(full_path) as f:
                    pack_data = json.load(f)
                continue

            if file.endswith(".png"):
                new_image = pg.image.load(full_path).convert_alpha()
                images.append([file.removesuffix(".png"), new_image])

        assert pack_data, FileNotFoundError(f"Could not find pack_data.json in {pack_directory}")

        self._build_texture_array(images, pack_data)

        return self.texture_array

    def _build_texture_array(self, images: list[pg.image], pack_data: dict) -> None:
        texture_resolution = pack_data["texture_resolution"]
        self.texture_array = pg.Surface((texture_resolution * 6, texture_resolution * (len(images) + 1)))
        # self.texture_array.fill((0, 0, 1))
        # self.texture_array.set_colorkey((0, 0, 1))

        images.sort(key=lambda n: [ind for ind, itm in enumerate(pack_data["ids"]) if n[0] in itm])
        images = [img[1] for img in images]

        for index, (image, image_data) in enumerate(zip(images, pack_data["ids"])):
            texture_type = image_data[1]
            cropped_textures = self._texture_splitter(image, texture_resolution,
                                                      image.get_width() // texture_resolution)
            for x in range(6):
                curr_tex = cropped_textures[pack_data["texture_types"][str(texture_type)][x]]

                self.texture_array.blit(curr_tex, (x * texture_resolution, (index + 1) * texture_resolution))

        # pg.image.save(self.texture_array, paths.get_resource_path() + r"\tex_array.png")

    @staticmethod
    def _texture_splitter(texture: pg.Surface, image_res: int, width: int) -> list[pg.Surface]:
        res = []
        crop_rect = pg.Rect((0, 0), (image_res, image_res))
        for i in range(width):
            res_tex = pg.Surface((image_res, image_res))
            crop_rect.x = image_res * i
            res_tex.blit(texture, (0, 0), crop_rect)
            res.append(res_tex)

        return res


if __name__ == "__main__":
    pg.init()
    pg.display.set_mode((0, 0))
    test = TextureArrayBuilder()
    test.load_texture_pack()
    pg.quit()
