import glm
from functools import singledispatch


@singledispatch
def safe_normalize(vector):
    raise NotImplementedError(f"Нормализация не реализована для типа: {type(vector)}")


@safe_normalize.register(glm.vec2)
def _(vector):
    length = glm.length(vector)
    if length == 0:
        return glm.vec2(0, 0)
    else:
        return glm.normalize(vector)


@safe_normalize.register(glm.vec3)
def _(vector):
    length = glm.length(vector)
    if length == 0:
        return glm.vec3(0, 0, 0)
    else:
        return glm.normalize(vector)
