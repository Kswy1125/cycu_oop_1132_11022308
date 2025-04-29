import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
from shapely.geometry import Point, LineString
import os
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# 設定中文字型（支援中文）
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'
matplotlib.rcParams['axes.unicode_minus'] = False

def read_route_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8')
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf

def draw_route_with_stop(input_files: list, outputfile: str, stop_name: str, marker_image_path: str):
    colors = ['blue', 'green', 'red', 'purple', 'orange']  # 預備多條線用不同顏色
    fig, ax = plt.subplots(figsize=(12, 12))

    stop_found = False
    stop_location = None

    for idx, file in enumerate(input_files):
        gdf = read_route_csv(file)
        color = colors[idx % len(colors)]

        # 繪製點
        gdf.plot(ax=ax, color=color, marker='o', markersize=5, label=f"路線 {os.path.basename(file)}")

        # 將點的 geometry 轉換為 LineString 並繪製線
        line_geometry = LineString(gdf.geometry.tolist())
        line_gdf = gpd.GeoDataFrame([1], geometry=[line_geometry], crs=gdf.crs)
        line_gdf.plot(ax=ax, color=color, linewidth=1)

        # 顯示每個站名，並檢查是否有匹配的站牌名稱
        for x, y, name in zip(gdf.geometry.x, gdf.geometry.y, gdf["車站名稱"]):
            ax.text(x, y, name, fontsize=6, ha='left', va='center')
            if name == stop_name:
                stop_found = True
                stop_location = (x, y)

    # 如果找到站牌，使用圖片標記該位置
    if stop_found and stop_location:
        try:
            img = Image.open(marker_image_path)
            imagebox = OffsetImage(img, zoom=0.1)  # 調整圖片大小
            ab = AnnotationBbox(imagebox, stop_location, frameon=False)
            ax.add_artist(ab)
        except FileNotFoundError:
            print(f"錯誤: 找不到標記圖片 '{marker_image_path}'")
    else:
        print(f"警告: 找不到站牌 '{stop_name}'")

    ax.set_title("多條公車路線圖")
    ax.set_xlabel("經度")
    ax.set_ylabel("緯度")
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    os.makedirs(os.path.dirname(outputfile), exist_ok=True)
    plt.savefig(outputfile, dpi=300)
    plt.close()

if __name__ == "__main__":
    input_files = [
        "data/bus_route_0161000900.csv",
        "data/bus_route_0161001500.csv"
    ]
    outputfile = "20250429/bus_routes_with_stop.png"
    marker_image_path = "C:/Users/User/Documents/GitHub/cycu_oop_1132_11022343/20250429/123.png"  # 修改為圖片的完整路徑

    # 輸入站牌名稱
    stop_name = input("請輸入站牌名稱: ")

    # 繪製地圖
    draw_route_with_stop(input_files, outputfile, stop_name, marker_image_path)

    print(f"地圖已儲存至 {outputfile}")
