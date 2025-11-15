import numpy as np

def ransac_plane_fitting(points, threshold=0.01, max_iterations=2000):
    """
    RANSAC を用いて平面推定を行う。

    Parameters:
        points (np.ndarray): (N, 3) 点群
        threshold (float): インライア判定距離[m]
        max_iterations (int): 試行回数

    Returns:
        best_plane (tuple): (normal_vector, d)
        best_inliers (np.ndarray): インライアのインデックス
    """
    best_inliers = []
    best_plane = None
    N = points.shape[0]

    for _ in range(max_iterations):
        # --- 1) ランダムに3点サンプリング ---
        idx = np.random.choice(N, 3, replace=False)
        p1, p2, p3 = points[idx]

        # --- 2) 平面法線を求める ---
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        if np.linalg.norm(normal) < 1e-6:
            continue  # 3点がほぼ一直線 → 平面定義不可

        normal = normal / np.linalg.norm(normal)

        # 平面方程式 ax + by + cz + d = 0
        d = -np.dot(normal, p1)

        # --- 3) 全点と平面の距離を計算 ---
        distances = np.abs(np.dot(points, normal) + d)

        # --- 4) インライア判定 ---
        inliers = np.where(distances < threshold)[0]

        # --- 5) ベスト更新 ---
        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_plane = (normal, d)

    return best_plane, best_inliers


# -----------------------------
# 使用例
# -----------------------------
if __name__ == "__main__":
    # 平面 z = 0.5x + 0.3y + 2 に ノイズを追加した点群
    np.random.seed(0)
    xy = np.random.rand(500, 2)
    z = 0.5*xy[:,0] + 0.3*xy[:,1] + 2 + 0.01*np.random.randn(500)
    points = np.hstack([xy, z.reshape(-1,1)])

    plane, inliers = ransac_plane_fitting(points, threshold=0.02)

    print("平面の法線:", plane[0])
    print("d:", plane[1])
    print("インライア数:", len(inliers))
