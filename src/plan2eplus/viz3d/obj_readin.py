from pathlib import Path
from loguru import logger
import trimesh
from trimesh.base import TextureVisuals
from trimesh.exchange.obj import load_obj
from trimesh.visual.color import ColorVisuals
from trimesh.visual.material import SimpleMaterial


def make_transparent(scene: trimesh.Scene, alpha: int = 128) -> trimesh.Scene:
    for key, mesh in scene.geometry.items():
        viz = mesh.visual
        try:
            assert isinstance(viz, ColorVisuals), f"{key} has type {type(viz)}"

            viz.face_colors[:, 3] = alpha
            logger.debug(f"Set face colors for {key}")
            # viz.main_color = [*color[:3], 128]
            # mesh.visual.vertex_colors[:, 3] = alpha
        except AssertionError:
            assert isinstance(viz, TextureVisuals), f"{key} has type {type(viz)}"
            material = mesh.visual.material
            assert isinstance(material, SimpleMaterial)
            logger.debug((key, material))
            diffuse_color = mesh.visual.material.diffuse

            # Change the alpha channel (index 3) to 128 (~50% transparent)
            diffuse_color[3] = 128

            # Write it back to the material
            mesh.visual.material.diffuse = diffuse_color
    return scene


def read_building(
    path: Path,
):
    obj = trimesh.load(path)
    obj = make_transparent(obj)
    obj.show()
    return obj
    obj = load_obj(file_obj=path, group_material=False, skip_materials=True)
