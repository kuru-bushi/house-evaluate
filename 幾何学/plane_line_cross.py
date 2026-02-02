import numpy as np

def find_line_plane_intersection(p_line, p1, p2, p3):
    """
    原点と p_line を通る直線と、p1, p2, p3 を通る平面の交点を求める
    """
    # ベクトルとして定義
    P_line = np.array(p_line, dtype=float)
    P1 = np.array(p1, dtype=float)
    P2 = np.array(p2, dtype=float)
    P3 = np.array(p3, dtype=float)

    # 1. 平面の法線ベクトルを計算 (外積)
    v12 = P2 - P1
    v13 = P3 - P1
    normal = np.cross(v12, v13)

    # 3点が一直線上にある場合、平面が定義できない
    if np.linalg.norm(normal) < 1e-9:
        raise ValueError("指定された3点が一直線上にあるため、平面を定義できません。")

    # 2. 平面の方程式 Ax + By + Cz = d の d を求める
    # 法線ベクトルと平面上の点の点乗積
    d = np.dot(normal, P1)

    # 3. 直線 L = t * P_line と平面の交差判定
    # normal · (t * P_line) = d  => t = d / (normal · P_line)
    denom = np.dot(normal, P_line)

    if abs(denom) < 1e-9:
        if abs(d) < 1e-9:
            return "直線は平面に含まれています（無限の交点）"
        else:
            return "直線と平面は平行です（交点なし）"

    # パラメータ t を計算
    t = d / denom
    
    # 交点座標を計算
    intersection = t * P_line
    return intersection

# --- テストデータ ---
# 直線が通る点 (a, b, c)
line_target = [1, 1, 1]

# 平面を通る3点
plane_p1 = [1, 0, 0]
plane_p2 = [0, 1, 0]
plane_p3 = [0, 0, 1]

# 計算実行
try:
    result = find_line_plane_intersection(line_target, plane_p1, plane_p2, plane_p3)
    print(f"直線が通る点: {line_target}")
    print(f"平面を通る3点: {plane_p1}, {plane_p2}, {plane_p3}")
    print(f"交点座標: {result}")
except ValueError as e:
    print(e)