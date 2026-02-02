import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.cm as cm # カラーマップを使うためにインポート

def draw_rectangles_with_gradient_colors(list_of_rect_coords):
    """
    指定された複数の四角形の座標を描画する関数。
    四角形の色はグラデーション（カラーマップ）で割り当てられ、凡例も表示される。
    
    Args:
        list_of_rect_coords (list of list of tuples/lists): 
            複数の四角形の座標のリスト。
            例: [[[x1,y1],[x2,y2],[x3,y3],[x4,y4]], [[x1',y1'], ...]]
    """
    
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal', adjustable='box') # アスペクト比を保ち、正方形を正方形に見せる

    all_x = []
    all_y = []

    num_rectangles = len(list_of_rect_coords)
    
    # カラーマップを選択
    # 例: 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'jet' など
    cmap = cm.get_cmap('viridis', num_rectangles) # num_rectangles の数だけ色を生成

    for i, rect_coords in enumerate(list_of_rect_coords):
        # カラーマップから現在の四角形の色を取得
        current_color = cmap(i) 

        # matplotlib.patches.Polygon を使用して四角形を描画
        polygon = patches.Polygon(rect_coords, closed=True, 
                                  fill=True, edgecolor='black', facecolor=current_color, alpha=0.7,
                                  label=f'Rectangle {i+1}') # 凡例のためのラベルを追加
        ax.add_patch(polygon)
        
        # x, y 座標を収集して描画範囲を調整
        coords_np = np.array(rect_coords)
        all_x.extend(coords_np[:, 0])
        all_y.extend(coords_np[:, 1])

    # 描画範囲を調整 (少し余白を持たせる)
    if all_x and all_y:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        x_margin = (max_x - min_x) * 0.1 if (max_x - min_x) != 0 else 1
        y_margin = (max_y - min_y) * 0.1 if (max_y - min_y) != 0 else 1
        
        ax.set_xlim(min_x - x_margin, max_x + x_margin)
        ax.set_ylim(min_y - y_margin, max_y + y_margin)
    
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Multiple Rectangles with Gradient Colors and Legend')
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1)) # 凡例を表示位置を調整
    plt.tight_layout() # レイアウトを自動調整して凡例が切れないようにする
    plt.show()

# --- 使用例 ---

rect1_coords = [[1, 1], [5, 1], [5, 4], [1, 4]]
rect2_coords = [[6, 2], [8, 3], [7, 6], [5, 5]]
rect3_coords = [[-3, -2], [0, -1], [-1, 1], [-4, 0]]
rect4_coords = [[-7, 5], [-5, 6], [-4, 3], [-6, 2]] # 4つ目の四角形を追加

all_rectangles = [rect1_coords, rect2_coords, rect3_coords, rect4_coords]

draw_rectangles_with_gradient_colors(all_rectangles)