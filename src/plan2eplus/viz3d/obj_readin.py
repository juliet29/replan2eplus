from pathlib import Path
from loguru import logger
import numpy as np
import pyglet
import xarray as xr
import trimesh
from trimesh.viewer import SceneViewer
from trimesh.visual.color import ColorVisuals

from plan2eplus.ezcase.ez import EZ
from plan2eplus.viz3d.arrows import make_case_arrows


def make_transparent(scene: trimesh.Scene, alpha: int = 128) -> trimesh.Scene:
    for key, mesh in scene.geometry.items():
        if not isinstance(mesh.visual, ColorVisuals):
            mesh.visual = mesh.visual.to_color()
        mesh.visual.face_colors[:, 3] = alpha
        logger.debug(f"Set face colors for {key}")
    return scene


def set_isometric_camera(scene: trimesh.Scene, transform_str: str) -> trimesh.Scene:
    scene.camera_transform = np.array(np.matrix(transform_str))
    return scene


def read_building(case: EZ, obj_path: Path, data: xr.DataArray):
    building = trimesh.load(obj_path)
    assert isinstance(building, trimesh.Scene)
    building = make_transparent(building, alpha=100)

    arrow_scenes = make_case_arrows(case, data)

    final_scene = trimesh.Scene()
    for name, geom in building.geometry.items():
        if name == "roof":
            continue
        if name == "wall":
            geom.visual.face_colors[:, :3] = [211, 182, 131]
        final_scene.add_geometry(geom, geom_name=name)
    for arrow_scene in arrow_scenes:
        for name, geom in arrow_scene.geometry.items():
            final_scene.add_geometry(geom, geom_name=name)

    # final_scene = set_isometric_camera(final_scene, transform_str="paste matrix here")

    viewer = SceneViewer(final_scene, start_loop=False)

    @viewer.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.P:
            print(viewer.scene.camera_transform)

    pyglet.app.run()
    return final_scene
