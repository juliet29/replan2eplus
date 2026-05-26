from pathlib import Path
import xarray as xr
import trimesh
from trimesh.visual.texture import TextureVisuals
from trimesh.visual.color import ColorVisuals
from trimesh.visual.material import SimpleMaterial

from plan2eplus.ezcase.ez import EZ
from plan2eplus.viz3d.arrows import make_case_arrows


def make_transparent(scene: trimesh.Scene, alpha: int = 128) -> trimesh.Scene:
    for key, mesh in scene.geometry.items():
        viz = mesh.visual
        try:
            assert isinstance(viz, ColorVisuals), f"{key} has type {type(viz)}"

            viz.face_colors[:, 3] = alpha
            # viz.main_color = [*color[:3], 128]
            # mesh.visual.vertex_colors[:, 3] = alpha
        except AssertionError:
            assert isinstance(viz, TextureVisuals), f"{key} has type {type(viz)}"
            material = mesh.visual.material
            assert isinstance(material, SimpleMaterial)
            diffuse_color = mesh.visual.material.diffuse

            # Change the alpha channel (index 3) to 128 (~50% transparent)
            diffuse_color[3] = 128

            # Write it back to the material
            mesh.visual.material.diffuse = diffuse_color
    return scene


def read_building(case: EZ, obj_path: Path, data: xr.DataArray):
    building = trimesh.load(obj_path)
    assert isinstance(building, trimesh.Scene)
    building = make_transparent(building, alpha=30)

    arrow_scenes = make_case_arrows(case, data)

    final_scene = trimesh.Scene()
    for name, geom in building.geometry.items():
        if name == "roof":
            continue
        final_scene.add_geometry(geom, geom_name=name)
    for arrow_scene in arrow_scenes:
        for name, geom in arrow_scene.geometry.items():
            final_scene.add_geometry(geom, geom_name=name)

    final_scene.show()
    return final_scene
