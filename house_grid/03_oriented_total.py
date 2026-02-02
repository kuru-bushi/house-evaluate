import numpy as np
import trimesh



def align_points_to_axis(points, mesh=None, obb=None, target_axis='x'):
    """
    points: (N,3) numpy array (点群)
    mesh: trimesh.Trimesh (任意) — OBB を mesh から得る場合に使う
    obb: trimesh.primitives.Box (任意) — 既に OBB を持っている場合はこちらを優先
    target_axis: 'x' or 'y'  — OBB の"長軸"をどちらに合わせるか

    戻り値:
      points_aligned: (N,3) numpy array
      M_total: (4,4) 合成変換行列（同次）
    """
    assert (mesh is not None) or (obb is not None), "mesh か obb のどちらかを指定してください"

    if obb is None:
        obb = mesh.bounding_box_oriented

    # OBB の transform（box_local -> world）
    T_obb = obb.primitive.transform.copy()   # 4x4

    # OBB の回転（列が box のローカル軸方向）
    R_obb = T_obb[:3, :3]
    extents = obb.primitive.extents  # 長さ (x_len, y_len, z_len) の順（Box のローカル軸順）

    # 最長軸を選ぶ（例: 長手方向を合わせる）
    long_idx = int(np.argmax(extents))
    obb_axis = R_obb[:, long_idx]    # world 空間でのその軸ベクトル
    # 正規化（重要）
    obb_axis = obb_axis / np.linalg.norm(obb_axis)

    # 目的のワールド軸ベクトル
    if target_axis == 'x':
        tgt = np.array([1.0, 0.0, 0.0])
    elif target_axis == 'y':
        tgt = np.array([0.0, 1.0, 0.0])
    else:
        raise ValueError("target_axis must be 'x' or 'y'")

    # 符号を揃える（tgt と反対向きだったら反転して扱う）
    if np.dot(obb_axis, tgt) < 0:
        obb_axis = -obb_axis

    # ロドリゲスで軸 -> tgt への回転を作る
    v = np.cross(obb_axis, tgt)
    s = np.linalg.norm(v)
    c = np.dot(obb_axis, tgt)

    if np.isclose(s, 0.0):
        R_align = np.eye(3)  # 既に揃っているか、180度のケース
        if np.isclose(c, -1.0):
            # 180度回転（任意の直交ベクトルを軸にする）
            # obb_axis に直交するベクトルを作る
            if abs(obb_axis[0]) < 0.9:
                perp = np.array([1.0, 0.0, 0.0])
            else:
                perp = np.array([0.0, 1.0, 0.0])
            axis = np.cross(obb_axis, perp)
            axis = axis / np.linalg.norm(axis)
            # Rodrigues formula for 180deg:
            K = np.array([[0, -axis[2], axis[1]],
                          [axis[2], 0, -axis[0]],
                          [-axis[1], axis[0], 0]])
            R_align = np.eye(3) + 2 * K.dot(K)
    else:
        vx = np.array([[0, -v[2], v[1]],
                       [v[2], 0, -v[0]],
                       [-v[1], v[0], 0]])
        R_align = np.eye(3) + vx + (vx @ vx) * ((1 - c) / (s**2))

    # 回転中心は OBB の中心（world座標）
    # trimesh の Box オブジェクトは center_mass や bounds 中心を持つ
    try:
        center = obb.center_mass   # or obb.centroid
    except Exception:
        # fallback: transform の平行移動成分
        center = T_obb[:3, 3].copy()

    # 同次変換を作る: T_to_origin, R_align, T_back
    T_to_origin = np.eye(4)
    T_to_origin[:3, 3] = -center

    R4 = np.eye(4)
    R4[:3, :3] = R_align

    T_back = np.eye(4)
    T_back[:3, 3] = center

    M_total = T_back @ R4 @ T_to_origin

    # numpy の点群に適用 (同次座標)
    pts_h = np.hstack([points, np.ones((points.shape[0], 1))])  # (N,4)
    pts_trans_h = pts_h @ M_total.T
    pts_trans = pts_trans_h[:, :3]

    return pts_trans, M_total

# 使い方の例
# mesh = trimesh.load("model.obj")
# points = mesh.vertices.copy()   # あるいは別の (N,3) np.array
# aligned_points, M = align_points_to_axis(points, mesh=mesh, target_axis='x')
