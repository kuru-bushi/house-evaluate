import trimesh
import numpy as np

# mesh の読み込み
mesh = trimesh.load("model.obj")

# OBB を取得
obb = mesh.bounding_box_oriented

# OBB の変換行列（4×4）
T_obb = obb.primitive.transform

# OBB の回転部分を取り出し (3×3)
R_obb = T_obb[:3, :3]

# OBB の各軸（列ベクトルがOOBの軸）
axis_x = R_obb[:, 0]   # OBBの X 軸（最長方向とは限らない）
axis_y = R_obb[:, 1]
axis_z = R_obb[:, 2]

# ---- ここで、揃えたい軸方向を決める ----
# 例: OBB の X軸を +X に合わせる
target_axis = np.array([1, 0, 0])  # worldの X 軸

# OBB の軸は正負があるため、符号を合わせる
if np.dot(axis_x, target_axis) < 0:
    axis_x = -axis_x

# 回転行列を求める
# 回転前軸: axis_x → 回転後: target_axis
v = np.cross(axis_x, target_axis)
s = np.linalg.norm(v)
c = np.dot(axis_x, target_axis)

# ロドリゲスの回転公式により回転行列を構築
if s == 0:
    R_align = np.eye(3)  # すでに揃っている
else:
    vx = np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])
    R_align = np.eye(3) + vx + vx.dot(vx) * ((1 - c) / (s**2))

# 4x4 のホモ行列に拡張
M = np.eye(4)
M[:3, :3] = R_align

# mesh を回転
mesh.apply_transform(M)

# 保存
mesh.export("aligned.obj")
