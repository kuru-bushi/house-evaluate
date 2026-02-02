import numpy as np

def calculate_xy_distance_np(p1, p2):
    # 配列に変換
    a = np.array(p1[:2]) # x, y のみ抽出
    b = np.array(p2[:2])
    
    # ユーリッド距離を計算
    return np.linalg.norm(a - b)

# --- 使用例 ---
point_a = np.array([1, 2, 5])
point_b = np.array([4, 6, 10])

print(f"xy平面上の距離 (NumPy): {calculate_xy_distance_np(point_a, point_b)}")