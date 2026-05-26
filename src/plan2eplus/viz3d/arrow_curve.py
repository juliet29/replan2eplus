from enum import Enum
import numpy as np
import shapely.geometry
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


def sample_quadratic_bezier(
    p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, n: int = 30
) -> np.ndarray:
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2


def create_tube(
    p0: np.ndarray,
    p1: np.ndarray,
    p2: np.ndarray,
    radius: float,
    color: list,
    n: int = 30,
) -> trimesh.Trimesh:
    pts = sample_quadratic_bezier(p0, p1, p2, n)
    circle = shapely.geometry.Point(0, 0).buffer(radius)
    tube = trimesh.creation.sweep_polygon(circle, pts)
    tube.visual.face_colors = color
    return tube


def create_arrow_head(
    pt: np.ndarray,
    drn: np.ndarray,
    color: list,
    radius: float = 0.05,
    len: float = 0.25,
) -> trimesh.Trimesh:
    head = trimesh.creation.cone(radius=radius, height=len)
    head.apply_translation(pt)
    head = align_cone_to_direction(head, drn, pt)
    head.visual.face_colors = color
    return head


def create_segmented_arrow(
    p_start,
    p_mid,
    p_end,
    arrow_loc: ArrowHeadLoc,
    color: list = [255, 0, 0, 255],
    radius: float = 0.02,
):
    """Creates a 3D arrow mesh composed of a bezier tube and a cone head."""
    p_start = np.array(p_start, dtype=float)
    p_mid = np.array(p_mid, dtype=float)
    p_end = np.array(p_end, dtype=float)

    tube = create_tube(p_start, p_mid, p_end, radius=radius, color=color)

    head_pt = p_start if arrow_loc == ArrowHeadLoc.START else p_end
    drn = compute_endpoint_direction(p_start, p_mid, p_end, arrow_loc)
    arrow_head = create_arrow_head(head_pt, drn, color=color, radius=radius * 2.5)

    scene = trimesh.Scene()
    scene.add_geometry(tube)
    scene.add_geometry(arrow_head)

    # scene.show()
    return scene
