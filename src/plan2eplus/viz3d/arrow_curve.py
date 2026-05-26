from enum import Enum
import numpy as np
from loguru import logger
from trimesh.path.entities import Bezier
import trimesh


class ArrowHeadLoc(Enum):
    START = -1
    END = 1


def compute_endpoint_direction(
    p_start: np.ndarray, p_mid: np.ndarray, p_end: np.ndarray, arrow_loc: ArrowHeadLoc
) -> np.ndarray:
    if arrow_loc == ArrowHeadLoc.END:
        drn = p_end - p_mid
    else:
        drn = p_start - p_mid
    return drn / np.linalg.norm(drn)


def align_cone_to_direction(
    cone: trimesh.Trimesh, drn: np.ndarray, pt: np.ndarray
) -> trimesh.Trimesh:
    z = np.array([0.0, 0.0, 1.0])
    axis = np.cross(z, drn)
    angle = np.arccos(np.clip(np.dot(z, drn), -1.0, 1.0))
    if np.linalg.norm(axis) > 1e-6:
        matrix = trimesh.transformations.rotation_matrix(angle, axis, point=pt)
        cone.apply_transform(matrix)
    return cone


def create_arrow_head(pt, drn: np.ndarray, radius=0.01, len: float = 0.25):
    head = trimesh.creation.cone(radius=radius, height=len)
    head.apply_translation(pt)
    head = align_cone_to_direction(head, drn, pt)
    return head


def create_segmented_arrow(
    p_start, p_mid, p_end, arrow_loc: ArrowHeadLoc, radius: float = 0.05
):
    """Creates a 3D arrow mesh composed of two segments and a head."""
    # Convert points to numpy arrays
    p_start = np.array(p_start, dtype=float)
    p_mid = np.array(p_mid, dtype=float)
    p_end = np.array(p_end, dtype=float)
    print("hi")

    points = np.array([p_start, p_mid, p_end])
    print(points)
    bezier = Bezier(points=[0, 1, 2], color=[255, 0, 0, 255])
    print("hi2")

    logger.debug(bezier)
    print(bezier)
    path = trimesh.path.Path3D(entities=[bezier], vertices=points)

    head_pt = p_start if arrow_loc == ArrowHeadLoc.START else p_end
    drn = compute_endpoint_direction(p_start, p_mid, p_end, arrow_loc)
    arrow_head = create_arrow_head(head_pt, drn)
    scene = trimesh.Scene()
    scene.add_geometry(arrow_head)
    scene.add_geometry(path)

    logger.debug(scene)
    scene.show()
    return scene
