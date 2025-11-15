import numpy as np

def ransac_plane(points, threshold=0.01, max_iterations=2000):
    """
    単一平面を RANSAC で抽出する関数
    """
    best_inliers = []
    best_plane = None
    N = points.shape[0]

    for _ in range(max_iterations):
        # ランダムに3点を選ぶ
        idx = np.random.choice(N, 3, replace=False)
        p1, p2, p3 = points[idx]

        # 法線の計算
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        if np.linalg.norm(normal) < 1e-6:
            continue
        normal = normal / np.linalg.norm(normal)

        # 平面の d を計算 (ax + by + cz + d = 0)
        d = -np.dot(normal, p1)

        # 全点との距離
        distances = np.abs(np.dot(points, normal) + d)

        # インライア
        inliers = np.where(distances < threshold)[0]

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_plane = (normal, d)

    return best_plane, best_inliers


def extract_multiple_planes(points, num_planes=3,
                            threshold=0.01, max_iterations=2000,
                            min_points=50):
    """
    複数の平面を RANSAC で抽出する。
    
    Returns:
        planes: [{'normal': n, 'd': d, 'inliers': indices}, ...]
        remaining_points: 最後に残った点群
    """
    planes = []
    remaining = points.copy()

    for i in range(num_planes):
        if remaining.shape[0] < min_points:
            break

        # RANSAC で1平面を推定
        plane, inliers = ransac_plane(
            remaining, threshold, max_iterations
        )

        if plane is None or len(inliers) < min_points:
            break

        normal, d = plane

        planes.append({
            'normal': normal,
            'd': d,
            'inliers': inliers.copy(),
            'points': remaining[inliers].copy()
        })

        # インライアを除外して次の平面へ
        mask = np.ones(remaining.shape[0], dtype=bool)
        mask[inliers] = False
        remaining = remaining[mask]

    return planes, remaining


# ----------------------------------------
#  使用例
# ----------------------------------------
if __name__ == "__main__":
    # (例) 3つの平面を持つ点群を作成
    np.random.seed(0)

    # 平面1: z = 0.5x + 0.3y + 2
    xy1 = np.random.rand(300, 2)
    z1 = 0.5*xy1[:,0] + 0.3*xy1[:,1] + 2 + 0.01*np.random.randn(300)
    p1 = np.hstack([xy1, z1.reshape(-1,1)])

    # 平面2: z = -x + 1
    xy2 = np.random.rand(300, 2)
    z2 = -xy2[:,0] + 1 + 0.01*np.random.randn(300)
    p2 = np.hstack([xy2, z2.reshape(-1,1)])

    # 平面3: y = 2 (垂直)
    x3 = np.random.rand(300)
    z3 = np.random.rand(300)
    y3 = np.full(300, 2) + 0.01*np.random.randn(300)
    p3 = np.vstack([x3, y3, z3]).T

    # まとめて点群にする
    points = np.vstack([p1, p2, p3])

    # 平面を抽出
    planes, remaining = extract_multiple_planes(
        points, num_planes=3, threshold=0.05
    )

    for i, pl in enumerate(planes):
        print(f"Plane {i+1}:")
        print("  normal:", pl['normal'])
        print("  d:", pl['d'])
        print("  inliers:", len(pl['inliers']))

    print("残った点数:", remaining.shape[0])
