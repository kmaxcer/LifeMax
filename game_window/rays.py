import glm
from typing import List
# from world import World
from constants import *

world = None


def init_ray_casting(world_):
    global world
    world = world_


def ray_cast(start: glm.vec3, end: glm.vec3):
    # start point
    x1, y1, z1 = start
    # end point
    x2, y2, z2 = end

    current_voxel_pos = glm.ivec3(x1, y1, z1)
    # self.voxel_id = 0
    # self.voxel_normal = glm.ivec3(0)
    voxel_id = 0
    voxel_normal = glm.ivec3(0)
    step_dir = -1

    dx = glm.sign(x2 - x1)
    delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
    max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

    dy = glm.sign(y2 - y1)
    delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
    max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

    dz = glm.sign(z2 - z1)
    delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
    max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

    while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

        result = get_voxel_id(voxel_world_pos=current_voxel_pos)
        if result[0]:
            voxel_id, voxel_index, voxel_local_pos, chunk = result
            voxel_world_pos = current_voxel_pos

            if step_dir == 0:
                voxel_normal.x = -dx
            elif step_dir == 1:
                voxel_normal.y = -dy
            else:
                voxel_normal.z = -dz
            return voxel_id, voxel_index, voxel_local_pos, chunk, voxel_normal, voxel_world_pos

        if max_x < max_y:
            if max_x < max_z:
                current_voxel_pos.x += dx
                max_x += delta_x
                step_dir = 0
            else:
                current_voxel_pos.z += dz
                max_z += delta_z
                step_dir = 2
        else:
            if max_y < max_z:
                current_voxel_pos.y += dy
                max_y += delta_y
                step_dir = 1
            else:
                current_voxel_pos.z += dz
                max_z += delta_z
                step_dir = 2
    return [None] * 6


def get_voxel_id(voxel_world_pos):
    cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

    if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
        chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
        chunk = world.chunks[chunk_index]

        lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

        voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
        voxel_id = chunk.voxels[voxel_index]
        return voxel_id, voxel_index, voxel_local_pos, chunk
    return 0, 0, 0, 0
