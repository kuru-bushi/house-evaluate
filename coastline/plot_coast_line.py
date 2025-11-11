import pandas as pd
from geopy.geocoders import Nominatim
import folium


# 1. データの読み込み
# try:
#     # CSVファイルを読み込む（必要に応じてencoding='shift_jis'などを設定）
#     df = pd.read_csv('locations.csv', encoding='utf-8')
# except FileNotFoundError:
#     print("エラー: 'locations.csv'が見つかりません。ファイル名を確認してください。")
#     exit()
#     df = pd.DataFrame({
#         "都道府県": ["青森県", "青森県",],
#         "市名": ["八戸市", "六ヶ所村"]
#     })

df = pd.DataFrame({
    "都道府県": ["青森県", "青森県",],
    "市名": ["八戸市", "六ヶ所村"]
})



# 2. ジオコーディングの設定
# Nominatimはオープンソースのジオコーディングサービス（利用制限に注意）
geolocator = Nominatim(user_agent="city_locator_script")

# ジオコーディング結果を格納するリストを初期化
latitude_list = []
longitude_list = []
failed_addresses = []

# 3. 各行の住所を検索
print("ジオコーディングを開始します...")

for index, row in df.iterrows():
    # 検索する完全な住所文字列を作成
    full_address = str(row['都道府県']) + str(row['市名'])
    
    try:
        # 住所から緯度・経度を取得（時間がかかる処理）
        location = geolocator.geocode(full_address, timeout=10)
        
        if location:
            latitude_list.append(location.latitude)
            longitude_list.append(location.longitude)
            print(f"✅ 成功: {full_address} -> ({location.latitude}, {location.longitude})")
        else:
            # 住所が見つからなかった場合
            latitude_list.append(None)
            longitude_list.append(None)
            failed_addresses.append(full_address)
            print(f"❌ 失敗: {full_address} の位置情報が見つかりませんでした。")
            
    except Exception as e:
        # ネットワークエラーなど、その他の問題が発生した場合
        latitude_list.append(None)
        longitude_list.append(None)
        failed_addresses.append(full_address)
        print(f"🛑 エラー: {full_address} の処理中にエラーが発生しました: {e}")

# 4. 結果をデータフレームに追加
df['緯度'] = latitude_list
df['経度'] = longitude_list

# 5. 地図の作成と点のプロット
# 成功したデータのみをフィルタリング
success_df = df.dropna(subset=['緯度', '経度'])

if not success_df.empty:
    # 日本の中心に近い適当な初期位置を設定
    map_center = [success_df['緯度'].mean(), success_df['経度'].mean()]
    m = folium.Map(location=map_center, zoom_start=6)

    # 各都市の位置をマーカーとして地図に追加
    for index, row in success_df.iterrows():
        city_name = str(row['都道府県']) + str(row['市名'])
        folium.Marker(
            location=[row['緯度'], row['経度']],
            popup=city_name,
            tooltip=city_name
        ).add_to(m)

    # 6. 地図をHTMLファイルとして保存
    output_html = '/content/drive/city_locations_map.html'
    m.save(output_html)
    print("\n-----------------------------------------------------")
    print(f"🎉 処理完了! 地図ファイルが '{output_html}' として保存されました。")
    print("ブラウザでこのファイルを開いて位置を確認してください。")
else:
    print("\n-----------------------------------------------------")
    print("データから有効な緯度・経度を取得できませんでした。地図は作成されません。")


if failed_addresses:
    print("\n--- 検索に失敗した住所 ---")
    for addr in failed_addresses:
        print(f"- {addr}")