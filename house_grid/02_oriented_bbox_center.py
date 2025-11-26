import trimesh
import numpy as np

mesh = trimesh.load("model.obj")

# 1. メッシュの中心（重心）を取得
center = mesh.centroid

# 2. メッシュを原点へ移動
T1 = np.eye(4)
T1[:3, 3] = -center
mesh.apply_transform(T1)

# 3. 回転行列を適用（例: R_align）
M = np.eye(4)
M[:3, :3] = R_align
mesh.apply_transform(M)

# 4. 必要であれば元の位置に戻す
T2 = np.eye(4)
T2[:3, 3] = center
mesh.apply_transform(T2)
