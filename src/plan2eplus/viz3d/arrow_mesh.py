import numpy as np
import trimesh


def create_segmented_arrow(p_start, p_mid, p_end, radius=0.05):
    """Creates a 3D arrow mesh composed of two segments and a head."""
    # Convert points to numpy arrays
    p_start = np.array(p_start, dtype=float)
    p_mid = np.array(p_mid, dtype=float)
    p_end = np.array(p_end, dtype=float)

    # --- 1. Segment 1: Shaft from Start to Mid ---
    vec1 = p_mid - p_start
    len1 = np.linalg.norm(vec1)
    dir1 = vec1 / len1

    # Create cylinder at origin pointing along +Z, then align and place it
    shaft1 = trimesh.creation.cylinder(radius=radius, height=len1)
    shaft1.apply_translation([0, 0, len1 / 2.0])  # Center to base origin
    rot1 = trimesh.geometry.align_vectors([0, 0, 1], dir1)
    shaft1.apply_transform(rot1)
    shaft1.apply_translation(p_start)

    # --- 2. Segment 2: Shaft from Mid to End (shortened for the head) ---
    vec2 = p_end - p_mid
    total_len2 = np.linalg.norm(vec2)
    dir2 = vec2 / total_len2

    # Reserve space at the end for the arrowhead (e.g., 4 times the radius)
    head_len = radius * 4.0
    # Safeguard if the segment is extremely short
    if head_len > total_len2:
        head_len = total_len2 * 0.4

    shaft2_len = total_len2 - head_len

    # Create, align, and position the second shaft segment
    shaft2 = trimesh.creation.cylinder(radius=radius, height=shaft2_len)
    shaft2.apply_translation([0, 0, shaft2_len / 2.0])
    rot2 = trimesh.geometry.align_vectors([0, 0, 1], dir2)
    shaft2.apply_transform(rot2)
    shaft2.apply_translation(p_mid)

    # --- 3. Arrowhead: Cone at the End ---
    head = trimesh.creation.cone(radius=radius * 2.5, height=head_len)
    head.apply_translation([0, 0, head_len / 2.0])  # Move base to origin
    head.apply_transform(rot2)  # Shares alignment with the second segment

    # Place head right where shaft2 ends
    p_head_base = p_mid + (dir2 * shaft2_len)
    head.apply_translation(p_head_base)

    # --- 4. Combine Segments ---
    arrow_mesh = trimesh.util.concatenate([shaft1, shaft2, head])
    return arrow_mesh
